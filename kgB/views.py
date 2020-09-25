import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import get_nodelist, get_relationshiplist, get_provincedict, get_scoreline, get_provinceID
# Create your views here.

def helloworld(request):
    return HttpResponse('Hello World!')

def kgB_index(request):
    province = get_provincedict()
    return render(request, 'kgB_index.html', {'province': province})

def kg_province(request):
    province = request.GET.get("select_province", '')
    node = get_nodelist(str(province))
    edge = get_relationshiplist(node)
    scoreline = get_scoreline(get_provinceID(province))
    request.encoding = 'utf-8'
    return render(request,
                  'kg_province.html',
                  {'node': json.dumps(node),
                   'edge': json.dumps(edge),
                   'scoreline': json.dumps({'data': scoreline}),
                   # 'firstLine2017Art': scoreline['firstLine2017Art'],
                   # 'firstLine2018Art': scoreline['firstLine2018Art'],
                   # 'firstLine2019Art': scoreline['firstLine2019Art'],
                   # 'firstLine2017Sci': scoreline['firstLine2017Sci'],
                   # 'firstLine2018Sci': scoreline['firstLine2018Sci'],
                   # 'firstLine2019Sci': scoreline['firstLine2019Sci'],
                   # 'secondLine2017Art': scoreline['secondLine2017Art'],
                   # 'secondLine2018Art': scoreline['secondLine2018Art'],
                   # 'secondLine2019Art': scoreline['secondLine2019Art'],
                   # 'secondLine2017Sci': scoreline['secondLine2017Sci'],
                   # 'secondLine2018Sci': scoreline['secondLine2018Sci'],
                   # 'secondLine2019Sci': scoreline['secondLine2019Sci'],
                   })
