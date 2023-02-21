import pandas as pd
from preprocessing.preprocessing import (
    remove_links,
    remove_punct,
    remove_html_tags,
    remove_non_english,
    remove_mentions,
    remove_hashtags,
    remove_emoji,
)

df = pd.read_csv("../resources/messages.csv", index_col=[0])

# Remove short messages
wantedRows = df[df["content"].str.split().str.len() < 6].index
df = df.drop(wantedRows, axis=0)
df = df.reset_index(drop=True)

# Remove empty, duplicates
df = df.dropna()
df = df.drop_duplicates()
df = df.reset_index(drop=True)

# Remove non-english messages
df["content"] = remove_non_english(df, "content")

# Lowercase resources
df["content"] = df["content"].str.lower()

# Remove links
for index, row in df.iterrows():
    sentence = df.iloc[index]["content"]
    sentence_without_links = remove_links(sentence)
    df.at[index, "content"] = sentence_without_links

# Remove html tags
df["content"] = remove_html_tags(df.content)

# Remove mentions
df["content"] = remove_mentions(df.content)

# Remove hashtags
df["content"] = remove_hashtags(df.content)

# Remove emojis
for index, row in df.iterrows():
    sentence = df.iloc[index]["content"]
    sentence_without_emoji = remove_emoji(sentence)
    df.at[index, "content"] = sentence_without_emoji

# Remove punctuation
for index, row in df.iterrows():
    sentence = df.iloc[index]["content"]
    sentence_without_punctuation = remove_punct(sentence)
    df.at[index, "content"] = sentence_without_punctuation

df.to_csv("../resources/messages-prep.csv")
