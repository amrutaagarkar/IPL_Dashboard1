import streamlit as st
import pandas as pd
import requests
import io
import zipfile
import plotly.express as px

st.title("🏏 IPL Analytics Dashboard")
st.info("📥 Loading data from Google Drive...")

# -----------------------------
# Google Drive Direct Links
# -----------------------------
MATCHES_URL = "https://drive.google.com/uc?export=download&id=1YUc6XB52LI5d0b4kdsj8Ax9TMet1X241"
DELIVERIES_ZIP_URL = "https://drive.google.com/uc?export=download&id=1sPdWjzvWTTO4tv2ty9zpznMddGDklocs"


# -----------------------------
# Function: Load CSV (Normal File)
# -----------------------------
def load_csv(url):
    try:
        r = requests.get(url)
        content = r.content

        # Detect HTML error from Google Drive
        if b"<html" in content[:200].lower():
            st.error("❌ Google Drive returned an HTML page instead of CSV. File too large or permissions issue.")
            return None

        # Try different encodings
        for enc in ["utf-8", "latin1", "cp1252"]:
            try:
                return pd.read_csv(io.BytesIO(content), encoding=enc)
            except:
                pass

        st.error("❌ Could not decode CSV with utf-8, latin1, or cp1252.")
        return None

    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return None


# -----------------------------
# Function: Load CSV from ZIP
# -----------------------------
def load_csv_from_zip(url, expected_csv_name=None):
    try:
        r = requests.get(url)
        content = r.content

        # Detect HTML error
        if b"<html" in content[:200].lower():
            st.error("❌ Google Drive returned HTML instead of ZIP. ZIP too large or access denied.")
            return None

        # Load ZIP from bytes
        z = zipfile.ZipFile(io.BytesIO(content))

        # If user doesn't know filename → pick first CSV inside
        if not expected_csv_name:
            for name in z.namelist():
                if name.endswith(".csv"):
                    expected_csv_name = name
                    break

        with z.open(expected_csv_name) as f:
            data = f.read()

        # Try encodings
        for enc in ["utf-8", "latin1", "cp1252"]:
            try:
                return pd.read_csv(io.BytesIO(data), encoding=enc)
            except:
                pass

        st.error("❌ Could not decode CSV inside ZIP file.")
        return None

    except Exception as e:
        st.error(f"❌ Error reading ZIP: {e}")
        return None


# -----------------------------
# Load Data
# -----------------------------
matches = load_csv(MATCHES_URL)
deliveries = load_csv_from_zip(DELIVERIES_ZIP_URL)

if matches is None or deliveries is None:
    st.stop()


# -----------------------------
# Dashboard UI
# -----------------------------
choice = st.selectbox(
    "Select a visualization 👇",
    ["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums", "Top Bowlers"]
)


# -----------------------------
# Visualization Logic
# -----------------------------
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
