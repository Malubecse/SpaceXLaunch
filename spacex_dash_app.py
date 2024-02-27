# Import required libraries
import pandas as pd
import dash
from dash import html
#import dash_html_components as html
from dash import dcc
#import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launchlist =set(spacex_df['Launch Site'])


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                          {'label': "CCAFS LC-40", 'value': "CCAFS LC-40"},
                                          {'label': "CCAFS SLC-40", 'value':  "CCAFS SLC-40"},
                                          {'label': "KSC LC-39A", 'value': "KSC LC-39A"},
                                          {'label': "VAFB SLC-4E", 'value': "VAFB SLC-4E"},
                                          #{'label': i, 'value': i} for i in launchlist
                                         # {'label': spacex_df.loc[0,'Launch Site'], 'value': spacex_df.loc[0,'Launch Site']}
                                           #for i in range(0,spacex_df['Launch Site'].size)],
                                          
                                        ],
                                        value='ALL',
                                         placeholder='Select Site',searchable=True),
                                #  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,
                                               marks={0: '0',100: '100'},value=[min_payload,max_payload]),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))
def update_output_container(selected_launch_site):
    print("$$$$$$$$$$$"+selected_launch_site)
    if(selected_launch_site=='ALL'):
        print('IFFIFIFIFIF')
        exp_rec =spacex_df.groupby('Launch Site')['class'].sum() 
        print(exp_rec)
        figure=px.pie(exp_rec,
        values='class',
        names="class",
        title="Total successful launches count for all sites")
        return figure
                
    else:
        print('EEEEEEEEELSE')
        filter_df=spacex_df[spacex_df['Launch Site']==selected_launch_site]
        exp_rec =filter_df.groupby('class')['class'].count()
        print(exp_rec)
        figure=px.pie(exp_rec,
        values='class', 
        names="class",
        title="Total successful launches count for Launch Site {}".format(selected_launch_site))
        return figure
                
   
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
         Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown',component_property='value'),
        Input(component_id='payload-slider',component_property='value')])

def update_input_output_container(selected_launch_site,payload_slider):
    if selected_launch_site=='ALL':
            figure=px.scatter(spacex_df,y="class", x="Payload Mass (kg)", color="Booster Version Category",title='Correlation between payload and Success for all sites')
            return figure
    else:
            filter_df=spacex_df[spacex_df['Launch Site']==selected_launch_site]
            figure=px.scatter(filter_df,
                              y="class", x="Payload Mass (kg)", 
                             color="Booster Version Category",
                             title="Correlation between payload and Success for {}".format(selected_launch_site))
            return figure
# Run the app
if __name__ == '__main__':
    app.run_server()
