import requests
import json
import time
from requests.auth import HTTPBasicAuth

DEFAULT_URL = "https://api.github.com"

class GitHub:
    def __init__(self, repo):
        self.repo = repo

    def verify_ratelimit(self):
        url = DEFAULT_URL + '/rate_limit'
        response = requests.get(url, auth=HTTPBasicAuth('user','pass'))

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

class PullRequest:
    def __init__(self, id, url, number, state, title, body, created_at, updated_at=None, closed_at=None, merged_at=None, **args):
        self.id = id
        self.url = url
        self.number = number
        self.state = state
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        self.merged_at = merged_at

    def to_dict(self):
        return{
            'id':self.id,
            'url':self.url,
            'number':self.number,
            'state':self.state,
            'title':self.title,
            'body':self.body,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'close_at':self.closed_at,
            'merged_at':self.merged_at
        }