import numpy as np
import pandas as pd
from scipy.stats import truncnorm
def pick_random(df, norm_book=True, norm_chap=True, uniform=True, verb=True, seed=False ):

    if seed:
        np.random.seed(1)

    if norm_book:
        book = np.random.choice(df.book.unique())
        df_book = df.set_index('book').loc[book]
        if norm_chap:
            chapter = np.random.choice(df_book.chapter.unique())
            df_chapter = df_book.set_index('chapter').loc[chapter]
        else:
            chapter = np.random.choice(df_book.chapter)
            df_chapter = df_book.set_index('chapter').loc[chapter]
        verse = np.random.choice(df_chapter.verse)
        text = df_chapter.set_index('verse').loc[verse]['text']
    else:
        if uniform:
            i = np.random.randint(0, high=len(df))
        else:
            loc, scale = 0.5, 0.5/2
            clip_a, clip_b = 0, 1
            a = (clip_a-loc)/scale
            b = (clip_b-loc)/scale
            i = int(df.shape[0] * truncnorm(a,b,loc,scale).rvs())
        bv = df.iloc[i]
        book = bv['book']
        chapter = bv['chapter']
        verse = bv['verse']
        text = bv['text']



    if verb:
        print(f'{book} {chapter}:{verse} (NKJV)\n{text}')

    return book