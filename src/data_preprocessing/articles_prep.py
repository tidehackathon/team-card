from .preprocessing import remove_links, remove_punct, remove_html_tags, remove_html_tags_string


def preprocess_articles(df, column_name):
    """Returns a preprocessed dataframe.
    
    Args:
        df (dataframe): articles dataframe.
        column_name (str): the name of the text column which will be preprocessed.

    Returns:
        df (datafarme): a preprocessed dataframe.
                        Preprocessing steps: lowercase the text, remove html links and tags, remove punctuation.
    """

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

def preprocess_article(article):
    """Returns a preprocessed article text in a string format.

    Args:
        article (str): the article text in a string format.

    Returns:
        article (str): the preprocessed article in a string format.
                       Preprocessing steps: lowercase the text, remove html links and tags, remove punctuation.
    """
    article = article.lower()
    article = remove_links(article)
    article = remove_html_tags_string(article)
    article = remove_punct(article)
    return article
