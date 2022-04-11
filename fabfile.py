from contextlib import contextmanager

from fabric import Connection, Config
from fabric.tasks import task

from fabfile_config import config


class Fabric:

    def __init__(self, env, fast=False):
        self.config = config[env]
        self.gunicorn_service = self.config.get('gunicorn_service', 'gunicorn.socket')
        connection_config = self.config['connection'].get('config')
        if connection_config:
            self.config['connection']['config'] = Config(overrides=self.config['connection']['config'])
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
        self.connection.sudo(f'systemctl restart {service}')

    def restart_gunicorn(self):
        print('Restarting gunicorn: ')
        self.restart_service(self.gunicorn_service)

    def deploy(self):
        self.pull()
        if not self.fast:
            self.install_requirements()
            self.manage('migrate')
            self.manage('collectstatic --noinput')
        self.restart_gunicorn()


@task(help={
    'env': '배포환경 (예. dev, staging, prod)',
    'fast': '빠른 배포 진행 여부'
})
def deploy(c, env='prod', fast=False):
    """
    서버 배포
    """
    fabric = Fabric(env, fast=fast)
    fabric.deploy()


@task(help={
    'management_command': 'manage.py "management_command"',
    'env': '배포환경 (예. dev, staging, prod)'
})
def manage(c, management_command, env='prod'):
    """
    django management command 실행
    """
    fabric = Fabric(env)
    fabric.manage(management_command)
