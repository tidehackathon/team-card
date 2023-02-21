import pandas as pd
import re
import string

#Remove links
def remove_links(text_string):
    pattern = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.(com|net|lt|eu)+((\/|\&|\=|\.|\?|-){1}\w+)*", '', text_string)
    return pattern

#Remove html tags
def remove_html_tags(text_string):
    text_string = text_string.apply(lambda x : re.sub('(<.*?>).*?(<.*?>)', '', x))
    return text_string

#Remove punctuation
def remove_punct(text_string):
    text_string = text_string.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    text_string = text_string.replace('„', ' ')
    text_string = text_string.replace('“', ' ')
    text_string = text_string.replace('”', ' ')
    text_string = text_string.replace('’', ' ')
    text_string = text_string.replace('‘', ' ')
    text_string = text_string.replace('…', ' ')
    text_string = text_string.replace('–', ' ')
    text_string = text_string.replace('—', ' ')
    text_string = text_string.replace('   ', ' ')
    text_string = text_string.replace('  ', ' ')
    text_string = re.sub(r'(\w+)(\d{4})', r'\1 \2', text_string)
    return text_string

def remove_double_spaces(df, column_name):
    text = pd.DataFrame(columns=[column_name])
    for i in range(len(df)):
        s = " ".join(df[column_name][i].split())
        text.loc[i] = [s]
    return text
    