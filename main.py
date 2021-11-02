from wsgiref import headers
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import time
import random
url = "https://www.ozon.ru/product/albom-sketchbuk-kremovyy-a5-145h210-mm-100-g-m2-120-listov-proshivka-brauberg-art-classic-128961-161619975/reviews/"
headers = {
     "Accept":"*/*",
     "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
 }
reg = requests.get(url, headers=headers)
src = reg.text
print(src)

with open("index_Test.html", "w",encoding='utf-8') as file:
    file.write(src)
with open("index_Test.html",encoding='utf-8') as file:
    src = file.read()
soup = BeautifulSoup(src,"lxml")
name =soup.find(class_="ao5").text
# Списки для датафрема пандаса
buyer=[]
dignity=[]
limitations=[]
comment=[]
star_list=[]
i=1
time_to_stop=0
value=int(soup.find(class_="a4q5 a4q7").text)
print(value)
while value==i and time_to_stop==0:
    all_opinions = soup.find_all(class_="gb4")
    for item in all_opinions:
        star="-"
        if item.find(class_="MiSB").get("style")=="width:100%;":
            star=5
        elif item.find(class_="MiSB").get("style")=="width:80%;":
            star=4
        elif item.find(class_="MiSB").get("style")=="width:60%;":
            star=3
        elif item.find(class_="MiSB").get("style")=="width:40%;":
            star=2
        elif item.find(class_="MiSB").get("style")=="width:20%;":
            star=1
        elif item.find(class_="MiSB").get("style")=="width:0%;":
            star=0
        star_list.append(star)
        buyer.append(item.find(class_="e2w4").find(class_="e2w5").text)
        check_for_availability=item.find(class_="e2u8")
        if check_for_availability is None:
            print("Пустая")
            comment.append("-")
            dignity.append("-")
            limitations.append("-")
        else:
            blok_dlc=item.find(class_="e2u5 e2r6").find_all(class_="e2u8")
            blansion = ''

            for blok in blok_dlc:
                try:
                    buff = blok.find(class_="e2u7").text
                    buff = re.sub("^\s+|\n|\r|\s+$", '', buff)
                    if buff == "Достоинства":
                        dignity.append(blok.find(class_="e2u6").text)
                        blansion=blansion+'1'
                    elif buff == "Недостатки":
                        limitations.append(blok.find(class_="e2u6").text)
                        blansion = blansion + '2'
                    else:
                        comment.append(blok.find(class_="e2u6").text)
                        blansion = blansion + '3'
                except:
                        buff = blok.find(class_="e2u6").text
                        buff = re.sub("^\s+|\n|\r|\s+$", '', buff)
                        comment.append(blok.find(class_="e2u6").text)
                        dignity.append("-")
                        limitations.append("-")
            print(blansion)
            if blansion == '1':
                limitations.append("-")
                comment.append("-")
            elif blansion == '12':
                comment.append("-")
            elif blansion == '23':
                dignity.append("-")
            elif blansion == '3':
                dignity.append("-")
                limitations.append("-")
            elif blansion == '2':
                dignity.append("-")
                comment.append("-")
            elif blansion == '13':
                limitations.append("-")

    time.sleep(random.randrange(2,4))
    try:
        url = "https://www.ozon.ru" + soup.find(class_="a4q5 a4q7").find_next().get("href")
        reg = requests.get(url, headers=headers)
        src = reg.text
        with open("index_Test.html", "w",encoding='utf-8') as file:
            file.write(src)
        with open("index_Test.html",encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src,"lxml")
        try:
            value = int(soup.find(class_="a4q5 a4q7").text)
        except:
            time_to_stop=1
        i=i+1
        print(i)
    except:
        time_to_stop = 1
print(len(buyer),len(dignity),len(limitations),len(comment),len(star_list))
print(buyer)
output = pd.DataFrame({
    'Покупатель':buyer,
    'Достоинства':dignity,
    'Недостатки':limitations,
    'Комментарий':comment,
    'Оценка 1/5':star_list
})
output.to_csv('Результат парсинга.csv',index = False,sep='|',encoding='utf-8')
