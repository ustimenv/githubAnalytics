import requests
from requests.auth import HTTPBasicAuth
import json
import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='username', type=str)
    parser.add_argument('--password', dest='password', type=str)
    args = parser.parse_args()
    return args


class DataCollector:
    def __init__(self, username='', password=''):
        self.authentification = HTTPBasicAuth(username=username, password=password)

    def _collect(self, url, filename, write=True):
        result = requests.get(url=url, auth=self.authentification)
        data = result.json()
        if write:
            with open(filename+'.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            print(data)
        return data, result.status_code


    def collectUserToplevel(self, user):
        url = 'https://api.github.com/users/' + user + '/'
        return self._collect(url, 'User-'+user)

    def collectRepository(self, repoName, owner):
        url = 'https://api.github.com/repos/'+owner+'/'+repoName+'/commits'
        return self._collect(url, 'Repo-' + owner + '-' + repoName)

    def collectReposToplevel(self, owner):
        url = 'https://api.github.com/users/'+owner+'/repos/'
        return self._collect(url, 'Repositories-'+owner)


if __name__ == "__main__":
    args = parseArgs()
    username = args.username
    password = args.password
    Collector = DataCollector(username, password)
    Collector.collectReposToplevel('google')
    # Collector.collectReposToplevel('ustimenv')

