from contextlib import contextmanager

from fabric.api import settings
from fabric.context_managers import cd, prefix
from fabric.operations import run
from fabric.state import env

import fabfile_config as config


env.hosts = config.ROLEDEFS['prod']
env.passwords = config.PASSWORDS
env.directory = '/home/django/{}'.format(config.REPOSITORY_NAME)
env.activate = 'source /home/django/{}/.venv/bin/activate'.format(config.REPOSITORY_NAME)


@contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def dev():
    env.hosts = config.ROLEDEFS['dev']


def deploy():
    pull()
    install_requirements()
    migrate()
    task_init()
    restart()


def restart():
    with virtualenv():
        run("systemctl restart {}".format(config.PROJECT_NAME))
        run("systemctl restart nginx")


def task_init():
    with virtualenv():
        run("chmod -R 777 ./")
        run("./manage.py collectstatic --noinput")


def migrate():
    with virtualenv():
        run("./manage.py migrate")


def install_requirements():
    with virtualenv():
        run("pip install --upgrade -r requirements.txt")


def pull():
    with virtualenv():
        prompts = {
            "Username for 'https://gitlab.com': ": config.GIT_USERNAME,
            "Password for 'https://{}@gitlab.com': ".format(config.GIT_USERNAME): config.GIT_PASSWORD,
        }
        with settings(prompts=prompts):
            run('git reset --hard origin/master')
            run('git pull origin master')


def manage(param):
    with virtualenv():
        run("./manage.py {}".format(param))
