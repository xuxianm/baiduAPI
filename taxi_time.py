import requests
import json

import datetime
import pymysql
conn = pymysql.connect(host='172.16.5.10', port=3306, user='root', passwd='183217', charset='utf8', db='xn-poi')
cusor = conn.cursor()


ak = 'EdXKC0zvR8OKAqvjTvot0E9OjayYo1ex'
#region = input('请输入要查询的城市:')
tag1 = '房地产'
query1 = '小区'
region_list =['西宁市城东区','西宁市城西区','西宁市城中区','西宁市城北区']
i=0
j=0
for i in range(4):
    #始发地的区
    start_region = region_list[i]

    for j in range(4):
        #目的地的区
        end_region = region_list[j]
        start_url = 'http://api.map.baidu.com/place/v2/search?query=' + query1 + '&tag=' + tag1 + '&region=' + start_region + '&output=json&ak=IyBt2aQhVm6fkjC0iqFrRx1RBRetd75v'
        start_html = requests.get(start_url)
        start_data = start_html.json()
        for item in start_data['results']:
            start_name = item['name']
            #origin = str(item['location'])
            start_lat = str(item['location']['lat'])
            start_lng = str(item['location']['lng'])
            start_address = item['address']
            start_area = item['area']
            tag2 = '政府机构'
            # 政府机构 公司企业
            query2 = '西宁市单位'
            # 青海省单位 西宁市单位 公司
            end_url = 'http://api.map.baidu.com/place/v2/search?query=' + query2 + '&tag=' + tag2 + '&region=' + end_region + '&output=json&ak=IyBt2aQhVm6fkjC0iqFrRx1RBRetd75v'
            end_html = requests.get(end_url)
            end_data = end_html.json()
            for item in end_data['results']:
                end_name = item['name']
                #destination = str(item['location'])
                end_lat = str(item['location']['lat'])
                end_lng = str(item['location']['lng'])
                end_address = item['address']
                end_area = item['area']
                #print(start_name,end_name,start_area,end_area,start_lat,start_lng,end_lat,end_lng)
                trans_url = 'http://api.map.baidu.com/direction/v2/driving?origin=' + start_lat +',' + start_lng + '&destination=' + end_lat +',' + end_lng + '&ak=IyBt2aQhVm6fkjC0iqFrRx1RBRetd75v'
                print(trans_url)
                trans_html = requests.get(trans_url)
                trans_data = trans_html.json()
                #print(trans_data)
                #print(type(trans_data))
                if(trans_data['result']):
                    style = '驾车/Taxi'
                    #print(trans_data['result']['routes'][0]['distance'])
                    if(trans_data['result']['routes'][0]['distance'] > 10):
                        a =trans_data['result']['routes'][0]
                        distance = a['distance']
                        duration = a['duration']
                        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()[1]
                        value =(start_name, end_name, start_area, end_area,distance,duration,style,time)
                        print(value)
                        sql = 'insert into trip_time(origin,destination,origin_area,destination_area,distance,duration,style,time) values{}'.format(value)
                        cusor.execute(sql)
                        conn.commit()

                else:
                    continue

conn.close()





