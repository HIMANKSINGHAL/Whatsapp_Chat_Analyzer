from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df["message"]:
        words.extend(message.split())

    num_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):

    x = df["user"].value_counts().head()

    new_df = (
        round((df["user"].value_counts() / df.shape[0]) * 100, 2)
        .reset_index()
    )
    new_df.columns = ["User", "Percent"]

    return x, new_df


def create_wordcloud(selected_user, df):

    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().split())

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"].copy()

    def remove_stop_words(message):
        return " ".join(
            word
            for word in message.lower().split()
            if word not in stop_words
        )

    temp["message"] = temp["message"].apply(remove_stop_words)

    text = temp["message"].str.cat(sep=" ").strip()

    if text == "":
        return None

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color="white"
    )

    return wc.generate(text)


def most_common_words(selected_user, df):

    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().split())

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    words = []

    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []

    for message in df["message"]:
        emojis.extend(
            [char for char in message if char in emoji.EMOJI_DATA]
        )

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=["Emoji", "Count"]
    )

    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = (
        df.groupby(["year", "month_num", "month"])
        .count()["message"]
        .reset_index()
    )

    timeline["time"] = (
        timeline["month"] + "-" + timeline["year"].astype(str)
    )

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return (
        df.groupby("only_date")
        .count()["message"]
        .reset_index()
    )


def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    if df.empty:
        return pd.DataFrame()

    user_heatmap = pd.pivot_table(
        data=df,
        index="day_name",
        columns="period",
        values="message",
        aggfunc="count",
        fill_value=0
    )

    # Order the weekdays
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    user_heatmap = user_heatmap.reindex(days)

    return user_heatmap
