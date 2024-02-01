import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import datetime
from pytz import timezone
import os

# Configura tu token de acceso personal de GitHub
github_token = os.getenv('GITHUB_TOKEN')

# Función para obtener el historial de commits desde GitHub
def get_commit_history():
    repo_url = "https://api.github.com/repos/kont123456/datosventas/commits"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(repo_url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return []

def filter_commits(commits):
    # Obtén la zona horaria local
    local_tz = timezone('America/Lima')  # Reemplaza 'America/Lima' con tu zona horaria local
  
    # Filtra solo las últimas 10 actualizaciones
    filtered_commits = []
    for commit in commits[:10]:
        if isinstance(commit, dict) and 'commit' in commit and 'author' in commit['commit'] and 'date' in commit['commit']['author']:
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
        else:
            print(f"Commit inválido: {commit}")
        
    return filtered_commits

