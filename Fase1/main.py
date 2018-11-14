import requests
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
from requests.auth import HTTPBasicAuth

DEFAULT_URL = "https://api.github.com"
JSON_FILE_DATA = "dados_brutos.json"
JSON_FILE_ALL_PR = "pullrequests.json"


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


class GitHub:

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo

    def get_ratelimit(self):
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

    def save_pullrequests(self, object):
        if type(object) == list and isinstance(object[0], PullRequest):
            with open(JSON_FILE_ALL_PR, 'w') as file:
                json.dump([o.__dict__ for o in object], file)
        else:
            with open(JSON_FILE_DATA, 'w') as file:
                json.dump(object, file)

    def analysis_pullrequests(self):
        pullrequests = self.get_pullrequests()

        df = pd.DataFrame([s.to_dict() for s in pullrequests()])

        #Todos os PullRequests
        df['created_at'] = pd.to_datetime(df['created_at'])

        plt.figure(1)

        df.groupby(pd.Grouper(key='created_at', freq='5M')).count().reset_index().plot(x='created_at', y='body', color='g')

        plt.xlabel('Periódos')
        plt.ylabel('Quantidade')
        plt.title('PullRequests ao longo do Tempo(Angular)')

        #Somente os que tiveram Merge

        df = pd.DataFrame([s.to_dict() for s in pullrequests()])

        with_merged = df[~df.merged_at.isnull()]

        with_merged['merged_at'] = pd.to_datetime(with_merged['merged_at'])
        with_merged.groupby(pd.Grouper(key='merged_at', freq='5M')).count().reset_index().plot(x='merged_at', y='body', color='g')

        plt.xlabel('Periódos')
        plt.ylabel('Quantidade')
        plt.title('PullRequests que tiveram merge')

        plt.figure(2)

        plt.show()

    def get_pullrequests(self):
        have_content = True
        page_number = 1
        pullrequests = []
        parameters = {'state':'all'}

        while have_content:
            url = DEFAULT_URL + ('/repos/%s/%s/pulls?page=%d&per_page=100' % (self.owner, self.repo, page_number))

            self.get_ratelimit()

            response = requests.get(url, auth=HTTPBasicAuth('user','pass'), params=parameters)

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

        self.save_pullrequests(pullrequests)
        return pullrequests


if __name__ == '__main__':
    github = GitHub('angular', 'angular')

    github.analysis_pullrequests()

