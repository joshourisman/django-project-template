from invoke import task

from .base import DJANGO_ROOT, DEFAULT_ENV


@task(name="manage")
def management_command(c, cmd, env={}):
    """Run a Django command locally."""

    new_env = DEFAULT_ENV.copy()
    new_env.update(env)

    with c.cd(DJANGO_ROOT):
        c.run(f"./manage.py {cmd}", env=new_env, pty=True)


@task(name="shell")
def django_shell(c):
    """Open a local Django shell."""
    management_command(c, "shell_plus")


@task(name="run")
def run_server(c):
    env = DEFAULT_ENV.copy()
    env.update({"DJANGO_DEBUG": "True"})

    with c.cd(DJANGO_ROOT):
        c.run("uvicorn pingpong_bot.asgi:application --reload", env=env, pty=True)


@task(name="test")
def run_tests(c, github=False):
    """Run Django test suite."""

    env = {}
    if github is True:
        env["DATABASE_URL"] = "postgres://postgres:postgres@localhost/postgres"

    management_command(c, "test", env=env)
