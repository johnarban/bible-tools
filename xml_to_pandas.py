import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
from collections import Counter

etree = ET.parse('bible-translations/msg.xml')

dfcols = ['book','chapter','verse','text']
df = pd.DataFrame(columns = dfcols)

for item in tqdm(etree.iter()):
    if item.tag == 'book':
        book = item.attrib['name']
    elif item.tag == 'chapter':
        chapter = item.attrib['name']
    elif item.tag == 'verse':
        verse = item.attrib['name']
        text = item.text
        data = [book,chapter,verse,text]
        df = df.append(pd.Series(data,index=dfcols),ignore_index=True)
    else:
        pass

df.to_excel('msg.json')
books = df['book']
# bookcount = pd.DataFrame.from_dict(Counter(books),orient='index')
#bookcount.plot(kind='bar',yscale='log')