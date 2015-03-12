import json
import os
import re
import sys

from collections import OrderedDict
from distutils.util import strtobool
from fabric.api import local
from fabric.context_managers import hide, settings
from fabric.utils import puts
from fabric.colors import yellow, green, red

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def read_version(filename="VERSION"):
    path = os.path.join(PROJECT_ROOT, filename)

    f = open(path, 'r')
    current_version = f.read()
    f.close()

    return current_version


def increment_version(current_version=None, part="+patch"):
    def format_version(groups):
        return "{0}.{1}.{2}".format(*[g[1] for g in groups.items()])

    if current_version is None:
        current_version = read_version()

    regex = re.compile(r'(\d+)\.(\d+)\.(\d+)')
    match = regex.match(current_version)

    groups = OrderedDict([
        ('major', int(match.groups()[0])),
        ('minor', int(match.groups()[1])),
        ('patch', int(match.groups()[2])),
    ])

    inc_dec = part[0]
    part_type = part[1:]

    if inc_dec is "+":
        if part_type == 'major':
            groups['major'] += 1
            groups['minor'] = 0
            groups['patch'] = 0
        elif part_type == 'minor':
            groups['minor'] += 1
            groups['patch'] = 0
        elif part_type == 'patch':
            groups['patch'] += 1
    else:
        if groups[part_type] > 0:
            groups[part_type] -= 1

    new_version = format_version(groups)

    return new_version


def version(part="+patch", suppress=False, new_version=None):
    if new_version is None:
        if not suppress and part == "+patch":
            puts(red("WARNING: ") +
                 "version now defaults to +patch by default.")

        current_version = read_version()
        new_version = increment_version(current_version, part=part)

    try:
        package = json.load(open('package.json', 'r'))
    except IOError:
        pass
    else:
        package['version'] = new_version
        json.dump(package, open('package.json', 'w'), indent=2)

    path = os.path.join(PROJECT_ROOT, 'VERSION')

    f = open(path, 'w')
    f.write(new_version)
    f.close()

    puts(yellow("Version is now: ") + green(new_version))

    if not suppress:
        puts(yellow("Don't forget to commit, tag and run `git push --tags`") +
             " " + red("NOTE: tagging is no longer automatic"))


def get_local_database():
    database_url = os.environ.get(
        'DATABASE_URL', 'postgres://localhost/mindmapr')

    assert database_url.startswith('postgres://')
    return database_url.lstrip('postgres://').split('/')


def download_heroku_db(app='mindmapr'):
    local('wget `heroku pgbackups:url -a {}` -O heroku.dump'.format(app))

    local_db_host, local_db_name = get_local_database()
    try:
        local('dropdb %s' % local_db_name)
    except:
        # If we can't drop the database, that's probably just fine,
        # it may just mean that you don't have it.
        pass
    local('createdb %s -E utf8 -T template0' % local_db_name)
    try:
        local('pg_restore -h %s -d %s -v --no-owner --no-acl heroku.dump' %
              (local_db_host, local_db_name))
    except:
        pass


GIT_NOT_CLEAN = "Git tree is not clean."


def get_git_state():
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        ret_val = local("git status --porcelain | grep -v ??", capture=True)
        if ret_val.strip():
            return GIT_NOT_CLEAN


def release(gulp=True, part="+patch"):
    def ok():
        puts(green("    [OK]"))
    if isinstance(gulp, basestring):
        gulp = strtobool(gulp)

    report = get_git_state()
    if report:
        puts(red(report + " Aborting."))
        sys.exit()

    if gulp:
        puts(yellow("Running `gulp build`... "))
        with hide('stdout', 'running'):
            local("cd frontend && gulp build")
        ok()

    report = get_git_state()
    if report == GIT_NOT_CLEAN:
        puts(yellow("Gulp has updates. Adding static/ and committing."))
        with hide('running'):
            local("git add frontend/static/")
            local("git commit -m 'Automated gulp build for release.'")
    else:
        puts(yellow("Gulp build resulted in no changes."))
    ok()

    new_version = increment_version(part=part)

    puts(yellow("Initiating release... "))
    local("git flow release start '{version}'".format(version=new_version))
    ok()

    version(suppress=True, new_version=new_version)

    puts(yellow("Incrementing version... "))
    with hide('running'):
        local("git add VERSION")
        local("git add frontend/package.json")
        local("git commit -m 'Incrementing version to {version}.'".format(
            version=new_version))
    ok()

    puts(yellow("Finishing release. I'm going to need your help here..."))
    local("git flow release finish -m '{version}' '{version}'".format(
        version=new_version))
    ok()


def deploy():
    puts(yellow("Deploying to Heroku..."))
    local("git push --all && git push heroku master:master")
    puts(green("    [OK]"))
