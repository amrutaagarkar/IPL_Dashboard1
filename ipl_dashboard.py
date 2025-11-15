import streamlit as st
import pandas as pd
import requests
import io
import zipfile
import plotly.express as px

st.title("🏏 IPL Analytics Dashboard")

MATCHES_URL = "https://drive.google.com/uc?export=download&id=1YUc6XB52LI5d0b4kdsj8Ax9TMet1X241"
DELIVERIES_ZIP_URL = "https://drive.google.com/uc?export=download&id=1sPdWjzvWTTO4tv2ty9zpznMddGDklocs"

def load_csv(url):
    try:
        r = requests.get(url)
        for enc in ["utf-8", "latin1", "cp1252"]:
            try:
                return pd.read_csv(io.BytesIO(r.content), encoding=enc)
            except:
                pass
        st.error("❌ Could not decode CSV.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

def load_csv_from_zip(url):
    try:
        z = zipfile.ZipFile(io.BytesIO(requests.get(url).content))
        csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
        data = z.read(csv_name)
        for enc in ["utf-8", "latin1", "cp1252"]:
            try:
                return pd.read_csv(io.BytesIO(data), encoding=enc)
            except:
                pass
        st.error("❌ Could not decode ZIP CSV.")
        return None
    except Exception as e:
        st.error(f"❌ ZIP error: {e}")
        return None

matches = load_csv(MATCHES_URL)
deliveries = load_csv_from_zip(DELIVERIES_ZIP_URL)

if matches is None or deliveries is None:
    st.stop()

choice = st.selectbox(
    "Select a visualization 👇",
    ["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums", "Top Bowlers"]
)

if choice == "Top 5 Teams":
    data = matches['winner'].value_counts().head(5).reset_index()
    data.columns = ['Team', 'Wins']
    st.plotly_chart(px.bar(data, x='Team', y='Wins'))

elif choice == "Top Batsmen":
    data = deliveries.groupby('batsman')['batsman_runs'].sum().nlargest(10).reset_index()
    st.plotly_chart(px.bar(data, x='batsman_runs', y='batsman', orientation='h'))

elif choice == "Top Stadiums":
    data = matches['venue'].value_counts().head(10).reset_index()
    data.columns = ['Stadium', 'Matches']
    st.plotly_chart(px.bar(data, x='Matches', y='Stadium', orientation='h'))

elif choice == "Top Bowlers":
    wk = deliveries[deliveries['player_dismissed'].notnull()]
    data = wk.groupby('bowler').size().nlargest(5).reset_index(name='Wickets')
    st.plotly_chart(px.bar(data, x='Wickets', y='bowler', orientation='h'))
