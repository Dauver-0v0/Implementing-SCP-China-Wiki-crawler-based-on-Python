import requests
import csv
import json
import re
from bs4 import BeautifulSoup

def getHTMLText(url):   #函数getHTMLText用于获取网页内容，返回html的文本
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ''

def getList(html):    #得到各个界面的四个参数
    list_1 = []
    t = 0
    soup = BeautifulSoup(html, 'html.parser')
    main_content = soup.find('div', {'id': 'main-content'})
    try:
        p_tags = main_content.find_all('p')
    except:
        return 0
    for tag in p_tags:    #找到目标
        text = tag.get_text(strip=True)
        o_1 = re.search(r'项目编号', text)
        o_2 = re.search(r'项目等级', text)
        o_3 = re.search(r'特殊收容措施', text)
        o_4 = re.search(r'描述', text)
        o_5 = re.search(r'項目編號', text)
        o_6 = re.search(r'項目等級', text)
        if o_1 or o_2 or o_3 or o_4 or o_5 or o_6:
            t += 1
            text = text.replace('项目编号：', '')
            text = text.replace('项目等级：', '')
            text = text.replace('特殊收容措施：', '')
            text = text.replace('描述：', '')
            text = text.replace('項目編號：', '')
            text = text.replace('項目等級：', '')
            list_1.append(text)
    if t == 4:
        return list_1
    else:   #去除收容失效的项目
        return 0

def create_Bar(i,j):   #制作进度条
    a = '█' * (i - j + 1) * 2
    b = '█' * (j + 9 - i) * 2
    c = (i - j + 1) * 10
    print("\r{:>3}%[{:}->{:}]".format(c,a,b),end='')

def page_list(j):     #建立二维列表

    list_1 = [['项目编号', '项目等级', '特殊收容措施', '描述']]
    for i in range(j,j+10):
        create_Bar(i,j)
        if 1 <= i < 100 :
            t = str(i).rjust(3,'0')
            url = 'http://scp-wiki-cn.wikidot.com/scp-' + t
        else:
            url = 'http://scp-wiki-cn.wikidot.com/scp-' + str(i)
        test_1 = getList(getHTMLText(url))
        if test_1 == 0 :
            l_test = 'SCP-' + str(i) + '收容失效'
            list_1.append([l_test, '无数据', '无数据', '无数据'])
        else:
            list_1.append(test_1)
    print('\n')
    return list_1


def transToCSV(list_1):   #存放csv文件
    url = input("请输入csv文件要存放的位置与文件名（例如E:\list_csv.csv）：")
    url = url.replace('\\', '/')
    with open(url, 'w', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in list_1:
            writer.writerow(row)
        print(f'{f}文件已创建成功！')
        f.close()

def transToJSON(list_1):   #存放json文件
    url = input("请输入json文件要存放的位置与文件名（例如E:\list_json.json）：")
    #url = 'E:\list_json.json'
    url = url.replace('\\', '/')
    for i in range(1, len(list_1)):
        #print(i,list_1[0],list_1[i])
        list_1[i] = dict(zip(list_1[0], list_1[i]))
    with open(url, 'w', encoding="utf-8", newline="") as f:
        json.dump(list_1[1:], f, ensure_ascii=False)
        print(f'{f}文件已创建成功！')
        f.close()

j = int(input("请输入需要查询的10个连续SCP项目的首个编号："))
print("正在进行数据爬取，请稍后\n")
list_1 = page_list(j)
if list_1 == 0 :
    print("\n抱歉，未查询到该段的SCP项目")
#print(list_1)
else:
    transToCSV(list_1)
    transToJSON(list_1)
#url = "http://scp-wiki-cn.wikidot.com/scp-173"
#url = "http://scp-wiki-cn.wikidot.com/scp-series"
#print(getList(getHTMLText(url)))

