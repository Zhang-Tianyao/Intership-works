import sqlite3
import pandas as pd
import re

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ============================
# 1. load data
# ============================
def load_data():
    conn = sqlite3.connect("db/reddit.db")

    posts = pd.read_sql_query("SELECT id, title, body FROM posts", conn)
    comments = pd.read_sql_query("SELECT id, body FROM comments", conn)

    conn.close()

    posts["text"] = posts["title"].fillna("") + " " + posts["body"].fillna("")
    comments["text"] = comments["body"].fillna("")

    df = pd.concat(
        [posts[["id", "text"]], comments[["id", "text"]]],
        ignore_index=True
    )

    df = df[df["text"].str.strip() != ""]
    return df


# ============================
# 2. clean text
# ============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # 去掉链接
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)  # 去掉符号
    text = re.sub(r"\s+", " ", text)  # 多空格合并
    return text.strip()


# ============================
# 3. sentiment analysis
# ============================
analyzer = SentimentIntensityAnalyzer()

def sentiment_textblob(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def sentiment_vader(text):
    score = analyzer.polarity_scores(text)
    return score["compound"]


# ============================
# 4. classify sentiment
# ============================
def classify_sentiment(compound):
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"


# ============================
# 5. main
# ============================
def main():
    print("Loading data...")
    df = load_data()

    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    print("Running TextBlob sentiment...")
    df["polarity"], df["subjectivity"] = zip(*df["clean_text"].apply(sentiment_textblob))

    print("Running VADER sentiment...")
    df["compound"] = df["clean_text"].apply(sentiment_vader)

    print("Classifying sentiment...")
    df["sentiment"] = df["compound"].apply(classify_sentiment)

    print("Saving results...")
    df.to_csv("sentiment_results.csv", index=False)

    print("Done.")
    print(df.head())


if __name__ == "__main__":
    main()
