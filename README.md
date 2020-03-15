#部屬之前請依照順序安裝

1.安裝相依套件(包含python3 pip3 修改selinux )
sh pre_install.sh

2.再來請查看是要部屬server or exporter

server 
python3 promethous_server.py

exporter
python3 promethous_exporter.py



移除方式
1.此支腳本做的事情就是偵測您的systemctld內有什麼，假設是server就把對應移除，假設是exporter，就把相對應的移除
sh prome_reset.sh

