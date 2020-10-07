#coding=utf-8
from django.urls import path
from . import views
urlpatterns = [
    path('', views.helloworld, name='hello'),
    path('MapVisualization/',name='MapVisualization'),#地图可视化
    path('KgBaseInfoFillin/',views.KgBaseInfoFillin,name='KgBaseInfoFillin'),#填写志愿信息
    path('KgBaseInfoFillin/questions/',views.InfoIntoQuestions,name="InfoIntoQuestions"),#返回志愿问题
    path('KgBaseInfoFillin/questions/answers/',views.ChooseFunction,name="QuestionsIntoAnswers"),#返回问题答案
    path('CollegeInfoGraphs',views.CollegeInfoGraphs,name='CollegeInfoGraphs'), #大学录取分数线
    path('MajorInfoGraphs',views.MajorInfoGraphs,name='MajorInfoGraphs'), #专业录取分数线
    path('TopUnivOfNeighbors',views.DisplayTopUnivOfNeighbors,name='TopUnivOfNeighbors'), #邻近省份一流大学显示
]