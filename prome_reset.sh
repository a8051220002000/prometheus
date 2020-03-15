#!/bin/bash

#刪除普羅米修斯部屬步驟

function sv_p(){
rm -rf /etc/prometheus
rm -rf /var/lib/prometheus
rm -rf prometheus-2.8.1.linux-amd64
userdel  prometheus
rm -rf /usr/local/bin/promtool
rm -rf /usr/local/bin/prometheus
firewall-cmd --zone=public --remove-port=9090/tcp --permanent
systemctl stop prometheus
systemctl disable prometheus
rm -rf /etc/systemd/system/prometheus.service
rm -rf prometheus.service
systemctl daemon-reload
}




if  [[ -s /etc/systemd/system/prometheus.service ]];then
  sv_p;
elif [[ -s /etc/systemd/system/node_exporter.service  ]];then
  systemctl disable node_exporter
  systemctl stop node_exporter
  node_p;
else
  echo '沒有偵測到node 及 server systemd 檔案，不執行任何移除'
  exit 1
fi
