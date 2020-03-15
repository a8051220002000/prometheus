#!/usr/bin/python3
#_*_ coding:utf-8 _*_
'''
此為部屬普羅米修斯exporter用
'''
import os,re,wget,tarfile,pwd,grp,shutil,socket

user = 'nodeusr'
DATA_URL = 'https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz'
SYSTEMD_URL = 'https://raw.githubusercontent.com/a8051220002000/prometheus/master/node_exporter.service'
NODE_URL = ''
DIR_NAME = 'node_exporter-0.17.0.linux-amd64'
DST = '/usr/local/bin/'


def download_file():
  # promethous server install
  out_fname = 'promethous_exporter.tgz'
  
  # wget檔案與壓縮
  wget.download(DATA_URL, out=out_fname)
  tar = tarfile.open(out_fname)
  tar.extractall()
  tar.close()
  os.remove(out_fname)
  
def createUser():
    try:
      pwd.getpwnam('nodeusr')
      print('user nodeusr exists')
    except KeyError:
      return  os.system("useradd -rs /bin/false nodeusr")

def mv_file():  
  # 搬移檔案
  shutil.copy(DIR_NAME+'/node_exporter', DST)  
  
  # 修改owner group
  os.chown(DST+'/node_exporter', uid, gid)


def firewalld():
  # 安裝firewalld 
  os.system("firewall-cmd --zone=public --permanent --add-port=9100/tcp")
  firwalld_status = os.popen("firewall-cmd --check-conf").read()
  # 確認firewall-cmd --check-conf 無誤就重啟
  if (firwalld_status == 'success\n'):
    os.system("firewall-cmd --reload")
  else:
    print('firewall check conf not success. please check config')

def start_service():
  # 配置systemctl文件
  wget.download(SYSTEMD_URL, out='./')
  shutil.copy('node_exporter.service', '/etc/systemd/system/')
  os.system("systemctl daemon-reload")
  os.system("systemctl enable node_exporter")
  os.system("systemctl start node_exporter")

def check_ip(ipAddr):
 compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$') 
 if compile_ip.match(ipAddr):
   wget.download(DATA_URL, out=out_fname)
   
 else:
   #無窮
   IP = input('IP輸入錯誤,重新輸入: ')
   check_ip(IP)
   


'''
download_file()
createUser()
# 獲取userid以及groupid 為了chown用
uid = pwd.getpwnam(user).pw_uid
gid = grp.getgrnam(user).gr_gid
mv_file()
firewalld()
start_service()
'''
IP = input('exporter部屬完成，請輸入pormetheus_server端ip: ')
check_ip(IP)