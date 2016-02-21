#!/usr/bin/env python

from __future__ import division
import os
import requests
from bs4 import BeautifulSoup


class BoxOfficeSpider(object):

    def __init__(self, first_movie, second_movie):
        self.nations = {}
        self.first = first_movie
        self.second = second_movie
        self.get_boxoffice(first_movie)
        self.get_boxoffice(second_movie)


    def get_boxoffice(self, name, renew=False):
        if os.path.isfile('../cache/'+name) and not renew:
            handle = open('../cache/'+name).read()
        else:
            handle = requests.get('http://www.boxofficemojo.com/movies/?page=intl&id=%s.htm' % name ).content
            self.backup(name, handle)
        soup = BeautifulSoup(handle, 'html.parser')
        nation_list = soup.find_all('tr', bgcolor='#ffffff')[5:] + soup.find_all('tr', bgcolor='#f4f4ff')
        for i in nation_list:
            infos = i.text.split('\n')   # [nation, distributor, date, opening, percentage, boxoffice, asof]
            # print infos
            if infos[0] in self.nations:
                self.nations[infos[0]].append(int(infos[5][1:].replace(',','')))
            else:
                self.nations[infos[0]] = [int(infos[5][1:].replace(',',''))]


    @staticmethod
    def backup(name, content):
        with open('../cache/'+name, 'w') as f:
            f.write(content)


    def get_nations(self):
        return self.nations


    def get_comparison(self):
        return {nation: movies[0]/movies[1] for nation, movies in self.nations.items() if len(movies) > 1}


if __name__ == '__main__':
    b = BoxOfficeSpider('starwars7', 'fast7')
    print b.get_comparison()

        
