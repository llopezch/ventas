import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import datetime
from pytz import timezone
from app import app

# Configura tu token de acceso personal de GitHub
github_token = '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'

# Función para obtener el historial de commits desde GitHub
def get_commit_history():
    repo_url = "https://api.github.com/repos/kont123456/datosventas/commits"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(repo_url, headers=headers)
    commits = response.json()
    return commits

# Función para filtrar commits y obtener información relevante
def filter_commits(commits):
    # Obtén la zona horaria local
    local_tz = timezone('America/Lima')  # Reemplaza 'America/Lima' con tu zona horaria local

    # Filtra solo las últimas 10 actualizaciones
    filtered_commits = []
    for commit in list[:10]:
        # Obtener la fecha y hora sin la 'T' y 'Z' y con el formato deseado
        fecha_raw = commit['commit']['author']['date']
        fecha_obj_utc = datetime.strptime(fecha_raw, "%Y-%m-%dT%H:%M:%SZ")
        
        # Convierte a la zona horaria local
        fecha_obj_local = fecha_obj_utc.replace(tzinfo=timezone('UTC')).astimezone(local_tz)
        
        fecha_formateada = fecha_obj_local.strftime("%d-%m-%Y %H:%M:%S")

        # Divide la fecha y la hora
        fecha, hora = fecha_formateada.split(' ')
        

        commit_info = {
            
            'fecha': fecha,
            'hora': hora,
            'mensaje': commit['commit']['message']
        }
        filtered_commits.append(commit_info)
        # Agrega dos líneas en blanco para separar las fechas
        
    return filtered_commits


