import pandas as pd
import dash
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc
github_token = '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'

estilos = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.MATERIA]


app = dash.Dash(__name__, external_stylesheets=estilos)
server=app.server
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True

