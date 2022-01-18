# -*- coding: utf-8 -*-
import requests
import time
url="https://wenshu.court.gov.cn/website/parse/rest.q4w"
all_of_court=[]
province_code=sorted([850,451,1,51,1100,2950,100,300,600,750,1150,1300
    ,1451,1600,1700,1850,2050,2250,2400,2550,2900,3000,3250,3350,
    3600,3750,3900,451,2750,3500,4000,4050])


headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
with open("court_name.txt", 'w+') as f:
    for i in range(1,4050):
        data={
            "provinceCode": i,
            "searchParent": "false",
            "cfg": "com.lawyee.judge.dc.parse.dto.LoadDicDsoDTO@loadFy",
            "__RequestVerificationToken": "5ePpXU9JSdJgJEOkbSXyNg8a"
        }
        response=requests.post(url=url,headers=headers,data=data)
        print(response.text)
        dic=response.json()
        templist=dic['result']['fy']
        for j in range(len(templist)):
            all_of_court.append(templist[j]['name'])
            f.write(templist[j]['name']+" 3 ORG\n")
        time.sleep(0.5)
