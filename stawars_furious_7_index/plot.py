#!/usr/bin/env python

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from spider import BoxOfficeSpider
from math import sqrt
from sys import argv


def compute_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def box_office_plot(name1, name2, first, second):
    hdis = {}
    with open('hdi.txt') as f:
        for line in f:
            num = line[-6:-1]
            nation = line[:-6].strip()
            hdis[nation] = float(num)
    # print hdis
    propotions = BoxOfficeSpider(first, second).get_comparison()
    print propotions
    # open('swf7i', 'w').writelines(str(a)+' '+str(b)+'\n' for a, b in sorted(propotions.items(), key=lambda x:float(x[1])))

    points_to_show = set([(0,0)])
    points = set([(0,0)])
    for n in propotions.keys():
        points.add((hdis[n], propotions[n]))
        plt.plot(hdis[n], propotions[n], 'go')
        if min(map(compute_distance, points_to_show, 
            [(hdis[n], propotions[n])]*len(points_to_show))) > 0.05:
            plt.annotate(n, xy=(hdis[n], propotions[n]), xytext = (-5, -5), 
                textcoords = 'offset points', ha = 'right', va = 'bottom')
            points_to_show.add((hdis[n], propotions[n]))

    points.remove((0,0))
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    plt.plot(x, fit_fn(x), '--k')

    yhat = fit_fn(x)                         # or [p(z) for z in x]
    ybar = sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = sum((yihat-ybar)**2 for yihat in yhat)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = sum((yi - ybar)**2 for yi in y)    # or sum([ (yi - ybar)**2 for yi in y])
    r_squared = ssreg / sstot
    # plt.annotate(fit, )
    # plt.xlim(0, 5)
    print yhat, ybar, ssreg, sstot, r_squared
    plt.ylim(0)

    plt.title('The Relationship between \nthe Box Office Ratio of %s to %s \nand the Country\'s Development Degree' % (name1, name2))
    plt.xlabel('Human Development Index (HDI)\nR = %3f' % sqrt(r_squared))
    plt.ylabel('Box office of %s / Box office of %s' % (name1, name2))

    plt.show()
    

def main():
    first_movie_name = raw_input('First Movie: ')
    first_movie_id = raw_input('Mojo ID: ')
    second_movie_name = raw_input('Second Movie: ')
    second_movie_id = raw_input('Mojo ID: ')
    box_office_plot(first_movie_name, second_movie_name, 
        first_movie_id, second_movie_id)




if __name__ == '__main__':
    if argv[1] == '--default':
        box_office_plot('Star Wars: The Force Awakens', 'Furious 7', 'starwars7', 'fast7')
    elif argv[1] == '-n' and len(argv) == 6:
        box_office_plot(argv[2], argv[4], argv[3], argv[5])
    elif len(argv) == 1:
        main()
    else:
        print 'Usage: python plot.py [-n name1 id1 name2 id2 | --default]'
