import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Baseball Assessment")
st.header('Batted Ball Data')
st.markdown("This baseball data project visualizes and contextualizes batted ball outcomes between a batter and pitcher, focusing on the metrics of play outcomes, exit velocity, and launch angle. This project was built using Python with the Pandas, Streamlit, and Plotly libraries. \n\n" \
"The first graph is a pie chart that shows the distribution of outcomes for the whole dataset, as well as an option to view individual batters and their plate appearance outcomes. This visualization reveals that nearly two-thirds of all batted balls result in outs, which shows how difficult it is to reach base in professional baseball. It was also interesting to see that triples were more common than reaching on base due to a fielder's choice. \n\n" \
"The second graph illustrates the play outcomes and what the average exit velocity is for each in a bar graph. Exit velocity is a very important metric as it is a key indicator of quality of contact. The harder the ball is hit, the better the chance it will result in a hit rather than an out. Looking at the graph, if a player is able to generate an exit velocity of above 95–97 mph there is a very good chance that it will result in extra bases. \n\n" \
"The third graph displays resulting play outcomes with launch angle and exit velocity represented by colored points on a scatter plot. While exit velocity is an important metric, launch angle directly correlates with it. Balls hit too low or too high, regardless of speed, often result in outs with ground balls or popups. The ideal 'sweet spot' for launch angle is between 8 and 32 degrees, and it is shown very clearly here, as hits and runs tend to cluster within that range when paired with high exit velocity. \n\n")
st.divider()

# Load FIle
excel_file = 'BattedBallData.xlsx'
sheet_name = 'Data'

# Read Data
df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='A:M', header=0)

# Dropdown
batter_list = sorted(df['BATTER'].dropna().unique().tolist())
batter_list = ['All Batters'] + batter_list

selected_batter = st.selectbox("Select a Batter:", batter_list, index=0)

# Filter for the selected batter
if selected_batter == 'All Batters':
    filtered_df = df
else:
    filtered_df = df[df['BATTER'] == selected_batter]

# Group and count outcomes
outcome_counts = filtered_df['PLAY_OUTCOME'].value_counts().reset_index()
outcome_counts.columns = ['PLAY_OUTCOME', 'COUNT']

# Plot the pie chart
pie_chart = px.pie(
    outcome_counts,
    title=f"Distribution for {selected_batter}",
    values='COUNT',
    names='PLAY_OUTCOME'
)

# Display in Streamlit
st.plotly_chart(pie_chart)

st.divider()

# Bar graph for velo vs outcome

# Clean: remove rows with missing values in either column
velo_df = df[['PLAY_OUTCOME', 'EXIT_SPEED']].dropna()

# Group by outcome and calculate average exit speed
avg_exit_by_outcome = velo_df.groupby('PLAY_OUTCOME')['EXIT_SPEED'].mean().reset_index()
avg_exit_by_outcome.columns = ['PLAY_OUTCOME', 'AVG_EXIT_SPEED']

# Create bar graph
bar_chart = px.bar(
    avg_exit_by_outcome,
    x='PLAY_OUTCOME',
    y='AVG_EXIT_SPEED',
    title='Average Exit Speed by Play Outcome',
    labels={'AVG_EXIT_SPEED': 'Avg Exit Velocity (mph)', 'PLAY_OUTCOME': 'Outcome'},
    color='PLAY_OUTCOME',
    range_y=[60,110]
)

# Display in Streamlit
st.plotly_chart(bar_chart)

st.divider()

# Scatter plot for launch angle vs exit speed

# Drop rows with missing values for either launch angle or exit speed
df = df[['LAUNCH_ANGLE', 'EXIT_SPEED', 'PLAY_OUTCOME']].dropna()

# Create scatter plot
scatter_plot = px.scatter(
    df,
    x='LAUNCH_ANGLE',
    y='EXIT_SPEED',
    color='PLAY_OUTCOME',
    title='Launch Angle vs Exit Speed Colored by Play Outcome',
    labels={
        'LAUNCH_ANGLE': 'Launch Angle (°)',
        'EXIT_SPEED': 'Exit Velocity (mph)',
        'PLAY_OUTCOME': 'Outcome'
    },
    hover_data=['PLAY_OUTCOME'],
    range_x=[-90, 90]
)

# Display in Streamlit
st.plotly_chart(scatter_plot)
