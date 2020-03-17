#!/usr/bin/python3
#_*_ coding:utf-8 _*_

import requests,json

headers = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": "Bearer eyJrIjoiNExxNVlXQ3ZHeTkzbFdqSEd0OFVlT2xmMWhMbm1wdlIiLCJuIjoiYWRtaW4iLCJpZCI6MX0="
           }

r = requests.get("http://192.168.1.89:3000", headers=headers)
#print(r.text)
#print(r.status_code)


dashboard = {"id": "None",
             "uid": "dsafasdfdas",
             "title": "Production Overview",
             "tags": [ "templated" ],
             "timezone": "browser",
             "schemaVersion": 16,
             "version": 0
            }

payload = {"dashboard": dashboard } 

url = "http://192.168.1.89:3000/api/dashboards/db"

p = requests.post(url, headers=headers, json=payload)
#print(p)
print(p.status_code)
print(p.text)


