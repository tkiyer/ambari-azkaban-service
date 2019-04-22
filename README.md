# Intro
Ambari 集成 Azkaban

# Major Project Structure
- configuration : azkaban 配置文件
- package : 
  - scripts :  ambari 管理逻辑脚本
    - azkaban_executor.py  
    - azkaban_web.py
    - common.py
    - download.ini
    - params.py

## Setup

#### Deploy Hue on existing cluster
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
rm -rf /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/AZKABAN  
sudo git clone https://github.com/tkiyer/ambari-azkaban-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/AZKABAN
```

- Restart Ambari

```
service ambari-server restart
```

# Usage
https://cwiki.apache.org/confluence/display/AMBARI/Overview
