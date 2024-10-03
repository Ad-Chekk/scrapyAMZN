# import os
# import subprocess
# import dash
# from dash import html
# from dash.dependencies import Input, Output

# # Initialize the app
# app = dash.Dash(__name__)

# # Define the layout of the app with a gradient background and a button
# app.layout = html.Div(
#     children=[
#         html.Button('Execute Scrapy Command', id='execute-button', n_clicks=0),
#         html.Div(id='output-div')  # Placeholder for command output
#     ],
#     style={
#         'background': 'linear-gradient(to right, #a1c4fd, #c2e9fb)',  # Light blue to light green
#         'height': '100vh',  # Full viewport height
#         'display': 'flex',
#         'flexDirection': 'column',
#         'justifyContent': 'center',
#         'alignItems': 'center',
#         'textAlign': 'center',
#     }
# )

# # Define callback to execute Scrapy command when button is clicked
# @app.callback(
#     Output('output-div', 'children'),
#     Input('execute-button', 'n_clicks')
# )
# def execute_command(n_clicks):
#     if n_clicks > 0:
#         try:
#             # Define the path to your Scrapy project directory
#             scrapy_project_dir = r'C:\Users\ADMIN\Desktop\scrapy_lib'  # Replace with the actual path

#             # Run the Scrapy command in the specified directory
#             result = subprocess.run(
#                 'scrapy crawl quotes',  # Replace 'myspider' with your spider's name
#                 shell=True, capture_output=True, text=True, cwd=scrapy_project_dir
#             )

#             # Display the output from the Scrapy command
#             return f"Scrapy Output:\n{result.stdout}"
#         except subprocess.CalledProcessError as e:
#             # Handle errors (e.g., if Scrapy command fails)
#             return f"Error executing Scrapy command:\n{str(e)}"
#     return "Click the button to execute the Scrapy command"

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
