import pandas as pd
from data_preprocessing.articles_prep import preprocess_articles
from data_preprocessing.messages_prep import preprocess_messages

df_art = pd.read_csv("../resources/all-articles.csv", index_col=[0])
df_msg = pd.read_csv("../resources/messages.csv", index_col=[0])

df_msg = preprocess_messages(df_msg, "content")
df_art = preprocess_articles(df_art, "articles")

df_art.to_csv("../resources/articles-prep-test2.csv")
df_msg.to_csv("../resources/messages-prep-test.csv")