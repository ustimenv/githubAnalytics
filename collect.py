import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
from os.path import exists
from sys import stderr
from time import sleep, time

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='username', type=str)
    parser.add_argument('--password', dest='password', type=str)
    args = parser.parse_args()
    return args


class DataCollector:
    def __init__(self, username=None, password=None):
        self.authentificated = username is not None and password is not None
        self.authentification = HTTPBasicAuth(username=username, password=password)

    def _collect(self, url, filename, mode='w'):
        if self.authentificated:
            result = requests.get(url=url, auth=self.authentification)
        else:
            result = requests.get(url=url)
            # print('Persistent collection requires authentication', file=stderr)
            # raise RuntimeError()

        data = result.json(); code = result.status_code
        if code == 403:
            print('Quota exceeded, executing persistence procedure')
            self._wait()

        if mode is not None:
            with open('jsons/'+filename + '.json', mode, encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            pass
            print(data)
        return data

    def collectUserToplevel(self, user):
        url = 'https://api.github.com/users/' + user
        return self._collect(url, 'User-'+user)

    def collectRepository(self, repoName, owner):
        url = 'https://api.github.com/repos/'+owner+'/'+repoName+'/commits'
        return self._collect(url, 'Repo-' + owner + '-' + repoName)

    def collectReposToplevel(self, owner):
        url = 'https://api.github.com/users/'+owner+'/repos'
        return self._collect(url, 'Repositories-'+owner)

    def collectAllRepos(self, owner):
        data = self.collectUserToplevel(owner)
        # numRepos = self.read('User-'+owner+'.json')["public_repos"]
        numRepos = data["public_repos"]
        pageIndex = numRepos // 100 + 1
        self._createFile('All_Repositories-' + owner)

        for i in range(pageIndex):
            print(i+1, ' out of ', pageIndex)
            url = 'https://api.github.com/users/'+owner+'/repos?page='+str(i)+'&per_page=100'
            self._collect(url=url, filename='All_Repositories-'+owner, mode='a')

    def readJson(self, filename):
        return json.load(open(filename))

    def _createFile(self, filename):
        open('jsons/'+filename + '.json', 'w', encoding='utf-8')

    def getCurrentLimit(self):
        url = 'https://api.github.com/rate_limit'
        if self.authentificated:
            result = requests.get(url=url, auth=self.authentification)
        else:
            result = requests.get(url=url)
        data = result.json()
        remaining = data['resources']['core']['remaining']
        limit = data['resources']['core']['limit']
        return remaining, limit

    def _wait(self):
        while True:
            remaining, limit = self.getCurrentLimit()
            if remaining < 1:
                print('.', end='', sep='')
            else:
                return
            sleep(60)


if __name__ == "__main__":
    args = parseArgs()
    username = args.username
    password = args.password
    Collector = DataCollector(username, password)


    # Collector.getLimit()
    # Collector.collectAllRepos('microsoft')


