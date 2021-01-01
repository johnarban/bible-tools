import numpy as np
import pandas as pd
def pick_random(df, norm_book=True, norm_chap=True):

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
        i = np.random.randint(0, high=len(df))
        bv = df.iloc[i]
        book = bv['book']
        chapter = bv['chapter']
        verse = bv['verse']
        text = bv['text']




    print(f'{book} {chapter}:{verse} (NKJV)\n{text}')

    return None