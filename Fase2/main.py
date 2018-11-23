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
    github = gh.GitHub(repo, '02024dd694534f9d77cd73be4be48a0c5828c29c')
    print('{}/{}'.format(repo.owner, repo.name))
    github.make_analisys_api()


if __name__ == '__main__':
    pool = Pool(10)
    results = pool.map(process_repo, top10repos())
