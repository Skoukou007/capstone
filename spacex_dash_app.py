# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app_port = 4546
app = dash.Dash(__name__)

# Create dropdown options
launch_sites = spacex_df['Launch Site'].unique()
options_dropdown = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in launch_sites]

# Create app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=options_dropdown,
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={i: str(i) for i in range(0, 10001, 1000)}),
    
    # Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# ✅ Task 2: PIE CHART callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names='Launch Site', 
                     title='Total Successful Launches by Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(df, names='class', 
                     title=f'Success vs Failure for {selected_site}')
    return fig

# ✅ Task 4: SCATTER PLOT callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df.copy()

    # Filter by site
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Filter by payload range
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    # Create scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=f'Success by Payload for {selected_site}')
    return fig

# Run app
if __name__ == '__main__':
    app.run(port=app_port, debug=True)
