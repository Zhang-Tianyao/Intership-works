import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv("sentiment_results.csv")

plt.figure(figsize=(6,4))
df["sentiment"].value_counts().plot(kind="bar", color=["green","gray","red"])
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

def generate_wordcloud(text, title):
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(text))
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()

generate_wordcloud(df[df["sentiment"]=="positive"]["clean_text"], "Positive WordCloud")

generate_wordcloud(df[df["sentiment"]=="negative"]["clean_text"], "Negative WordCloud")

corr = df[["polarity", "subjectivity", "compound"]].corr()
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Sentiment Feature Correlation Heatmap")
plt.tight_layout()
plt.show()
