# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
# coding: utf-8
import string
import re
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
from collections import Counter
import utils as ju

df = pd.read_excel('nkjv.xlsx')

#get_ipython().run_line_magic('run', 'nkjvtoflat.ipy')
#get_ipython().run_line_magic('run', 'nkjvtoflat.ipy')

# focus on New Testament
nt = np.where(df['book']=='Matthew')
nt = df[nt[0][0] :]

nt = np.where(df['book']=='John')
nt = df.loc[nt[0]]

nttext = nt['text']
textlist = nttext.to_list()
cleanlist = [i for i in textlist if i if isinstance(i,str)]  # clear Nones
textlong = ' '.join(cleanlist)
regex = re.compile('[0-9]')
cleanlong = regex.sub('', textlong)
regex2 = re.compile('[%s]' % re.escape(string.punctuation))
cleanerlong = regex2.sub('', cleanlong)

def find_term(term, dataframe):
    return [i for i in range(len(dataframe)) if term.lower() in str(dataframe['text'].array[i]).lower()]

def markbook(book, ax=None, color='dodgerblue', ls='--'):
    '''
    make a vertical line where a book
    is on a plot
    '''
    i = np.where(nt['book'] == book)[0][0]
    if ax is None:
        ax = plt.gca()
    ax.axvline(i, color=color, ls=ls, zorder=0)
    return None

def spanbook(book1, book2, ax=None, facecolor='dodgerblue', edgecolor=None, ls='--', **kwargs):
    '''
    make a vertical span between books
    '''
    start = np.where(nt['book'] == book1)[0][0]
    end = np.where(nt['book'] == book2)[0][0]
    if ax is None:
        ax = plt.gca()
    ax.axvspan(start, end, facecolor=facecolor, edgecolor=edgecolor,**kwargs)
    return None

foundterm = find_term(term, nt)

edf = ju.edf(foundterm)[::-1] # just indexing the items

verses = nttext.array[foundterm]

if False:
    # get plotting

    plt.style.use('ggplot')

    fig, ax = plt.subplots(1,1,figsize=(14,6))

    ax.plot(*edf, color='r', lw=1.5,label=term)
    ax.legend()

    ax.plot(*edf, 'r.', ms=10, mec='w', mew=.75)

    ax.set_ylabel('# of times phrase has occured')
    ax.set_xlabel('Location (NKJV, N.T. Only)')

    ax.minorticks_off()

    markbook('Matthew')
    markbook('Mark')
    markbook('Luke')
    markbook('John')
    markbook('Acts', color='k')
    spanbook('1 John', 'Jude', facecolor='.5', alpha=0.5)
    spanbook('Hebrews', 'James', facecolor='.5', alpha=0.5)
    spanbook('Matthew', 'Acts', facecolor='indianred', alpha=0.5)



    ntbooks = np.unique(nt['book'])
    bookstart = [np.where(nt['book'] == bk)[0][0] for bk in ntbooks]
    #for i in enumerate(ntbooks):
    #    print(i)
    ntbooks[[3, 8, 9, 12, 14, 26, 22, 23, 7, 6, 10, 18]] = ''  # declutter

    ax.set_xticks(bookstart)
    ax.set_xticklabels(ntbooks,rotation=90)



    plt.figure()
    biblelist = list(cleanerlong.lower())
    biblelist.sort() # sort the list so it makes since
    letter_counts = Counter(biblelist)
    df2 = pd.DataFrame.from_dict(letter_counts, orient='index')
    df2.plot(kind='bar')
