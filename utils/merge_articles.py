import pandas as pd

art_df = pd.read_csv("../data/articles.csv", index_col=[0])
sputnik_df = pd.read_csv("../data/sputnik_news_up.csv", encoding="cp1252")

sputnik_df = sputnik_df.rename(columns={"Column2": "articles"})
sputnik_df = sputnik_df.drop(["Column1"], axis=1)

# Set labels
sputnik_df["label"] = 0  # disinformation
art_df["label"] = 1  # real facts

articles_df = pd.concat([art_df, sputnik_df], axis=0, ignore_index=True)

# Remove short articles
wantedRows = articles_df[articles_df["articles"].str.split().str.len() < 6].index
articles_df = articles_df.drop(wantedRows, axis=0)
articles_df = articles_df.reset_index(drop=True)

print(articles_df)
articles_df.to_csv("../data/all-articles.csv")
