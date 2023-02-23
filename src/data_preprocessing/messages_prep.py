from .preprocessing import (
    remove_links,
    remove_punct,
    remove_html_tags,
    remove_non_english,
    remove_mentions,
    remove_hashtags,
    remove_emoji,
)

def preprocess_messages(df, column_name):
    # Remove short messages
    wantedRows = df[df[column_name].str.split().str.len() < 6].index
    df = df.drop(wantedRows, axis=0)
    df = df.reset_index(drop=True)

    # Remove empty, duplicates
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    # Remove non-english messages
    df = remove_non_english(df, column_name)

    # Lowercase resources
    df[column_name] = df[column_name].str.lower()

    # Remove links
    for index, row in df.iterrows():
        sentence = df.iloc[index][column_name]
        sentence_without_links = remove_links(sentence)
        df.at[index, column_name] = sentence_without_links

    # Remove html tags
    df[column_name] = remove_html_tags(df.content)

    # Remove mentions
    df[column_name] = remove_mentions(df.content)

    # Remove hashtags
    df[column_name] = remove_hashtags(df.content)

    # Remove emojis
    for index, row in df.iterrows():
        sentence = df.iloc[index][column_name]
        sentence_without_emoji = remove_emoji(sentence)
        df.at[index, column_name] = sentence_without_emoji

    # Remove punctuation
    for index, row in df.iterrows():
        sentence = df.iloc[index][column_name]
        sentence_without_punctuation = remove_punct(sentence)
        df.at[index, column_name] = sentence_without_punctuation

    filter = df[column_name] != ""
    dfNew = df[filter]
    dfNew = dfNew.drop_duplicates().reset_index(drop=True)

    return dfNew

def preprocess_message(message):
    message = message.lower()
    message = remove_links(message)
    message = remove_html_tags(message)
    message = remove_mentions(message)
    message = remove_hashtags(message)
    message = remove_emoji(message)
    message = remove_punct(message)
    return message
