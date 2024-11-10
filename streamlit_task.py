import os
from collections import Counter

import pandas as pd
import requests
import streamlit as st
import dotenv

dotenv.load_dotenv()

search_term = st.text_input("Wyszukaj feedback")

r = requests.post(
    f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE')}/query",
    headers={
        "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",
        "Notion-Version": "2021-05-13",
    },
)
data = r.json()["results"]
data = {
    "Action": [
        data[i]["properties"]["Action"]["rich_text"][0]["text"]["content"]
        for i in range(len(data))
    ],
    "Situation": [
        data[i]["properties"]["Situation"]["title"][0]["text"]["content"]
        for i in range(len(data))
    ],
    "Outcome": [
        data[i]["properties"]["Outcome"]["rich_text"][0]["text"]["content"]
        for i in range(len(data))
    ],
}
df = pd.DataFrame(data)
df = df[df["Situation"].str.contains(search_term)]
st.dataframe(df, hide_index=True)

st.metric(label="Feedback count", value=len(df))

words = " ".join(df["Action"] + " " + df["Situation"] + " " + df["Outcome"]).split()
counter = Counter(words)
chart_data = pd.DataFrame(counter.most_common(20), columns=["word", "count"])

st.bar_chart(chart_data, x="word", y="count", horizontal=True)
