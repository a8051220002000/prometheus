#!/bin/bash

#關閉selinux
se_status=$(echo $(getenforce))

if [[ ${se_status} != 'Disabled' ]];then
  setenforce 0
  #抓取第幾行是設定SELINUX=
  line=$(grep -n 'SELINUX='  /etc/selinux/config  |grep -v '#'|awk -F':' '{print $1}')
  if [[ $(echo ${line}|wc -l) -ne 1 ]];then
    echo '/etc/selinux/config 設定超過一行,請手動修改配置成SELINUX=disabled'
    exit 1
  fi
  #移除該行
  sed -i "${line}"d /etc/selinux/config
  #在該行插入
  sed -i "${line}iSELINUX=disabled" /etc/selinux/config
fi

yum install python36 lrzsz ntpdate -y
echo '0  10  *  *  * root ntpdate -u tw.pool.ntp.org' >> /etc/crontab
python3 -m ensurepip
pip3 install --upgrade pip
pip3 install wget


