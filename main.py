import requests
import json
import time
from pandas import DataFrame
import matplotlib.pyplot as plt
from dateutil.parser import parse

DEFAULT_URL = "https://api.github.com"
JSON_NAME = "dados_brutos.json"


class PullRequest:
    def __init__(self, id, url, number, state, title, body, created_at, updated_at=None, close_at=None, merged_at=None, **args):
        self.id = id
        self.url = url
        self.number = number
        self.state = state
        self.title = title
        self.body = body
        self.created_at = parse(created_at)
        self.updated_at = updated_at
        self.close_at = close_at
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
            'close_at':self.close_at,
            'merged_at':self.merged_at
        }


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

    def save_pullrequests(self, json_response):
        with open(JSON_NAME, 'w') as file:
            json.dump(json_response, file)

    def get_pullrequests(self):
        have_content = True
        page_number = 1
        pullrequests = []

        while have_content:
            url = DEFAULT_URL + ('/repos/%s/%s/pulls?page=%d&per_page=100' % (self.owner, self.repo, page_number))

            self.get_ratelimit()

            response = requests.get(url)

            if response.status_code == 200:
                json_response = json.loads(response.text)

                if page_number == 1:
                    self.save_pullrequests(json_response)

                #Verifica se json está vazio
                if not json_response:
                    have_content = False
                    continue

                pullrequests.extend([PullRequest(**pullrequest) for pullrequest in json_response])

                page_number += 1

        return pullrequests


if __name__ == '__main__':
    github = GitHub('angular', 'angular')
    pullrequests = github.get_pullrequests()

    df = DataFrame.from_records([s.to_dict() for s in pullrequests])

    plt.hist(df['created_at'], facecolor='green', align='mid')

    plt.xlabel('Tempo')
    plt.ylabel('Quantidade')
    plt.title('PullRequests ao longo do tempo')

    plt.show()