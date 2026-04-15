import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# ============================
# 1. init output directory
# ============================
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================
# 2. load data
# ============================
df = pd.read_csv("sentiment_results.csv")

# ============================
# 3. sentiment distribution
# ============================
plt.figure(figsize=(6,4))
df["sentiment"].value_counts().plot(kind="bar", color=["green","gray","red"])
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sentiment_distribution.png"), dpi=300)
plt.close()

# ============================
# 4. word clouds
# ============================
def generate_wordcloud(text, title, filename):
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(" ".join(text))

    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close()

# positive word cloud
generate_wordcloud(
    df[df["sentiment"]=="positive"]["clean_text"],
    "Positive WordCloud",
    "positive_wordcloud.png"
)

# negative word cloud
generate_wordcloud(
    df[df["sentiment"]=="negative"]["clean_text"],
    "Negative WordCloud",
    "negative_wordcloud.png"
)

# ============================
# 5. sentiment feature correlation heatmap
# ============================
corr = df[["polarity", "subjectivity", "compound"]].corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Sentiment Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sentiment_heatmap.png"), dpi=300)
plt.close()

print("All visualizations saved to:", OUTPUT_DIR)
