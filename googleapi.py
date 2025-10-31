import streamlit as st
import feedparser
from datetime import datetime, timedelta

# -------------------------
# Helper function
# -------------------------
def get_google_news(query, days):
    """
    Fetch Google News RSS feed and filter by date range
    """
    feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    news_items = []
    cutoff_date = datetime.now() - timedelta(days=days)

    for entry in feed.entries:
        # Convert published time
        try:
            published_time = datetime(*entry.published_parsed[:6])
        except AttributeError:
            continue

        if published_time >= cutoff_date:
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": published_time.strftime("%Y-%m-%d %H:%M"),
                "summary": entry.summary
            })

    return news_items

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Cipla News Tracker", layout="wide")
st.title("📰 Cipla News Dashboard")

st.markdown("This dashboard shows the latest news about **Cipla Ltd** for various time ranges (1 week, 1 month, 3 months).")

# Sidebar
st.sidebar.header("🔎 Settings")
query = st.sidebar.text_input("Search Query", "Cipla")
time_range = st.sidebar.radio("Select Time Range", ["Last Week", "Last Month", "Last 3 Months"])

if time_range == "Last Week":
    days = 7
elif time_range == "Last Month":
    days = 30
else:
    days = 90

# Fetch data
with st.spinner(f"Fetching {time_range.lower()} news for '{query}'..."):
    news = get_google_news(query, days)

# -------------------------
# Display Results
# -------------------------
if news:
    st.success(f"Found {len(news)} news articles for '{query}' ({time_range})")
    for item in news:
        st.markdown(f"### [{item['title']}]({item['link']})")
        st.caption(f"🗓 Published: {item['published']}")
        st.write(item["summary"])
        st.divider()
else:
    st.warning("No recent news found for this period. Try adjusting the time range or query.")
