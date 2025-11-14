import pandas as pd
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display

# Load Data
matches_url = "https://drive.google.com/uc?export=download&id=1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_url = "https://drive.google.com/uc?export=download&id=1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = pd.read_csv(matches_url)
deliveries = pd.read_csv(deliveries_url)

# Dropdown
dropdown = widgets.Dropdown(
    options=["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums", "Top Bowlers"],
    description="View:"
)

output = widgets.Output()

def show_graph(change):
    output.clear_output()
    with output:
        choice = change['new']

        if choice == "Top 5 Teams":
            data = matches['winner'].value_counts().head(5).reset_index()
            data.columns = ['Team', 'Wins']
            fig = px.bar(data, x='Team', y='Wins', title='Top 5 Teams by Wins')
            fig.show()

        elif choice == "Top Batsmen":
            data = deliveries.groupby('batsman')['batsman_runs'].sum().nlargest(10).reset_index()
            fig = px.bar(data, x='batsman_runs', y='batsman', orientation='h', title='Top 10 Batsmen')
            fig.show()

        elif choice == "Top Stadiums":
            data = matches['venue'].value_counts().head(10).reset_index()
            data.columns = ['Stadium', 'Matches']
            fig = px.bar(data, x='Matches', y='Stadium', orientation='h', title='Top 10 Stadiums',color='Matches')
            fig.show()

        elif choice == "Top Bowlers":
            wickets = deliveries[deliveries['player_dismissed'].notnull()]
            data = wickets.groupby('bowler').size().nlargest(5).reset_index(name='Wickets')
            fig = px.bar(data, x='Wickets', y='bowler', orientation='h', title='Top 5 Bowlers')
            fig.show()

dropdown.observe(show_graph, names='value')
display(dropdown, output)
