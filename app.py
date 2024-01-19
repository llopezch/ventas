import pandas as pd
import dash
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc

estilos = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.MATERIA]

app = dash.Dash(__name__, external_stylesheets=estilos)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server
