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

import os.path as path

from common import AZKABAN_DB_URL, AZKABAN_WEB_URL, AZKABAN_WEB_HOME, AZKABAN_WEB_CONF, AZKABAN_INSTALL_DIR
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class WebServer(Script):
    def install(self, env):
        from params import java_home, azkaban_db
        Execute('{0} | xargs wget -O /tmp/azkaban-web.tgz'.format(AZKABAN_WEB_URL))
        Execute('{0} | xargs wget -O /tmp/azkaban-create-all.sql'.format(AZKABAN_DB_URL))
        Execute(
            'mysql -h{0} -P{1} -D{2} -u{3} -p{4} < /tmp/azkaban-create-all.sql'.format(
                azkaban_db['mysql.host'],
                azkaban_db['mysql.port'],
                azkaban_db['mysql.database'],
                azkaban_db['mysql.user'],
                azkaban_db['mysql.password']
            )
        )
        
        Execute(
            'export JAVA_HOME={0} && tar -zxvf /tmp/azkaban-web.tgz -C {1}'.format(
                java_home,
                AZKABAN_INSTALL_DIR
            )
        )
        Execute('rm -f /tmp/azkaban-web.tgz')
        Execute('mv /usr/local/azkaban-web-server-0.1.0-SNAPSHOT {0}'.format(AZKABAN_WEB_HOME))
        self.configure(env)

    def stop(self, env):
        from params import java_home
        Execute('cd {0} && export PATH=$PATH:{1}/bin && bin/shutdown-web.sh'.format(AZKABAN_WEB_HOME, java_home))

    def start(self, env):
        from params import java_home
        self.configure(env)
        Execute('cd {0} && export PATH=$PATH:{1}/bin && bin/start-web.sh'.format(AZKABAN_WEB_HOME, java_home))

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-web-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_db, azkaban_mail, azkaban_web_properties, azkaban_users, global_properties, log4j_properties
        key_val_template = '{0}={1}\n'

        with open(path.join(AZKABAN_WEB_CONF, 'azkaban.properties'), 'w') as f:
            for key, value in azkaban_db.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_mail.iteritems():
                f.write(key_val_template.format(key, value))    
            for key, value in azkaban_web_properties.iteritems():
                if key != 'content':
                    f.write(key_val_template.format(key, value))
            f.write(azkaban_web_properties['content'])

        with open(path.join(AZKABAN_WEB_CONF, 'azkaban-users.xml'), 'w') as f:
            f.write(str(azkaban_users['content']))

        with open(path.join(AZKABAN_WEB_CONF, 'global.properties'), 'w') as f:
            f.write(global_properties['content'])

        with open(path.join(AZKABAN_WEB_CONF, 'log4j.properties'), 'w') as f:
            f.write(log4j_properties['content'])


if __name__ == '__main__':
    WebServer().execute()
