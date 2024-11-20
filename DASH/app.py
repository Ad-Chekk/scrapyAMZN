from scrapy_lib.spiders.ex_scrapy import NetworkingSpider3
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import threading


def refresh():
    csv_file_path = r"C:/EchoSift/data/net_data.csv"
    df = pd.read_csv(csv_file_path)


def run_spider(url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(NetworkingSpider3, url=url)
    
    # Start the spider without blocking
    process.start(stop_after_crawl=False)


# Load the CSV file
csv_file_path = r"C:/EchoSift/data/net_data.csv"
df = pd.read_csv(csv_file_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# CSS styles
styles = {
    'gradient-background': {
        'background': 'linear-gradient(to right, #000000, #00000f, #00005f)',
        'min-height': '100vh',
        'padding': '20px',
        'display': 'flex',  # Changed to flex for sidebar layout
    },
    'sidebar': {
        'padding': '20px',
        'background': 'linear-gradient(to right, #000000, #00000f, #00005f)',
        'borderRadius': '1px',
        'margin-right': '20px',
        'width': '17%',  # Width of the sidebar
        'height': '100vh',  # Full height
    },
    'content': {
        'flex': '1',  # Take remaining space
        'display': 'grid',
        'gridTemplateRows': 'auto auto',
        'gridGap': '20px',
    },
    'row-container': {
        'display': 'grid',
        'gridTemplateColumns': '1.5fr 1fr 1fr',  # Three equal columns for the first row
        'gridGap': '10px',  # Gap between the elements
        'width': '100%',
        'height': '40vh',
        'backgroundColor': 'rgba(0, 0, 0, 0)',
    },
    'two-chart-row': {
        'display': 'grid',
        'gridTemplateColumns': '1fr 1.5fr',  # Two equal columns for the second row
        'gridGap': '2px',  # Gap between the elements
        'height': '60vh',
    },
    'chart-container': {
        'backgroundColor': 'rgba(255, 255, 255, 0.0)',  # White color with 10% opacity
        'borderRadius': '3px',
        'padding': '15px',
    },
    'text-style': {
        'color': 'white',
        'textAlign': 'center',
    }
}

# App layout
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H4('Input URL to Scrape:', style=styles['text-style']),
        dcc.Input(id='url-input', type='text', placeholder='Enter a URL', style={'width': '100%',
         'border-radius': '3px', }),
        html.Button('Submit', id='submit-button', n_clicks=0, style={
    'margin-top': '5px',
    'padding': '10px 10px',  # Adds padding for a larger button
    'border-radius': '10px',  # Rounded corners
    'color': 'black',  # Button text color
    'font-size': '13px',  # Text size
    'font-weight': 'bold',  # Bold text
    'cursor': 'pointer',  # Cursor changes on hover 
    
}),
        html.Div(id='submit-response', style={'margin-top': '10px', 'color': 'white'}),
        html.H4('Scraper Parameters summary:', style=styles['text-style']),
    
        html.Div([
    html.H5('IP Addresses:', style={'font-family': 'Calibri', 'color': 'white', 'textAlign': 'left'}),
    html.Div(id='all-ips', style={
        'background-color': 'rgba(255, 255, 255, 0.1)',  # Light transparent background
        'padding': '10px',
        'border': '1px solid white',  # White border to differentiate
        'border-radius': '5px',
        'color': 'white',
        'font-family': 'Calibri',
        'overflow-wrap': 'break-word',  # Ensure long IP addresses break nicely
        'white-space': 'pre-wrap'  # Keep the formatting for lists
    }),
], style={'margin-top': '10px'}),

# Display all User Agents
html.Div([
    html.H5('User Agents:', style={'font-family': 'Calibri', 'color': 'white', 'textAlign': 'left'}),
    html.Div(id='all-user-agents', style={
        'background-color': 'rgba(255, 255, 255, 0.1)',  # Light transparent background
        'padding': '10px',
        'border': '1px solid white',  # White border to differentiate
        'border-radius': '5px',
        'color': 'white',
        'font-family': 'Calibri',
        'font-size': '10px',
        'overflow-wrap': 'break-word',
        'white-space': 'pre-wrap'
    }),
], style={'margin-top': '10px'}),

# Display all URLs
html.Div([
    html.H5('Scraped URLs:', style={'font-family': 'Calibri', 'color': 'white', 'textAlign': 'left'}),
    html.Div(id='all-urls', style={
        'background-color': 'rgba(255, 255, 255, 0.1)',  # Light transparent background
        'padding': '10px',
        'border': '1px solid white',  # White border to differentiate
        'border-radius': '5px',
        'color': 'white',
        'font-family': 'Calibri',
        'overflow-wrap': 'break-word',
        'white-space': 'pre-wrap'
    }),
], style={'margin-top': '10px'}),
    ], style=styles['sidebar']),



    # Main content area
    html.Div([

        html.H4('Analysis Engine' , style={'color': 'white'}),
        
        # First row with three elements
        html.Div([
            html.Div([dcc.Graph(id='response-time-hist', style={'height': '300px'})], style=styles['chart-container']),
            html.Div([dcc.Graph(id='status-code-pie', style={'height': '300px'})], style=styles['chart-container']),
            html.Div([dcc.Graph(id='avg-response-time-gauge', style={'height': '300px'})], style=styles['chart-container']),
        ], style=styles['row-container']),  # First row using CSS grid

        # Second row with two elements
        html.Div([
            html.Div([dcc.Graph(id='depth-content-scatter', style={'height': '350px'})], style=styles['chart-container']),
            html.Div([dcc.Graph(id='content-length-box', style={'height': '350px'})], style=styles['chart-container']),
        ], style=styles['two-chart-row'])  # Second row using CSS grid
    ], style=styles['content'])  # Main content area
], style=styles['gradient-background'])

# Callback function to update graphs
@app.callback(
    Output('status-code-pie', 'figure'),
    Output('response-time-hist', 'figure'),
    Output('depth-content-scatter', 'figure'),
    Output('avg-response-time-gauge', 'figure'),
    Output('content-length-box', 'figure'),
    Output('submit-response', 'children'),  # Output for submit response
    Output('all-ips', 'children'),
    Output('all-user-agents', 'children'),
    Output('all-urls', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('url-input', 'value')
)


def update_graphs(n_clicks, url):
    # If the button is clicked and URL is provided
    if n_clicks > 0 and url:

 # Start spider in a separate thread to avoid blocking Dash
        thread = threading.Thread(target=run_spider, args=(url,))
        thread.start()

        submit_response = f'Spider started for URL: {url}'


    else:
        submit_response = 'Enter a URL and click Submit to start scraping.'

    # Status Code Pie Chart
    status_counts = df['Status Code'].value_counts()
    fig_pie = px.pie(values=status_counts.values, names=status_counts.index, title='Status Code Distribution')
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, color='white'), # Transparent background for the entire chart
        margin=dict(l=30, r=30, t=50, b=10),
        legend_bgcolor='rgba(0,0,0,0)',  # Transparent legend background
        showlegend=True
    )
    fig_pie.update_traces(marker=dict(line=dict(color='rgba(0,0,0,0)')))
    ################################################################################
    refresh()     #refreshdatabase
    ##########################################################################################################
    # Response Time Histogram
    fig_bar = px.bar(df, x='Response Time (s)', title='Response Time Distribution')
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        title_font=dict(size=20, color='white'),  # Title font size and color
        xaxis=dict(
            title_font=dict(size=14, color='white'),  # X-axis title font size and color
            tickfont=dict(size=12, color='white')  # X-axis tick label font size and color
        ),
        yaxis=dict(
            title_font=dict(size=14, color='white'),  # Y-axis title font size and color
            tickfont=dict(size=12, color='white')  # Y-axis tick label font size and color
        ),
        margin=dict(l=20, r=20, t=30, b=10),  # Adjust margins as needed
        height=300,  # Reduce the height of the chart
        width=400 
    )


    # Depth vs Content Length Scatter Plot
    fig_scatter = px.scatter(df, x='Depth', y='Content Length', title='Depth vs Content Length',
                             color='Status Code', hover_data=['URL'])
    fig_scatter.update_layout(
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(0,0,0,0.5)',
        title_font=dict(size=20, color='white'),
        xaxis=dict(
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white')
        ),
        yaxis=dict(
            title_font=dict(size=14, color='white'),
            tickfont=dict(size=12, color='white')
        )
    )
    fig_scatter.update_traces(marker=dict(
        colorbar=dict(
            title=dict(
                text='Status Code',  # Title of the color bar
                font=dict(
                    size=14,
                    color='white'  # Change the color of the color bar label
                )
            ),
            tickfont=dict(
                size=12,
                color='white'  # Change the color of the tick labels on the color bar
            )
        )
    ))

    # Average Response Time Gauge
    avg_response_time = df['Response Time (s)'].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_response_time,
        title={'text': "Average Response Time (s)"},
        gauge={'axis': {'range': [None, df['Response Time (s)'].max()]},
               'steps': [
                   {'range': [0, 0.5], 'color': "white"},
                   {'range': [0.5, 1], 'color': "yellow"},
                   {'range': [1, df['Response Time (s)'].max()], 'color': "red"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1}}))
    fig_gauge.update_layout(
        plot_bgcolor='rgba(255,255,0,0.9)',  # Transparent background for the plot
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=20, color='white'),
        margin=dict(l=50, r=50, t=50, b=10)  
    )
    fig_line = px.line(df, y='Content Length', title='Content Length Over Time')
    fig_line.update_traces(line=dict(color='#1E90FF')) 
    fig_line.update_layout(
        plot_bgcolor='rgba(250, 250, 250, 0.1)', 
        paper_bgcolor='rgba(1,0,0,0.6)',  
        title_font=dict(size=20, color='white'),  
        yaxis=dict(
            title_font=dict(size=14, color='white'), 
            tickfont=dict(size=12, color='white')  
        )
    )
    all_ips = ', '.join(df['IP Address'].dropna().unique())
    all_user_agents = ', '.join(df['User Agent'].dropna().unique())
    all_urls = ', '.join(df['URL'].dropna().unique()[:5])
    

    return fig_pie, fig_bar, fig_scatter, fig_gauge, fig_line, submit_response, all_ips, all_user_agents, all_urls

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
