import re
import string

# Remove links
def remove_links(text_string):
    pattern = re.sub(
        r"(https?:\/\/)?([\da-z\.-]+)\.(com|net|lt|eu|be|org|me|co|info|ly|gov|de|ru|it|fm|us|space|direct|biz|to|gl|vn|link|tv|ph|fi|fr|pub|watch|sk|su|ua|market|ink|at|cz|se|army|ee|nz|int|es|ngo|news|goog|edu|ws|world|one|uk|app|ca|video|bg|in|st|ac|im|l|c|sg|doctor|ir|mil|ie|sh|io|nl|kg|city|g|is|by)+((\/|\&|\=|\.|\?|-|#){1}\w+)*",
        "",
        str(text_string),
    )
    return pattern


# Remove html tags
def remove_html_tags(text_string):
    text_string = text_string.apply(lambda x: re.sub("(<.*?>).*?(<.*?>)", "", x))
    return text_string
    

def remove_html_tags_string(text_string):
    text_string = re.sub("(<.*?>).*?(<.*?>)", "", text_string)
    return text_string


# Remove mentions
def remove_mentions(text_string):
    text_string = text_string.str.replace("@[A-Za-z0-9]+\s?", "", regex=True)
    return text_string

def remove_mentions_string(text_string):
    text_string = re.sub("@[A-Za-z0-9]+\s?", "", text_string)
    return text_string


# Remove hashtags
def remove_hashtags(text_string):
    text_string = text_string.str.replace("#[A-Za-z0-9]+\s?", "", regex=True)
    return text_string

def remove_hashtags_string(text_string):
    text_string = re.sub("#[A-Za-z0-9]+\s?", "", text_string)
    return text_string


# Remove non-english
def remove_non_english(df, column_name):
    text = df[df[column_name].map(lambda x: x.isascii())].reset_index(drop=True)
    return text


# Remove emojis
emoji_nuke2 = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)

emoj = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F913-\U0001F937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "\u263a"
    "]+",
    re.UNICODE,
)

emoji_string_nuke2 = re.compile(r"U0001F[0-9A-F]{3}")
emoji_string_nuke_lower2 = re.compile(r"0001f[0-9a-f]{3}")


def remove_emoji(text_string):
    text_string = emoji_nuke2.sub(r"", text_string)
    text_string = emoji_string_nuke2.sub(r"", text_string)
    text_string = emoji_string_nuke_lower2.sub(r"", text_string)
    text_string = re.sub("\s+", " ", text_string)
    text_string = re.sub(emoj, "", text_string)
    text_string = re.sub("(<u+.*?>)", "", text_string)
    return text_string


# Remove punctuation
def remove_punct(text_string):
    text_string = text_string.translate(
        str.maketrans(string.punctuation, " " * len(string.punctuation))
    )
    text_string = text_string.replace("„", " ")
    text_string = text_string.replace("“", " ")
    text_string = text_string.replace("”", " ")
    text_string = text_string.replace("’", " ")
    text_string = text_string.replace("‘", " ")
    text_string = text_string.replace("…", " ")
    text_string = text_string.replace("–", " ")
    text_string = text_string.replace("—", " ")
    text_string = text_string.replace("   ", " ")
    text_string = text_string.replace("  ", " ")
    text_string = text_string.replace("   ", " ")
    text_string = re.sub(r"(\w+)(\d{4})", r"\1 \2", text_string)
    return text_string
