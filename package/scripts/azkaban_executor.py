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

from common import AZKABAN_EXECUTOR_URL, AZKABAN_EXEC_HOME, AZKABAN_INSTALL_DIR, AZKABAN_EXEC_CONF, AZKABAN_EXEC_AS_USER_C_URL
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class ExecutorServer(Script):
    def install(self, env):
        from params import java_home
        Execute('{0} | xargs wget -O /tmp/azkaban-exec.tgz'.format(AZKABAN_EXECUTOR_URL))
        Execute('{0} | xargs wget -O /tmp/execute-as-user.c'.format(AZKABAN_EXEC_AS_USER_C_URL))
        Execute(
            'export JAVA_HOME={0} && tar -zxvf /tmp/azkaban-exec.tgz -C {1}'.format(
                java_home,
                AZKABAN_INSTALL_DIR
            )
        )
        Execute('rm -f /tmp/azkaban-exec.tgz')
        Execute('mv /usr/local/azkaban-exec-server-0.1.0-SNAPSHOT {0}'.format(AZKABAN_EXEC_HOME))
        Execute('mkdir {0}'.format(AZKABAN_EXEC_HOME + '/native-lib'))
        Execute('gcc /tmp/execute-as-user.c -o /tmp/execute-as-user')
        Execute('cp /tmp/execute-as-user {0}'.format(AZKABAN_EXEC_HOME + '/native-lib'))
        Execute('chown root {0}'.format(AZKABAN_EXEC_HOME + '/native-lib/execute-as-user'))
        Execute('chown 6050 {0}'.format(AZKABAN_EXEC_HOME + '/native-lib/execute-as-user'))
        Execute('echo execute.as.user=true > {0} '.format(AZKABAN_EXEC_HOME + '/plugins/jobtypes/commonprivate.properties'))
        Execute('echo azkaban.native.lib={0} > {1} '.format(AZKABAN_EXEC_HOME + '/native-lib', AZKABAN_EXEC_HOME + '/plugins/jobtypes/commonprivate.properties'))
        Execute('echo azkaban.group.name=hadoop > {0} '.format(AZKABAN_EXEC_HOME + '/plugins/jobtypes/commonprivate.properties'))
        self.configure(env)

    def stop(self, env):
        Execute('cd {0} && export JAVA_HOME={1} && bin/shutdown-exec.sh'.format(AZKABAN_EXEC_HOME, java_home))

    def start(self, env):
        from params import azkaban_executor_properties
        self.configure(env)
        Execute('cd {0} && export JAVA_HOME={1} && bin/start-exec.sh'.format(AZKABAN_EXEC_HOME, java_home))
        # check process status
        status(self, env)

        Execute(
            'curl http://localhost:{0}/executor?action=activate'.format(azkaban_executor_properties['executor.port'])
        )

    def status(self, env):
        try:
            Execute(
                'export AZ_CNT=`ps -ef |grep -v grep |grep azkaban-exec-server | wc -l` && `if [ $AZ_CNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import azkaban_executor_properties, log4j_properties, azkaban_db, azkaban_mail
        key_val_template = '{0}={1}\n'

        with open(path.join(AZKABAN_EXEC_CONF, 'azkaban.properties'), 'w') as f:
            for key, value in azkaban_db.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_mail.iteritems():
                f.write(key_val_template.format(key, value))
            for key, value in azkaban_executor_properties.iteritems():
                if key != 'content':
                    f.write(key_val_template.format(key, value))
            f.write(azkaban_executor_properties['content'])

        with open(path.join(AZKABAN_EXEC_CONF, 'log4j.properties'), 'w') as f:
            f.write(log4j_properties['content'])


if __name__ == '__main__':
    ExecutorServer().execute()
