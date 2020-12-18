from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher
from rec2020.settings import graph

# Create your models here.

def get_provinceID(province):
    """
    获取省份ID
    :param province: 省份, string; 例如: '河南'
    :return: 省份ID, int; 例如: 1
    """
    query = "match (n:`省份`) where n.Name='" + str(province)+ "' return n"
    resultDict = dict(graph.run(query).data()[0]['n'])
    return resultDict['ID']

def get_collegesInProvince(province):
    """
    获取特定省份内的大学列表
    :param province: 省份, string; 例如: '河南'
    :return: 一个 大学信息字典 的列表
    """
    query = "MATCH (n:`学校`)-[:located]-(p:`省份`) WHERE p.Name='" + str(province)+ "' RETURN n"
    collegesInProvince = []
    result = graph.run(query).data()
    for item in result:
        collegesInProvince.append(dict(item['n']))
    return collegesInProvince

def get_scoreinfo(province):
    """
    获取指定省份的分数信息
    :param province: 省份, string; 例如: '河南'
    :return: 分数信息列表
    """
    scoreinfolist = []
    matcher = NodeMatcher(graph)
    data = matcher.match("分数信息", provinceID=get_provinceID(province)).all()
    for item in data:
        d = dict(item)
        if d['category']=='文科':
            char = 'w'
        elif d['category']=='理科':
            char = 'l'
        else:
            char = 'z'
        scoreinfo = {'id': str(d['year'])+char,
                     'name': str(d['year'])+d['category'][0],
                     'category': char,
                     'year': d['year'],
                     'province': province,
                     }
        scoreinfolist.append(scoreinfo)
    return scoreinfolist

def get_nodelist(province):
    """
    获取特定省份的节点列表（用于知识图谱可视化）
    注：此处只获取了省内211院校，而非全部
    :param province: 省份, string; 例如: '河南'
    :return: 结点列表
    """
    nodelist = []
    # append college nodes
    collegelist = get_collegesInProvince(province)
    for item in collegelist:
        if item['_211_']:
            nodelist.append(
                {'data': {'id': str(item['ID']), 'name': item['Name'], 'label': 'college'}}
            )
    # append province node
    nodelist.append({'data': {'id': str(get_provinceID(province)), 'name': province, 'label': 'province'}})
    # append scoreinfo nodes
    scoreinfolist = get_scoreinfo(province)
    for item in scoreinfolist:
        item['label'] = 'scoreinfo'
        nodelist.append({'data': item})
    # append scoreline and rank
    linklist = get_scoreinfolink(province)
    for item in linklist:
        nodelist.append({'data': item})
    return nodelist

def get_relationshiplist(nodelist):
    college_list = []
    scoreinfo_list = []
    firstline_list = []
    secondline_list = []
    ranktable_list = []

    for item in nodelist:
        label = item['data']['label']
        if (label == 'college'):
            college_list.append(item)
        elif (label == 'province'):
            provinID = item['data']['id']
        elif (label == 'scoreinfo'):
            scoreinfo_list.append(item)
        elif (label == 'firstline'):
            firstline_list.append(item)
        elif (label == 'secondline'):
            secondline_list.append(item)
        elif (label == 'ranktable'):
            ranktable_list.append(item)

    relationshiplist = []
    for item in college_list:
        relationshiplist.append({'data': {'source': str(item['data']['id']), 'target': str(provinID), 'relationship':''}}) # 'relationship':'located'
    for item in scoreinfo_list:
        relationshiplist.append({'data': {'source': str(item['data']['id']), 'target': str(provinID), 'relationship':''}}) # 'relationship':'score_province'
    for item in firstline_list:
        relationshiplist.append({'data': {'source': str(item['data']['id']), 'target': str(item['data']['id'])[0:5], 'relationship':'line1'}})
    for item in secondline_list:
        relationshiplist.append({'data': {'source': str(item['data']['id']), 'target': str(item['data']['id'])[0:5], 'relationship':'line2'}})
    for item in ranktable_list:
        relationshiplist.append({'data': {'source': str(item['data']['id']), 'target': str(item['data']['id'])[0:5], 'relationship':'rank'}})

    return relationshiplist

def get_provincedict():
    """
    获得 省份ID-省份 的对应字典
    :return: 省份ID-省份 字典, dict; 例如:{"1": "北京", "2": "天津", "3":"江苏"}
    """
    query = "MATCH (n:`省份`) RETURN n"
    data = graph.run(query).data()
    provincedict = dict()
    for item in data:
        d = dict(item['n'])
        provincedict[str(d['ID'])] = d['Name']
    return provincedict

def get_ranktable(provinceID, year, category):
    """
    获取一分一段表
    :param provinceID: 省份编号, int
    :param year: 年份, int
    :param category: 科类, string
    :return: 一分一档字典, dict; 例如:{700: 20, 695: 26, 690: 38, 685: 50, ...}
    """
    matcher = NodeMatcher(graph)
    data = matcher.match("分数信息",
        provinceID=provinceID,
        year=year,
        category=category).all()[0]
    scoreinfo = dict(data)
    if(len(scoreinfo['score']) != len(scoreinfo['cumulateNumber'])):
        raise IndexError
    ranktable = dict()
    for score, rank in zip(scoreinfo['score'], scoreinfo['cumulateNumber']):
        ranktable[score] = rank
    return ranktable

def get_scoreinfolink(province):
    provinceID = get_provinceID(province)
    matcher = NodeMatcher(graph)
    scoreinfo_nodes = matcher.match("分数信息", provinceID=provinceID).all()
    scoreinfo_lists = []
    for node in scoreinfo_nodes:
        scoreinfo_list = []
        cate = node['category']
        year = node['year']
        scorenum = len(node['scoreLineClass'])
        if cate == '文科':
            catechar = 'w'
        elif cate == '理科':
            catechar = 'l'
        else:
            catechar = 'z'
        first, second = {'id': str(year) + catechar + 'f', 'name': 0, 'label': 'firstline'}, {
            'id': str(year) + catechar + 's', 'name': 0, 'label': 'secondline'}
        if scorenum == 1:
            first['name'] = node['scoreLineValue'][0]
            scoreinfo_list.append(first)
        elif scorenum >= 2:
            first['name'] = node['scoreLineValue'][0]
            scoreinfo_list.append(first)
            second['name'] = node['scoreLineValue'][0]
            scoreinfo_list.append(second)
        score1, score100, score1000 = {'id': str(year) + catechar + 'r1', 'name': 0, 'label': 'ranktable'}, {
            'id': str(year) + catechar + 'r100', 'name': 0, 'label': 'ranktable'}, {
                                          'id': str(year) + catechar + 'r1000', 'name': 0, 'label': 'ranktable'}
        if 1 in node['cumulateNumber']:
            index1 = node['cumulateNumber'].index(1)
            score1['name'] = '第1名: '+str(node['score'][index1])+'分'
            scoreinfo_list.append(score1)
        if 100 in node['cumulateNumber']:
            index100 = node['cumulateNumber'].index(100)
            score100['name'] = '第100名: '+str(node['score'][index100])+'分'
            scoreinfo_list.append(score100)
        if 1000 in node['cumulateNumber']:
            index1000 = node['cumulateNumber'].index(1000)
            score1000['name'] = '第1000名: '+str(node['score'][index1000])+'分'
            scoreinfo_list.append(score1000)

        scoreinfo_lists.append(scoreinfo_list)

    scorelinelist = []
    for item1 in scoreinfo_lists:
        for item2 in item1:
            scorelinelist.append(item2)
    return scorelinelist

def get_scoreline(provinceID):
    scoreline = {
        'firstLine2017Art': -1,
        'firstLine2018Art': -1,
        'firstLine2019Art': -1,
        'firstLine2017Sci': -1,
        'firstLine2018Sci': -1,
        'firstLine2019Sci': -1,
        'secondLine2017Art': -1,
        'secondLine2018Art': -1,
        'secondLine2019Art': -1,
        'secondLine2017Sci': -1,
        'secondLine2018Sci': -1,
        'secondLine2019Sci': -1,
    }
    matcher = NodeMatcher(graph)
    data = matcher.match("分数信息", provinceID=provinceID).all()
    for item in data:
        d = dict(item)
        if d['category'] == '文科':
            cate = ['Art']
        elif d['category'] == '理科':
            cate = ['Sci']
        elif d['category'] == '综合':
            cate = ['Art', 'Sci']
        # get the length of score line data
        if len(d['scoreLineValue']) > 2:
            length = 2
        else:
            length = len(d['scoreLineValue'])
        # assignment
        for i in range(length):
            for word in cate:
                if not i:
                    scoreline['firstLine' + str(d['year']) + word] = d['scoreLineValue'][i]
                else:
                    scoreline['secondLine' + str(d['year']) + word] = d['scoreLineValue'][i]
    return scoreline
