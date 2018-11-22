from Fase2 import GitHub as gh
from multiprocessing.dummy import Pool


def top10repos():
    repos = []

    repos.append(gh.Repo('Microsoft', 'vscode'))
    repos.append(gh.Repo('facebook', 'react-native'))
    repos.append(gh.Repo('tensorflow', 'tensorflow'))
    repos.append(gh.Repo('angular', 'angular-cli'))
    repos.append(gh.Repo('MicrosoftDocs', 'azure-docs'))
    repos.append(gh.Repo('angular', 'angular'))
    repos.append(gh.Repo('ansible', 'ansible'))
    repos.append(gh.Repo('kubernetes', 'kubernetes'))
    repos.append(gh.Repo('npm', 'npm'))
    repos.append(gh.Repo('DefinitelyTyped', 'DefinitelyTyped'))

    return repos


def process_repo(repo):
    github = gh.GitHub(repo, '25d9bcaf7160e2f2eec7969d7b893b5729701e63')
    print('{}/{}'.format(repo.owner, repo.name))
    github.make_analisys_api()


if __name__ == '__main__':
    pool = Pool(10)
    results = pool.map(process_repo, top10repos())
