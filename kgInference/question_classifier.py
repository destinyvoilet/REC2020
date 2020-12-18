#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.score_path=os.path.join(cur_dir, 'dict/score.txt')
        self.year_path=os.path.join(cur_dir, 'dict/year.txt')
        self.university_path = os.path.join(cur_dir, 'dict/university.txt')
        self.major_path = os.path.join(cur_dir, 'dict/major.txt')
        self.province_path = os.path.join(cur_dir, 'dict/province.txt')
        # 加载特征词
        self.university_wds= [i.strip() for i in open(self.university_path,encoding="utf-8") if i.strip()]
        self.major_wds= [i.strip() for i in open(self.major_path,encoding="utf-8") if i.strip()]
        self.province_wds= [i.strip() for i in open(self.province_path,encoding="utf-8") if i.strip()]
        self.score_wds=[i.strip() for i in open(self.score_path,encoding='utf-8') if i.strip()]
        self.year_wds=[i.strip() for i in open(self.year_path,encoding='utf-8') if i.strip()]
        self.jbw_wds=["985"]
        self.eyy_wds=["211"]
        self.doubleclass_wds=["一流大学",'一流学科']
        self.region_words = set(self.university_wds + self.major_wds + self.province_wds+self.score_wds+
        self.year_wds+self.jbw_wds+self.eyy_wds+self.doubleclass_wds)
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        self.firstline_wds=["一本","一本线"]
        self.secondline_wds=["二本",'二本线']
        self.rank_wds=['排名','名次']
        self.score_wds=['分']
        self.year_wds=['2016','2017','2018','2019','2020','2021']
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.university_qwds = ['能上','能不能上','想上', '报考', '学校','什么学校',
        '能上什么985','能上哪些985','能不能上985','能上什么211','能上哪些211','能不能上211']
        self.major_qwds = ['专业','学院', '系','什么专业','什么专业好','互联网','医院',
        '电网','工厂','青春饭']
        self.province_qwds = ['省份', '省', '自治区', '直辖市', '特区','北京','天津',
        '河北','山西','内蒙古','宁夏','青海',
        '陕西','甘肃','新疆','辽宁','吉林','黑龙江','山东','江苏','上海','浙江',
        '安徽','福建','江西','河南','湖南','湖北','四川','贵州','云南','重庆','西藏'
        ,'广东','广西','海南','香港','澳门','台湾']
        self.jbw_qwds=['是不是985','是985吗']
        self.eyy_qwds=['是不是211','是211吗']
        self.doubleclass_qwds=['是不是双一流','是不是一流大学','是不是一流学科','是双一流吗','是一流大学吗',
        '是一流学科吗']
        self.score_qwds=['要多少分','多少分能上','多少分有机会','多少分能稳上','多少分能冲一下']
        self.rank_qwds=['排多少名','排名','什么排名','排名怎么样']
        self.firstline_qwds=['一本线','上一本要多少分','多少分能上一本']
        self.secondline_qwds=['二本线','上二本要多少分','多少分能上二本']
        self.year_qwds=['2016','2017','2018','2019','2020','2021']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        school_dict = self.check_school(question)
        if not school_dict:
            return {}
        data['args'] = school_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in school_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        """
        #一所大学的哪些专业好
        if self.check_words(self.university_qwds, question) and ('major' in types):
            question_type = 'university_major'
            question_types.append(question_type)
        """
        """
        #一个专业哪些大学强
        if self.check_words(self.major_qwds, question) and ('university' in types):
            question_type = 'major_university'
            question_types.append(question_type)
        """
        """
        #大学在那个省
        if self.check_words(self.university_qwds, question) and ('province' in types):
            question_type = 'university_province'
            question_types.append(question_type)
        """
        #X省有哪些大学
        if self.check_words(self.province_qwds, question) and ('university' in types):
            question_type = 'province_university'
            question_types.append(question_type)
        """
        #上XX大学要多少分
        if self.check_words(self.university_qwds, question) and ('score' in types):
            question_type = 'university_score'
            question_types.append(question_type)
        """
        """
        #XX分能上哪些大学
        if self.check_words(self.score_qwds, question) and ('university' in types):
            question_type = 'score_university'
            question_types.append(question_type)
        """
        """
        #XX大学是不是985
        if self.check_words(self.university_qwds, question) and ('985' in types):
            question_type = 'university_985'
            question_types.append(question_type)
        """
        """
        #有哪些大学是985
        if self.check_words(self.jbw_qwds, question) and ('university' in types):
            question_type = '985_university'
            question_types.append(question_type)
        """
        """
        #XX大学是不是211
        if self.check_words(self.university_qwds, question) and ('211' in types):
            question_type = 'university_211'
            question_types.append(question_type)
        """
        """
        #有哪些大学是211
        if self.check_words(self.eyy_qwds, question) and ('university' in types):
            question_type = '211_university'
            question_types.append(question_type)
        """
        """
        #XX大学是不是双一流
        if self.check_words(self.university_qwds, question) and ('985' in types):
            question_type = 'university_doubleclass'
            question_types.append(question_type)
        """
        """
        #有哪些大学是双一流
        if self.check_words(self.jbw_qwds, question) and ('university' in types):
            question_type = 'doubleclass_university'
            question_types.append(question_type)
        """
        #XX省的一本线
        if self.check_words(self.province_qwds,question) and ('firstline' in types):
            question_type='province_firstline'
            question_types.append(question_type) 
        #XX省的二本线
        if self.check_words(self.province_qwds,question) and ('secondline' in types):
            question_type='province_secondline'
            question_types.append(question_type)
        #排名
        if self.check_words(self.province_qwds,question) and ('rank' in types) and ('year' in types):
            question_type='province_year_rank'
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.university_wds:
                wd_dict[wd].append('university')
            if wd in self.major_wds:
                wd_dict[wd].append('major')
            if wd in self.province_wds:
                wd_dict[wd].append('province')
            if wd in self.score_wds:
                wd_dict[wd].append('score')
            if wd in self.year_wds:
                wd_dict[wd].append('year')
            if wd in self.jbw_wds:
                wd_dict[wd].append('985')
            if wd in self.eyy_wds:
                wd_dict[wd].append('211')
            if wd in self.doubleclass_wds:
                wd_dict[wd].append('doubleclass')#意为双一流
            if wd in self.firstline_wds:
                wd_dict[wd].append('firstline')#一本线
            if wd in self.secondline_wds:
                wd_dict[wd].append('secondline')#二本线
            if wd in self.rank_wds:
                wd_dict[wd].append('rank')#排名
            if wd in self.year_wds:
                wd_dict[wd].append('year')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_school(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)