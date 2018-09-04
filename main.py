import requests
import json
import time

DEFAULT_URL = "https://api.github.com"

class PullRequest:
    def __init__(self, id, url, number, state, title, body, created_at, updated_at=None, close_at=None, merged_at=None, **args):
        self.id = id
        self.url = url
        self.number = number
        self.state = state
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.close_at = close_at
        self.merged_at = merged_at


class GitHub:

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo

    def get_ratelimit(self):
        url = DEFAULT_URL + '/rate_limit'
        response = requests.get(url)

        if response.status_code == 200:
            json_response = json.loads(response.text)
            remaining = json_response['resources']['core']['remaining']
            if remaining == 0:
                mins = 0
                secs = 59
                print('Você chegou ao limite de requisições. Esperando até que possamos continuar o trabalho... \r')

                while mins != 60:
                    print('Falta {} min e {:2d} sec para continuar as requisições'.format(60 - mins, secs))

                    time.sleep(1)
                    secs -= 1

                    if secs == 0:
                        secs = 59
                        mins += 1
            else:
                print('Você ainda tem {} requisições para se fazer'.format(remaining))

    def get_pullrequests(self):
        url = DEFAULT_URL + ('/repos/%s/%s/pulls' % (self.owner, self.repo))

        self.get_ratelimit()

        response = requests.get(url)
        if response.status_code == 200:
            json_response = json.loads(response.text)

            pullrequests = [PullRequest(**pullrequest) for pullrequest in json_response]

            return pullrequests


if __name__ == '__main__':
    github = GitHub('PyGithub', 'PyGithub')
    github.get_pullrequests()
