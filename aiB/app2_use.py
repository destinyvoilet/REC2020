import csv
from PIL import Image,ImageFont,ImageDraw

def application2(str):
    list=[]
    with open('大学内专业评级(正式).csv', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        #print(type(reader))
        for row in reader:
            if(row[1]==str):
                list.append([row[2]+' '+row[3]])
    print(list)
    text = "'字数长度限制(字数长度限制AAA) D'"
    font = ImageFont.truetype("font.ttf", 18)
    lines = list
    line_height = font.getsize(text)[1]
    img_height = line_height * (lines.__len__()+1)
    im = Image.new("RGB", (600, img_height), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    x, y = 5, 5
    for line in lines:
        dr.text((x, y), line[0], font=font, fill="#000000")
        y += line_height
    im.save("majorRank.jpg")

#测试
#application2('兰州大学')
