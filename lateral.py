import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.express as px 
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
from app import app
from df import df

layout=dbc.Container([
         dbc.Card([
         html.Div([
                    html.I(className="fas fa-th",style={"margin":"auto", "font-size":"30px","color":"white"}), 
                    html.H1("Ventas Totales",style={"font-size":"16px","padding-top": "15px","color":"white","margin-right":"34px"}),
          ],style={"display":"flex","margin-top":"25px"}),
       
           html.Hr(style={"color":"white"}),
           html.Br(),
           html.Legend("Filtros",style={"font-size":"16px","padding-left":"20px","color":"white"}),
           html.Div([
                dbc.Row([
                   dbc.Col([
                   
                            html.Label("Productos",style={"padding-left":"58px","color":"white"}),
                            html.Div([
                            html.I(className="far fa-dot-circle",style={"color":"white","margin-right":"-15px","margin-top":"55px"}),
                            dcc.Dropdown(id="lista1",
                                         persistence=True,
                                         persistence_type="session",
                                         clearable=False,
                                         multi=True,
                                       
                                         style={"font-size":"13px","width": "153px","margin-left": "30px","height":120,'background-color':'black',"left": "-30px"},
                                         
                                         ),
                            ],style={"display":"flex"}),
                            html.Br(),
                            html.Label("Empaque",style={"padding-left": "58px","color":"white"}),
                            html.Div([
                            html.I(className="far fa-dot-circle",style={"color":"white","margin-right":"-15px","margin-top":"55px"}),
                            
                            dcc.Dropdown(id="lista2",
                                         persistence=True,
                                         persistence_type="session",
                                         clearable=False,
                                         multi=True,
                                         style={"font-size":"14px","width": "153px","margin-left": "30px","height":120,'background-color':'black',"left": "-30px"}
                                         ),
                            
                            ],style={"display":"flex"}),
                            html.Br(),
                            html.Label("Pais",style={"padding-left":"58px","color":"white"}),
                            html.Div([
                            html.I(className="far fa-dot-circle",style={"color":"white","margin-right":"-15px","margin-top":"55px"}),
                            
                            dcc.Dropdown(id="lista3",
                                         persistence=True,
                                         persistence_type="session",
                                         clearable=False,
                                         multi=True,
                                         
                                         style={"font-size":"14px","width": "153px","margin-left": "30px","height":120,'background-color':'black',"left": "-30px"}
                                         )   
                            ],style={"display":"flex"}),                         
                   
                   ])# Aquí especificamos el ancho en diferentes tamaños de pantallas
               ])
           ], style={"margin-left": "30px"}), 
           html.Br(),
           dbc.Row([
               dbc.Col([
                   
                       dbc.Nav([
                           dbc.NavLink("ventas totales",href="/grafico1",active="exact"),
                           dbc.NavLink("ventas paises",href="/grafico2",active="exact")
                       ],vertical=True,pills=True,id="nav-link",style={"margin-bottom":"1px","width": "210px","padding-left": "15px","textAlign": "center"})
                  
               ])
           ])
         ],style={"height":760,"margin-top":"10px",'background-color':'black',"width": "228px","margin-left": "-12px",'border-radius': '15px'})  
])
@app.callback( Output("lista1","options"),
              [Input("lista2","value"),
               Input("lista3","value")])

def actualizar_listas(b_value,c_value):
    
    df_temp=df
    if b_value:
       df_temp=df_temp[df_temp["Empaque"].isin(b_value)] 
    
    if c_value:
       df_temp=df_temp[df_temp["Region"].isin(c_value)]
    
    return [{"label":x,"value":x} for x in sorted(df_temp["Subcategoria"].unique())]

@app.callback(Output("lista2","options"),
              [Input("lista1","value"),
               Input("lista3","value")])

def actualizar_listas2(a_value,c_value):
    df_temp=df
    if a_value:
       df_temp=df_temp[df_temp["Subcategoria"].isin(a_value)]
       
    if c_value:
       df_temp=df_temp[df_temp["Region"].isin(c_value)]
    
    return[{"label":x,"value":x} for x in sorted(df_temp["Empaque"].unique())]

@app.callback(Output("lista3","options"),
              [Input("lista1","value"),
               Input("lista2","value")])

def actualizar_listas3(a_value,b_value):
    df_temp=df
    if a_value:
       df_temp=df_temp[df_temp["Subcategoria"].isin(a_value)]
       
    if b_value:
       df_temp=df_temp[df_temp["Empaque"].isin(b_value)]
    
    return[{"label":x,"value":x} for x in sorted(df_temp["Region"].unique())]
    