#!/usr/bin/python3
#_*_ coding:utf-8 _*_
'''
此為部屬普羅米修斯exporter用
'''
import os,re,wget,tarfile,pwd,grp,shutil

user = 'prometheus'
DATA_URL = 'https://github.com/prometheus/prometheus/releases/download/v2.8.1/prometheus-2.8.1.linux-amd64.tar.gz'
SYSTEMD_URL = 'https://raw.githubusercontent.com/a8051220002000/prometheus/master/prometheus.service'
DIR_NAME = 'prometheus-2.8.1.linux-amd64'
DST = '/usr/local/bin/'
DIR_PATH1 = '/etc/prometheus'
DIR_PATH2 = '/var/lib/prometheus'


def download_file():
  # promethous server install
  out_fname = 'promethous_server.tgz'
  
  # wget檔案與壓縮
  wget.download(DATA_URL, out=out_fname)
  tar = tarfile.open(out_fname)
  tar.extractall()
  tar.close()
  os.remove(out_fname)
  
def createUser():
    try:
      pwd.getpwnam('prometheus')
      print('user prometheus exists')
    except KeyError:
      return  os.system("useradd --no-create-home --shell /bin/false prometheus")

def mkdir():
  folder1 = os.path.exists(DIR_PATH1)
  folder2 = os.path.exists(DIR_PATH2)
  if not folder1:
    os.makedirs(DIR_PATH1)
    print (DIR_PATH1," create")
  if not folder2:
    os.makedirs(DIR_PATH2)
    print (DIR_PATH2," create")
    
def mv_file():  
  # 搬移檔案
  shutil.copy(DIR_NAME+'/prometheus', DST)
  shutil.copy(DIR_NAME+'/promtool', DST)
  shutil.copy(DIR_NAME+'/prometheus.yml', DIR_PATH1+'/')     
  #搬移資料夾
  shutil.copytree(DIR_NAME+'/consoles', DIR_PATH1+'/consoles')
  shutil.copytree(DIR_NAME+'/console_libraries', DIR_PATH1+'/console_libraries')
  
  # 修改owner group
  os.chown(DST+'/promtool', uid, gid)
  os.chown(DST+'/prometheus', uid, gid)
  os.chown(DIR_PATH1, uid, gid)
  os.chown(DIR_PATH2, uid, gid)   
 
def chown_recusive():
  # 做出chwon -R 效果，遞迴修改檔案及資料夾owner.group
  for root, dirs, files in os.walk(DIR_PATH1):  
    for i in dirs:  
      os.chown(os.path.join(root, i), uid, gid)
    for o in files:
      os.chown(os.path.join(root, o), uid, gid)   

def firewalld():
  # 安裝firewalld 
  os.system("firewall-cmd --zone=public --permanent --add-port=9090/tcp")
  firwalld_status = os.popen("firewall-cmd --check-conf").read()
  # 確認firewall-cmd --check-conf 無誤就重啟
  if (firwalld_status == 'success\n'):
    os.system("firewall-cmd --reload")
  else:
    print('firewall check conf not success. please check config')

def start_service():
  # 配置systemctl文件
  wget.download(SYSTEMD_URL, out='./')
  shutil.copy('prometheus.service', '/etc/systemd/system/')
  os.system("systemctl daemon-reload")
  os.system("systemctl enable prometheus")
  os.system("systemctl start prometheus")




download_file()
createUser()
# 獲取prometheus的userid以及groupid 為了chown用
uid = pwd.getpwnam(user).pw_uid
gid = grp.getgrnam(user).gr_gid
mkdir()
mv_file()
chown_recusive()
firewalld()
start_service()