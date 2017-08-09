import datetime
import sys
import humanize
from workflow import Workflow, web

API_BASE_URL = 'https://api.travis-ci.org'
# GitHub repo for self-updating
GITHUB_UPDATE_CONF = {'github_slug': 'fniephaus/alfred-travis-ci'}
# GitHub Issues
HELP_URL = 'https://github.com/fniephaus/alfred-travis-ci/issues'


def display_repo(user_input):
    req = web.get('%s/repos/%s' % (API_BASE_URL, user_input))
    try:
        repo = req.json()
    except:
        parts = user_input.split('/')
        return display_repos(parts[0], parts[1])
    status = get_status(repo['last_build_result'])
    title = 'Build #%s (%s)' % (repo['last_build_number'], status)
    subtitle = None
    if repo['last_build_duration']:
        timedelta = datetime.timedelta(seconds=repo['last_build_duration'])
        subtitle = 'Duration: %s' % humanize.naturaldelta(timedelta)
    wf.add_item(title, subtitle,
                arg=user_input, autocomplete=user_input, valid=True)


def display_repos(user_input, repo_prefix=None):
    req = web.get('%s/repos/%s' % (API_BASE_URL, user_input))
    if req.status_code != 200:
        return wf.add_item('User invalid.', arg='')
    repos = req.json()
    if len(repos) > 0:
        for repo in repos:
            if repo_prefix:
                repo_name = repo['slug'].split('/')[1]
                if not repo_name.startswith(repo_prefix):
                    continue
            wf.add_item(repo['slug'], repo['description'], arg=repo[
                        'slug'], autocomplete=repo['slug'], valid=True)
    else:
        wf.add_item('No repositories found for this user.', arg='')


def main(wf):
    user_input = ''.join(wf.args)
    if not user_input:
        wf.add_item('Enter a username or a repo slug.', arg='')
    elif '/' in user_input:
        display_repo(user_input)
    else:
        display_repos(user_input)

    wf.send_feedback()


def get_status(res):
    return 'Passed' if res == 0 else 'Failed'


if __name__ == '__main__':
    wf = Workflow(update_settings=GITHUB_UPDATE_CONF, help_url=HELP_URL)
    sys.exit(wf.run(main))
