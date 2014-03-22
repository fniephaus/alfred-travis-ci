import sys
from urllib2 import urlopen, HTTPError
import json
from workflow import Workflow, web

API_BASE_URL = 'https://api.travis-ci.org/'


def main(wf):
    user_input = ''.join(wf.args)
    if "/" in user_input:
        try:
            repo = web.get(API_BASE_URL + 'repos/' + user_input).json()
            status = get_status(repo['last_build_result'])
            title = 'Build #' + \
                str(repo['last_build_number']) + ' (' + status + ')'
            subtitle = 'Duration: ' + str(repo['last_build_duration'])
            wf.add_item(title, subtitle,
                        arg=user_input, autocomplete=user_input, valid=True)
        except HTTPError:
            wf.add_item('Slug invalid.', arg='')
    else:
        try:
            repos = web.get(API_BASE_URL + 'repos/' + user_input).json()
            if len(repos) > 0:
                for repo in repos:
                    wf.add_item(repo['slug'], repo['description'], arg=repo[
                                'slug'], autocomplete=repo['slug'], valid=True)
            else:
                wf.add_item('No repositories found for this user.', arg='')
        except HTTPError:
            wf.add_item('User invalid.', arg='')

    wf.send_feedback()


def get_status(res):
    if res == 0:
        return "Passed"
    return "Failed"


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
