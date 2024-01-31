import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.express as px 
from dash.dependencies import Output,Input,State
from dash import dcc,html,dash_table
from app import app
from df import df,lat_long
import plotly.graph_objects as go
from actualizaciones import filter_commits, get_commit_history
from dash.exceptions import PreventUpdate

github_token = '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'


listas_años=[{"label":x,"value":x}for x in sorted(df["Año"].unique())]
main_config = {
    "hovermode": "x unified",
    "hoverlabel": {
        "bgcolor": "rgba(0,0,0,0.5)",
        "font": {"color": "white","size": 12}
    },
    "legend": {
        "yanchor":"top", 
        "y":0.9, 
        "xanchor":"left",
        "x":0.1,
        "title": {"text": None},
        "font" :{"color":"white"},
        "bgcolor": "rgba(0,0,0,0.5)"
    },
    "margin": {"l":30, "r":30, "t":30, "b":30}
}

meses_espanol = {
    1: 'Ene',
    2: 'Feb',
    3: 'Mar',
    4: 'Abr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Ago',
    9: 'Sept',
    10: 'Oct',
    11: 'Nov',
    12: 'Dic'
}


layout=dbc.Container([
           html.Div([  
           html.Label("Paginas / Ventas Paises",style={"font-size":"14px","margin-top":"10px"}),
           html.I(className="fas fa-user-alt",style={"margin-left":"815px","margin-top":"20px"}),
           html.I("Sign Out",style={"margin-left":"8px","margin-top":"20px","font-size":"14px",'font-weight': 'bold'}),
           html.I(className="fas fa-cog",style={"margin-left":"13px","margin-top":"20px"}),
           dbc.Button(children=[html.I(className="fas fa-bell",style={"font-size":"20px","margin-top":"5px"})],id="popover-target",color="link"),
           dbc.Popover(
            [
                dbc.PopoverHeader("Historial"),
                dbc.PopoverBody(
                    [
                        html.Table(
                            # Estructura de la tabla con la información del historial
                            # Mostrar solo la columna 'Fecha'
                            [html.Tr([html.Th('Fecha'), html.Th('Hora')])] +
                            [html.Tr([
                                html.Td(commit['fecha'],style={'font-weight': 'bold'}),
                                html.Td(commit['hora'], style={'color': 'blue'})
                             ]) for commit in filter_commits(get_commit_history())]
                        ),
                        dbc.Button("Cerrar", id="cerrar-btn", color="danger", className="mt-2",size="sm"),
                    ]
                ),
            ],
            id="popover",
            is_open=False,
            target="popover-target",
            ),
            dcc.Interval(
            id='interval-component',
            interval=10*1000,  # en milisegundos, actualizar cada 10 segundos
            n_intervals=0
            ),
           
           
            ],style={"display":"flex"}),
          
           
           dbc.Row(
                    html.Label("VENTAS PAISES",style={'font-weight': 'bold',"font-size":"14px"})
           ),
           dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dcc.Dropdown(id="lit_años",
                                     multi=True,
                                     clearable= False,
                                     persistence=True,
                                     options=listas_años,
                                     value=[df["Año"].max()],
                                     style={"font-size":"13px","width": "153px","margin-left":"8px"}
                                     ) ,
                        
                        dcc.Checklist(id="uti_vent",
                                     options=[{"label":"Ventas","value":"Ventas"},
                                               {"label":"Utilidad","value":"Utilidad"}] ,
                                     value=[ "Ventas", "Utilidad"],
                                     labelStyle={"display":"inline-block","font-size":"13px","margin-left":"15px","margin-top":"15px"}
                                     ),
                       html.Div([
                            html.I(className="fas fa-chart-line",style={"font-size":"32px","color":"red","padding-left":"14px","margin-top":"30px"}),
                            html.Legend("Total",style={"font-size":"13px","padding-left":"10px"})
                       ],style={"display":"flex"}) ,
                            html.Label(id="numventas",style={"font-size":"12px",'font-weight':'bold',"padding-left":"60px","position":"relative","top":"-45px","color":"green"}),
                            html.Label(id="numutilidad",style={"font-size":"12px",'font-weight':'bold',"padding-left":"60px","position":"relative","top":"-45px","color":"green"})       
                    ],md=2),
                    dbc.Col([
                            dcc.Graph(id="graficos_lineas" )
                    ],md=10)
                ])
            ],style={"margin-top":"15px","height":220}),
           dbc.Card([
               dbc.Row([
                   dbc.Col([
                       html.Div([
                           html.I(className="fas fa-globe-americas",style={"font-size":"32px","color":"green","padding-left":"14px","margin-top":"10px"}),
                           html.Legend("Ventas por Pais",style={"font-size":"16px","padding-left":"10px","margin-top":"12px",'font-weight':'bold'})  
                       ],style={"display":"flex"}),                  
                   ],md=4),
                   dbc.Col([
                       dcc.Dropdown(id="lista_añitos",
                                   persistence=True,
                                   persistence_type="session",
                                   clearable=False,
                                  
                                   options=listas_años,
                                   style={"width": "70%","font-size":"13px","margin-left":"-100px","margin-top":"8px"},
                                   value=df["Año"].max()
                                   )
                  ],md=2),
                dbc.Row([
                    dbc.Col([
                    html.Div(id="formato",className="dbc")
                    ],md=3),
                    dbc.Col([
                       dcc.Graph(id="formato_mapa",style={"margin-left": "210px","margin-top":"-40px"}),  # Nuevo Div para el mapa
                       dcc.Store(id='relayout-store', storage_type='session')  # Almacena los datos de diseño del mapa
                    ], md=9),
                    
                ])   
              ])
           ],style={"margin-top":"25px","height":"430px"} ),
           html.Br(),  
           html.Br(),  
           html.Div([ 
                 
                  html.I("Copyright © 2024,made with by Creative ",style={"font-size":"17px",'color': '#787878','font-family': 'Times New Roman',"padding-left":"20px"}),
                  html.I("  Luis Lopez & DASH-PLOTLY ",style={"font-size":"17px",'font-family': 'Times New Roman','font-weight': 'bold' }),
                  html.I("  for a better web.",style={"font-size":"17px",'color': '#787878','font-family': 'Times New Roman'}),
           ],style={"display":"flex"}),
            html.Br(),
            html.Br(),
            
           
])


@app.callback([Output("graficos_lineas","figure"),
               Output('numventas', 'children'),
               Output('numutilidad', 'children')],
               [Input("lista1","value"),
               Input("lista2","value"),
               Input("lista3","value"),
               Input("lit_años","value"),
               Input("uti_vent","value")]
              ) 


def actualizar_lineas(value1,value2,value3,value4,value5):
     df_temp=df.copy()
   
    
     if value1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value1)]
    
     if value2:
        df_temp=df_temp[df_temp["Empaque"].isin(value2)]
    
     if value3:
        df_temp=df_temp[df_temp["Region"].isin(value3)]
        
    
     df_goles=df_temp[df_temp["Año"].isin(value4)]
     
     numventas=df_goles["Ventas"].sum()
     numutilidad=df_goles["Utilidad"].sum()
      

     df_temp["Mes"] = df_temp["Fecha_envio"].dt.month.map(meses_espanol)
     df_temp=df_temp.groupby(["Año","Mes","N.MES"])[["Ventas","Utilidad"]].sum().reset_index()
     df_temp=df_temp.sort_values(by=["Año","Mes"])
     
     fig_venta_utilidad=go.Figure()
     for valores in  value5:
          for año in value4:
             df_año=df_temp[(df_temp["Año"]==año)].groupby(["Mes","N.MES"])[valores].sum().reset_index()
             df_año = df_año.sort_values(by="N.MES")
                                                                                                               # name solo sirve si usas leyendas pone valores atus leyendas
             fig_venta_utilidad.add_trace(go.Scatter(x=df_año["Mes"],y=df_año[valores],mode='lines+markers', name=f'{valores}-{año}',line_shape='spline')) 
    
     fig_venta_utilidad.update_layout(title=f"{'-'.join(value5)} {'-'.join(value4)}")
     fig_venta_utilidad.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=220,width=920,title_y=0.95, plot_bgcolor='white',)
     fig_venta_utilidad.update_layout({"legend": {"yanchor": "top", "y":0.99}}) 
     fig_venta_utilidad.update_layout(showlegend=False) 
     
     
     
     
     
     return fig_venta_utilidad,f"Ventas::{numventas:,.2f}",f"Utilidad:{numutilidad :,.2f}"
 
@app.callback(
    Output('relayout-store', 'data'),
    Input('formato_mapa', 'relayoutData'),
    State('relayout-store', 'data')
)
def store_relayout_data(relayoutData, stored_data):
    if relayoutData and ('mapbox.center' in relayoutData or 'mapbox.zoom' in relayoutData):
        stored_data = stored_data or {}
        stored_data.update(relayoutData)
    return stored_data

@app.callback([Output("formato","children"),
               Output("formato_mapa", "figure")],
              [Input("lista_añitos","value"),
               Input('relayout-store', 'data')]
              )
def actualizar_formato(value_a,stored_data):
   
   dfx=df.copy() 
   df_agrupada=dfx.groupby(["Region","Año"])["Ventas"].sum().reset_index()
   
   df_agrupada['var%'] = (df_agrupada.groupby('Region')['Ventas'].pct_change() * 100).round(2)
   df_agrupada['var%'] =df_agrupada["var%"].fillna(0)
   
   df_agrupada["año anterior var%"]=df_agrupada["var%"].apply(lambda x: 
    
    '🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥' if x <= -91 else
    '🟥🟥🟥🟥🟥🟥🟥🟥🟥⬜' if x <= -81 else
    '🟥🟥🟥🟥🟥🟥🟥🟥⬜⬜' if x <= -71 else
    '🟥🟥🟥🟥🟥🟥🟥⬜⬜⬜' if x <= -61 else
    '🟥🟥🟥🟥🟥🟥⬜⬜⬜⬜' if x <= -51 else
    '🟥🟥🟥🟥🟥⬜⬜⬜⬜⬜' if x <= -41 else
    '🟥🟥🟥🟥⬜⬜⬜⬜⬜⬜' if x <= -31 else
    '🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜' if x <= -21 else
    '🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜' if x <= -11 else
    '🟥⬜⬜⬜⬜⬜⬜⬜⬜⬜' if x <   -0.01 else
    '🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜' if x <   11 else
    '🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜' if x <   21 else
    '🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜' if x <   31 else
    '🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜' if x <   41 else
    '🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜' if x <   51 else
    '🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜' if x <   61 else
    '🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜' if x <   71 else
    '🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜' if x <   81 else
    '🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜' if x <   91 else
    '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩'
     )	
   dfx_tabla=df_agrupada[df_agrupada["Año"]==value_a][["Region","Ventas","var%","año anterior var%"]]    
   dfx_tabla['Ventas'] = dfx_tabla['Ventas'].round(2)
  
   dfx_tabla['var%'] = dfx_tabla['var%'].apply(lambda x: str(x) + '%')
   tabla_formato = dash_table.DataTable(
                    data=dfx_tabla.to_dict('records'),
                    columns=[
                             {"name": i, "id": i} for i in dfx_tabla.columns
                            ],
                    style_cell_conditional=[
                              {'if': {'column_id': 'año anterior var%'},
                                 'width': '50px'},
                              {'if': {'column_id': 'Region'},
                                     'textAlign': 'center','font-weight': 'bold'},
                              {'if': {'column_id': 'Ventas'},
                                    'textAlign': 'center'},          
                    ],
                    style_header_conditional=[
                                                {'if': {'column_id': 'var%'},
                                                'color': 'white'},
                    ],
                    style_header={
                                   'textAlign': 'center',
                                   'border': '0px solid white',
                                  },
                    style_cell={
                                 'border': '0px solid white',
                                },
                    style_data={
                                'height': '50px',  # Ajusta este valor según tus necesidades
                               },
                   )
   
   # Crear el mapa interactivo
   dfmap=dfx_tabla[["Region","Ventas"]].copy()
   df_mapa = pd.merge(dfmap, lat_long, left_on='Region', right_on='name', how='left')

   
   fig_mapa = px.scatter_mapbox(
        df_mapa,
        lon='longitude',
        lat='latitude',
        zoom=0.5,
        size='Ventas',
        size_max=25,
        color='Region',
        
        opacity=0.7,
        height=650,
        hover_data=['Ventas', 'Region'],
        color_discrete_sequence=px.colors.qualitative.G10,
        mapbox_style="carto-positron",
        hover_name=df_mapa['Region'],
        title='Ventas por País'
    )
   # Configurar el diseño
   fig_mapa.update_layout( 
     width=640,  # Establece el ancho deseado
     height=420,  # Establece la altura deseada                    
     margin=dict(l=0, r=0, b=0, t=0),  # Reducir los márgenes para maximizar el espacio
     showlegend=False  # Ocultar la leyenda
   )
   
   # Cambiar la capa base a "light_all" o "positron"
   

   if stored_data:
        if 'mapbox.zoom' in stored_data:
            fig_mapa['layout']['mapbox']['zoom'] = stored_data['mapbox.zoom']
        if 'mapbox.center' in stored_data:
            fig_mapa['layout']['mapbox']['center'] = stored_data['mapbox.center']
   
    # Eliminar etiquetas de país
   

   available_styles = px.colors.named_colorscales()

   
  
   return tabla_formato,fig_mapa

# Callback para actualizar el popover con el historial
@app.callback(
    [Output('popover', 'is_open'),
     Output('popover-target', 'n_clicks')],
    [Input('popover-target', 'n_clicks'),
     Input('cerrar-btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_popover(historial_btn, cerrar_btn):
    ctx = dash.callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    if 'popover-target' in ctx.triggered_id:
        is_open = True
    else:
        is_open = False

    return is_open, 0



