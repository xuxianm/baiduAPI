import requests
import json
import csv
import sys
import time
import pymysql
conn = pymysql.connect(host='172.16.5.10', port=3306, user='root', passwd='183217', charset='utf8', db='xn-poi')
cusor = conn.cursor()

#左下角坐标
lef_bottom='36.543753,101.632419'
#右上角坐标
right_top='36.762873,101.924189'
ak = 'EdXKC0zvR8OKAqvjTvot0E9OjayYo1ex'
region = input('请输入要查询的城市:')
tag = input('请输入查询类别：')
query = input('请输入查询内容：')
print('你要查询的是{}市{}类的{}'.format(region,tag,query))
for i in range(20):
    page_num = str(i)
    print(page_num)
    #print(type(page_num))
    url = 'http://api.map.baidu.com/place/v2/search?query=' + query + tag + '&region=' + region + '&page_num=' + page_num + '&output=json&ak=EdXKC0zvR8OKAqvjTvot0E9OjayYo1ex'
    #url = 'http://api.map.baidu.com/place/v2/search?query=' + query + '&bounds=' + lef_bottom + ','+ right_top + '&page_num=' + page_num + '&output=json&ak='+ ak
    html = requests.get(url)
    data = html.json()
    #print(data['results'])
    for item in data['results']:
        name = item['name']
        lat = str(item['location']['lat'])
        lng = str(item['location']['lng'])
        address = item['address']
        prov = item['province']
        city = item['city']
        area = item['area']
        phone = item.get('telephone')
        info =(name,query,lat,lng,address,prov,city,area,phone)
        print(info)
        sql = "insert into shuba(name,class,query,lat,lng,address,prov,city,area,phone) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(name,tag,query,lat,lng,address,prov,city,area,phone)
        print(sql)
        cusor.execute(sql)
conn.commit()
conn.close()
print('{}市的{}类的{}已查询完成'.format(city,tag,query))


