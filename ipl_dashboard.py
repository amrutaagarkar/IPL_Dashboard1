import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px

st.title("🏏 IPL Analytics Dashboard")

# Convert Google Drive links
matches_url = "https://drive.google.com/uc?export=download&id=1YUc6XB52LI5d0b4kdsj8Ax9TMet1X241"
deliveries_url = "https://drive.google.com/uc?export=download&id=1sPdWjzvWTTO4tv2ty9zpznMddGDklocs"

# Function to load CSV from Google Drive
def load_csv(url):
    try:
        r = requests.get(url)
        return pd.read_csv(io.BytesIO(r.content))
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

st.info("📥 Loading data from Google Drive...")
matches = load_csv(matches_url)
deliveries = load_csv(deliveries_url)

if matches is None or deliveries is None:
    st.stop()

# Dropdown / Selectbox
choice = st.selectbox(
    "Select a visualization 👇",
    ["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums", "Top Bowlers"]
)

# Display Graphs
if choice == "Top 5 Teams":
    data = matches['winner'].value_counts().head(5).reset_index()
    data.columns = ['Team', 'Wins']
    fig = px.bar(data, x='Team', y='Wins', title='Top 5 Teams by Wins')
    st.plotly_chart(fig)

elif choice == "Top Batsmen":
    data = deliveries.groupby('batsman')['batsman_runs'].sum().nlargest(10).reset_index()
    fig = px.bar(data, x='batsman_runs', y='batsman', orientation='h', title='Top 10 Batsmen')
    st.plotly_chart(fig)

elif choice == "Top Stadiums":
    data = matches['venue'].value_counts().head(10).reset_index()
    data.columns = ['Stadium', 'Matches']
    fig = px.bar(data, x='Matches', y='Stadium', orientation='h', title='Top 10 Stadiums')
    st.plotly_chart(fig)

elif choice == "Top Bowlers":
    wickets = deliveries[deliveries['player_dismissed'].notnull()]
    data = wickets.groupby('bowler').size().nlargest(5).reset_index(name='Wickets')
    fig = px.bar(data, x='Wickets', y='bowler', orientation='h', title='Top 5 Bowlers')
    st.plotly_chart(fig)
