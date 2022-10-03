import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
from collections import Counter
import re
import string

def xml_to_pandas(version):
    etree = ET.parse(f'bible-translations/{version}.xml')
    dfcols = ['book', 'chapter', 'verse', 'text']
    df = pd.DataFrame(columns=dfcols)
    for item in tqdm(etree.iter()):
        if item.tag == 'book':
            book = item.attrib['name']
        elif item.tag == 'chapter':
            chapter = item.attrib['name']
        elif item.tag == 'verse':
            verse = item.attrib['name']
            text = item.text
            data = [book, chapter, verse, text]
            df = df.append(pd.Series(data, index=dfcols), ignore_index=True)
        else:
            pass
    return df


# clean text of punctuation and numbers
def clean_text(text):
    regex = re.compile('[0-9]') # remove numbers
    clean = regex.sub('', text)
    regex2 = re.compile('[%s]' % re.escape(string.punctuation)) # remove punctuation
    cleaner = regex2.sub('', clean)
    return cleaner