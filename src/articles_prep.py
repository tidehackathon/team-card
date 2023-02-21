import pandas as pd
from preprocessing.preprocessing import remove_links, remove_punct, remove_double_spaces, remove_html_tags

df = pd.read_csv('../data/all-articles.csv', index_col=[0])

# Remove empty, duplicates
df = df.dropna()
df = df.drop_duplicates()
df = df.reset_index(drop=True)

# Lowercase data
df['articles'] = df['articles'].str.lower()

# Remove links
for index, row in df.iterrows():
    sentence = df.iloc[index]['articles']
    sentence_without_links = remove_links(sentence)
    df.at[index, 'articles'] = sentence_without_links

# Remove html tags
df['articles'] = remove_html_tags(df.articles)

# Remove punctuation 
for index, row in df.iterrows():
    sentence = df.iloc[index]['articles']
    sentence_without_punctuation = remove_punct(sentence)
    df.at[index, 'articles'] = sentence_without_punctuation

# Remove double spaces    
df['articles']=remove_double_spaces(df, 'articles')

df.to_csv('../data/articles-labeled.csv')