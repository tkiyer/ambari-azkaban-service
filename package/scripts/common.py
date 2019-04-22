# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from resource_management.libraries.script.script import Script

config = Script.get_config()
## Add stack version for HDP 3.0
# stack_version_unformatted = config['clusterLevelParams']['stack_version']
# Azkaban download url, changed the url by added '/' before azkaban/azkaban-${verion}.tar.gz
# download_url = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/azkaban/azkaban-web-server-0.1.0-SNAPSHOT.tar.gz"}\''

AZKABAN_HOME = '/usr/local/azkaban'
AZKABAN_NAME = 'azkaban'
AZKABAN_SQL = 'azkaban.sql'
AZKABAN_WEB_URL = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/azkaban/azkaban-web-server-0.1.0-SNAPSHOT.tar.gz"}\''
AZKABAN_EXECUTOR_URL = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT.tar.gz"}\''
AZKABAN_DB_URL = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/azkaban/create-all-sql-0.1.0-SNAPSHOT.sql"}\''
AZKABAN_EXEC_AS_USER_C_URL = 'cat /etc/yum.repos.d/ambari.repo | grep "baseurl" | awk -F \'=\' \'{print $2"/azkaban/execute-as-user.c"}\''
AZKABAN_CONF = AZKABAN_HOME + '/conf'
