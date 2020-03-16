#!/usr/bin/python3
#_*_ coding:utf-8 _*_
'''
此為部屬普羅米修斯exporter用
'''
import os,re,wget,tarfile,pwd,grp,shutil,socket

def install_service():
  # 安裝gafana
  os.system("yum install grafana -y ")
  # 安裝firewalld 
  os.system("firewall-cmd --zone=public --permanent --add-port=3000/tcp")
  firwalld_status = os.popen("firewall-cmd --check-conf").read()
  # 確認firewall-cmd --check-conf 無誤就重啟
  if (firwalld_status == 'success\n'):
    os.system("firewall-cmd --reload")
  else:
    print('firewall check conf not success. please check config')

def start_service():
  # 配置systemctl文件
  os.system("systemctl daemon-reload")
  os.system("systemctl start grafana-server")
  os.system("systemctl enable grafana-server")


install_service()
start_service()
