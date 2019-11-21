import json
import requests.exceptions


class Parser:
    def __init__(self):
        pass

    def jopen(self, filename):
        return json.load(open(filename))

    def extractAllRepos(self, owner):
        x = self.jopen('Repositories-google.json')
        print(len(x))


if __name__ == "__main__":
    X = Parser()
    X.extractAllRepos('s')
