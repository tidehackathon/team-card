from .preprocessing import remove_links, remove_punct, remove_html_tags


def preprocess_articles(df, column_name):

    # Remove empty, duplicates
    df = df.dropna().drop_duplicates().reset_index(drop=True)

    # Lowercase data
    df[column_name] = df[column_name].str.lower()

    # Remove links
    for index, row in df.iterrows():
        sentence = df.iloc[index][column_name]
        sentence_without_links = remove_links(sentence)
        df.at[index, column_name] = sentence_without_links

    # Remove html tags
    df[column_name] = remove_html_tags(df.articles)

    # Remove punctuation
    for index, row in df.iterrows():
        sentence = df.iloc[index][column_name]
        sentence_without_punctuation = remove_punct(sentence)
        df.at[index, column_name] = sentence_without_punctuation

    return df
