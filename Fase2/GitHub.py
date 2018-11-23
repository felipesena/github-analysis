from github import Github as g
import requests
import json
import time

DEFAULT_URL = "https://api.github.com"
JSON_FILE = "repo_infos.json"


class Repo:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.quantity_pullrequests = 0
        self.quantity_forks = 0
        self.quantity_stars = 0
        self.quantity_commits = 0

    def to_dict(self):
        return{
            'owner':self.owner,
            'name':self.name,
            'pullrequests':self.quantity_pullrequests,
            'forks':self.quantity_forks,
            'stars':self.quantity_stars,
            'commits':self.quantity_commits
        }


class GitHub:
    def __init__(self, repo, token):
        self.repo = repo
        self.git = g(token)
        self.repository = self.git.get_repo(f'{self.repo.owner}/{self.repo.name}')

    def make_analisys_api(self):
        self.get_infos_api()

        print(self.repo.__dict__)

    def get_infos_api(self):
        print('Starting getting repo informations using API...')
        self.get_stars_api()
        self.get_forks_api()
        self.get_pullrequests_api()
        self.get_commits_api()

    def get_commits_api(self):
        print('Starting getting number of commits using API...')
        commits = self.repository.get_commits()

        page = 1
        number_commits = len(commits.get_page(page))
        self.repo.quantity_commits += number_commits
        page += 1

        while number_commits != 0:
            time.sleep(9)
            number_commits = len(commits.get_page(page))
            self.repo.quantity_commits += number_commits
            page += 1

    def get_pullrequests_api(self):
        print('Starting getting number of pullrequests using API...')
        pulls = self.repository.get_pulls(state='all')

        page = 1
        number_pulls = len(pulls.get_page(page))
        self.repo.quantity_pullrequests += number_pulls
        page += 1

        while number_pulls != 0:
            time.sleep(9)
            page = 1
            number_pulls = len(pulls.get_page(page))
            self.repo.quantity_pullrequests += number_pulls
            page += 1

    def get_forks_api(self):
        print('Starting getting number of forks using API...')
        self.repo.quantity_forks = self.repository.forks_count

    def get_stars_api(self):
        print('Starting getting number of stars using API...')
        self.repo.quantity_stars = self.repository.stargazers_count

    def make_analisys(self):
        self.get_infos()

        file = open(JSON_FILE, 'w')
        json.dump(self.repo, file)
        file.close()

    def get_infos(self):
        print('Starting getting repo informations...')
        self.get_stars()
        self.get_forks()
        self.get_pullrequests()

    def get_stars(self):
        print('Starting getting number of stars...')

        self.verify_ratelimit()

        url = DEFAULT_URL + f'/repos/{self.repo.owner}/{self.repo.name}/stargazers?per_page=100'

        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            json_response = json.loads(response.text)

            if json_response:
                print('+ {} stars - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                self.repo.quantity_forks += len(json_response)

        while 'next' in response.links:
            time.sleep(9)
            response = requests.get(response.links['next']['url'], auth=self.auth)

            if response.status_code == 200:
                print('+ {} stars - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                self.repo.quantity_forks += len(json.loads(response.text))
            elif response.status_code == 403:
                while response.status_code != 200:
                    response = self.deal_abuse(response)

                if response.status_code == 200:
                    print('+ {} stars - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                    self.repo.quantity_forks += len(json.loads(response.text))
                    print('Continuing with the requests...')
            else:
                break

    def get_forks(self):
        print('Starting getting number of forks...')

        self.verify_ratelimit()
        url = DEFAULT_URL + f'/repos/{self.repo.owner}/{self.repo.name}/forks?per_page=100'

        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            json_response = json.loads(response.text)

            if json_response:
                print('+ {} forks - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                self.repo.quantity_forks += len(json_response)

        while 'next' in response.links:
            time.sleep(9)
            response = requests.get(response.links['next']['url'], auth=self.auth)

            if response.status_code == 200:
                print('+ {} forks - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                self.repo.quantity_forks += len(json.loads(response.text))
            elif response.status_code == 403:
                while response.status_code != 200:
                    response = self.deal_abuse(response)

                if response.status_code == 200:
                    print('+ {} forks - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                    self.repo.quantity_forks += len(json.loads(response.text))
                    print('Continuing with the requests...')
            else:
                break

    def deal_abuse(self, response):
        retry_time = int(response.headers['Retry-after'])
        print('Triggered an abuse detection. Retry after {} s'.format(retry_time))
        time.sleep(retry_time)
        response = requests.get(response.url, auth=self.auth)

        return response

    def get_pullrequests(self):
        print('Starting getting number of pullrequests...')

        have_content = True
        page_number = 1
        parameters = {'state': 'all'}

        while have_content:
            self.verify_ratelimit()

            url = DEFAULT_URL + f'/repos/{self.repo.owner}/{self.repo.name}/pulls?page={page_number:d}&per_page=100'

            time.sleep(9)

            response = requests.get(url, auth=self.auth, params=parameters)

            if response.status_code == 200:
                json_response = json.loads(response.text)

                if not json_response:
                    have_content = False
                    continue

                print('+ {} pullrequests - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                self.repo.quantity_pullrequests += len(json_response)

                page_number += 1
            elif response.status_code == 403:
                while response.status_code != 200:
                    response = self.deal_abuse(response)

                if response.status_code == 200:
                    print('+ {} pullrequests - {}/{}'.format(len(json_response), self.repo.owner, self.repo.name))
                    self.repo.quantity_forks += len(json.loads(response.text))
                    page_number += 1
                    print('Continuing with the requests...')

    def verify_ratelimit(self):
        url = DEFAULT_URL + '/rate_limit'
        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            json_response = json.loads(response.text)
            remaining = json_response['resources']['core']['remaining']
            if remaining == 0:
                minutes = 0
                secs = 59
                print('Você chegou ao limite de requisições. Esperando até que possamos continuar o trabalho... \r')

                while minutes != 60:
                    print('Falta {} min e {:2d} sec para continuar as requisições'.format(60 - minutes, secs))

                    time.sleep(1)
                    secs -= 1

                    if secs == 0:
                        secs = 59
                        minutes += 1


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