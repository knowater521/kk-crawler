from datetime import datetime

import pymysql
from lxml import etree
import requests
import time

def getArea(vals):
    tex = ""
    for val in vals:
        tex = tex + ',' + val.text
    return tex

config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"123456",
    "database":"knowledge_db"
}
db = pymysql.connect(**config)
cursor = db.cursor()
sql = "INSERT INTO `tb_data_house` (`name`, `layout`, `area`, `address`, `price`, `unit`, `create_time`, `district`, `type`, `url`) " \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

error = 0
succeed = 0
for a in range(16):
    url = 'https://nn.newhouse.fang.com/house/s/b9{}'.format(a+1)
    print(url)
    data = requests.get(url)
    data.encoding = 'gb2312'
    tx = data.text
    s=etree.HTML(tx)
    houses = s.xpath('//*[@id="newhouse_loupai_list"]/ul/li')
    time.sleep(2)

    lists = []
    for house in houses:
        try:
            name = house.xpath("./div/div[2]/div[1]/div[1]/a/text()")[0].strip()
            layout = getArea(house.xpath("./div/div[2]/div[2]/a"))
            area = house.xpath("./div/div[2]/div[2]/text()")[0].strip()
            address = house.xpath("./div/div[2]/div[3]/div[1]/a/@title")[0].strip()
            price = house.xpath("./div/div[2]/div[5]/span/text()")[0].strip()
            unit = house.xpath("./div/div[2]/div[5]/em/text()")[0].strip()[0]
            district = house.xpath("./div/div[2]/div[3]/div[1]/a/text()")[0].strip().split(']')[0]
            type = 'fang.com'
            url = house.xpath("./div/div[2]/div[1]/div[1]/a/@href")[0].strip()
            row = (name, layout, area, address, price, unit, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), district, type, url)
            lists.append(row)
            print(row)
            succeed = succeed + 1
        except:
            error = error + 1
    cursor.executemany(sql, lists)
    db.commit()
    print("DB插入完成：" + str(len(lists)))

cursor.close()
db.close()
print("爬取完成，成功：" + str(succeed) + "条，失败：" + str(error) + "条")