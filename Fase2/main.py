from Fase2 import GitHub as gh
from multiprocessing.dummy import Pool


def top10Repos():
    repos = []

    repos.append(gh.Repo('Microsoft', 'vscode'))
    repos.append(gh.Repo('facebook', 'react-native'))
    repos.append(gh.Repo('tensorflow', 'tensorflow'))
    repos.append(gh.Repo('angular', 'angular-cli'))
    repos.append(gh.Repo('MicrosoftDocs', 'azure-docs'))
    repos.append(gh.Repo('angular', 'angular'))
    repos.append(gh.Repo('ansible', 'ansible'))
    repos.append(gh.Repo('kubernates', 'kubernates'))
    repos.append(gh.Repo('npm', 'npm'))
    repos.append(gh.Repo('DefinitelyTyped', 'DefinitelyTyped'))

    return repos


def processRepo(repo):
    github = gh.GitHub(repo)
    print('{}/{}'.format(repo.owner, repo.name))


if __name__ == '__main__':
    pool = Pool(10)
    results = pool.map(processRepo, top10Repos())
