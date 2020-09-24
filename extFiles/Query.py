import pandas as pd
import time
import os
import six
import numpy as np
import matplotlib.pyplot as plt

'''
# 接收大学，科类，年份，省份为输入参数，展示大学该年份在该省的各专业分数情况及排名
def query_1(college, Category, year, Province):  # year必须是自然数，in17，18，19
    """
    college:是大学名称
    Category:是科类，是{"理科","文科","不分文理"}
    year:年份只能是2019，2018，2017，应该是数字类型
    province:省份名称
    """
    table = pd.read_csv(f"final_{year}.csv")#这个地方是文件名称，可能要改
    #table=pd.read_csv('D:\大三短学期课程\软件实践2\my_work\iseu2012-rec2020-master\\rec2020\extFiles\\final_2018.csv')
    table.columns = ["College", "Year", "Province", "Category", "Major", "Score"]  # 加入标题行
    tar_major = []
    tar_score = []
    for item in table.iterrows():
        if item[1][0] == college and item[1][2] == Province and item[1][3] == Category:
            tar_major.append(item[1][4])
            tar_score.append(item[1][5])
    Data = {"Major": tar_major,
            "Socre": tar_score}
    Data_f = pd.DataFrame(Data)

    return Data_f
'''


# 绘图函数
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=12,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return fig


def query_1(college, Category, year, Province):  # year必须是自然数，in17，18，19
    """
    college:是大学名称
    Category:是科类，是{"理科","文科","不分文理"}
    year:年份只能是2019，2018，2017，应该是数字类型
    province:省份名称
    """
    path = "final_" + str(year) + ".csv"
    table = pd.read_csv(path)  # 这个地方是文件名称，可能要改
    # table=pd.read_csv('D:\大三短学期课程\软件实践2\my_work\iseu2012-rec2020-master\\rec2020\extFiles\\final_2018.csv')

    table.columns = ["College", "Year", "Province", "Category", "Major", "Score"]  # 加入标题行
    tar_major = []
    tar_score = []
    tar_rank = []
    for item in table.iterrows():
        if item[1][0] == college and item[1][2] == Province and item[1][3] == Category:
            tar_major.append(item[1][4])
            tar_score.append(item[1][5])
            name = str(year) + Province + Category
            path = "json_csv//" + name + ".csv"
            table2 = pd.read_csv(path)
            temp1 = 0
            for i in table2.iterrows():
                if i[1][1] > item[1][5]:
                    temp1 = i[1][2]
                if i[1][1] <= item[1][5]:
                    tar_rank.append(temp1 + 1)
                    break

    Data = {"Major": tar_major,
            "Socre": tar_score,
            "Rank": tar_rank}
    Data_f = pd.DataFrame(Data)
    fig = render_mpl_table(Data_f)

    return fig


start = time.time()
res1 = query_1('东南大学', '理科', 2018, '山西')  # 大约8s
print(res1)
end = time.time()
print(f'1号查询花费时间{end - start}s')
print("#######################################################################")
start = time.time()
res1 = query_1('东南大学', '理科', 2018, '山西')  # 大约8s

print(res1)
end = time.time()
print(f'1号查询花费时间{end - start}s')
print("#######################################################################")


# 查询某年某省某类别的一分一段表，我们在数据集的名称上进行了微调
def score_iqury(Year, Category, Province):
    """
    是用来展示一分一段表的,我们将一分一段表的奇怪后缀去掉了，如果是all，则category设置为all即可
    Year:年份只能是2019，2018，2017，应该是数字类型
    Category:是科类，是{"理科","文科","不分文理"}
    province:省份名称
    """
    year = str(Year)
    name = year + Province + Category
    path = "json_csv//" + name + ".csv"
    df1 = pd.read_csv(path)
    df2 = df1.drop(['Unnamed: 0', '省份', '年份', '科类'], axis=1)
    fig = render_mpl_table(df2)

    return fig


start = time.time()
res2 = score_iqury(2018, '理科', '山西')
print(res2)
end = time.time()
print(f'一分一段表号查询花费时间{end - start}s')
print("#######################################################################")


# 接收的输入为分数，省份，科目类别，这个输入的年份应自动标记为当前年份，用以看去年的分数情况,分数上下波动10分
def query_2(score, province, category, year=2020, wave=10):
    """
    这个用来展示用户分数在去年上下波动10分有哪些选择的情况。
    wave:是分数上下波动所允许的范围
    """
    # table = pd.read_csv(f"final_{year}.csv")  # 这个地方是文件名称，可能要改
    table = pd.read_csv('D:\大三短学期课程\软件实践2\my_work\iseu2012-rec2020-master\\rec2020\extFiles\\final_2018.csv')
    table.columns = ["College", "Year", "Province", "Category", "Major", "Score"]  # 加入标题行
    tar_major = []
    tar_score = []
    tar_college = []
    tar_province = []
    for item in table.iterrows():
        if item[1][5] <= score + wave and item[1][5] >= score - wave and item[1][2] == province and item[1][
            3] == category:
            tar_major.append(item[1][4])
            tar_score.append(item[1][5])
            tar_college.append(item[1][0])
            tar_province.append(item[1][2])
    Data = {"College": tar_college, "Major": tar_major,
            "Socre": tar_score, 'Province': tar_province}
    Data_f = pd.DataFrame(Data)
    fig = render_mpl_table(Data_f)
    return fig


start = time.time()
res3 = query_2(625, '山西', '理科', 2019)
print(res3)
end = time.time()
print(f'2号查询查询花费时间{end - start}s')
print("#######################################################################")

def main(Province="",Grade=0,Year=2019,Category="",College=""):
    if Year in [2017,2018,2019]:
        if College!="" and Grade=="":
            res=query_1(College,Category,Year,Province)
        elif College=="" and Grade!="":
            res=query_2(Grade,Province,Category,Year)
        elif College=="" and Grade=="":
            res=score_iqury(Year,Category,Province)
        else:
            return
    else:
        return
    return res


