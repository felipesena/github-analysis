from Fase2 import GitHub as gh
from multiprocessing.dummy import Pool


class Repo:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name


def top10Repos():
    repos = []

    repos.append(Repo('Microsoft', 'vscode'))
    repos.append(Repo('facebook', 'react-native'))
    repos.append(Repo('tensorflow', 'tensorflow'))
    repos.append(Repo('angular', 'angular-cli'))
    repos.append(Repo('MicrosoftDocs', 'azure-docs'))
    repos.append(Repo('angular', 'angular'))
    repos.append(Repo('ansible', 'ansible'))
    repos.append(Repo('kubernates', 'kubernates'))
    repos.append(Repo('npm', 'npm'))
    repos.append(Repo('DefinitelyTyped', 'DefinitelyTyped'))

    return repos


def processRepo(repo):
    github = gh.GitHub(repo)
    print('{}/{}'.format(repo.owner, repo.name))


if __name__ == '__main__':
    pool = Pool(10)
    results = pool.map(processRepo, top10Repos())
