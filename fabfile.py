from contextlib import contextmanager

from fabric import Connection
from fabric.tasks import task

from fabfile_config import config


class Fabric:

    def __init__(self, env, fast=False):
        self.config = config[env]
        self.connection = Connection(**self.config['connection'])
        self.fast = fast

    @contextmanager
    def virtualenv(self):
        with self.connection.cd(self.config['path_project']):
            with self.connection.prefix(f'source {self.config["path_project"]}/.venv/bin/activate'):
                yield

    def pull(self):
        with self.virtualenv():
            self.connection.run('git reset --hard origin/master')
            self.connection.run('git pull origin master')

    def install_requirements(self):
        with self.virtualenv():
            self.connection.run('pip install --upgrade -r requirements.txt')

    def manage(self, param):
        with self.virtualenv():
            self.connection.run(f'./manage.py {param}')

    def restart_service(self, service):
        self.connection.run(f'systemctl restart {service}')

    def restart_gunicorn(self):
        print('Restarting gunicorn: ')
        if self.fast:
            # https://stackoverflow.com/a/47115688
            r = r's/.*Main PID: \(.*\)$/\1/g p'
            self.connection.run(f"systemctl status gunicorn |  sed -n '{r}' | cut -f1 -d' ' | xargs kill -HUP")
        else:
            self.restart_service('gunicorn.socket')

    def deploy(self):
        self.pull()
        if not self.fast:
            self.install_requirements()
            self.manage('migrate')
            self.manage('collectstatic --noinput')
            self.restart_service('nginx')
        self.restart_gunicorn()


@task(help={
    'env': '배포환경 (예. dev, staging, prod)',
    'fast': '빠른 배포 진행 여부'
})
def deploy(c, env='staging', fast=False):
    """
    서버 배포
    """
    fabric = Fabric(env, fast=fast)
    fabric.deploy()
