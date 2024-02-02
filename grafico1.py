import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.express as px 
from dash.dependencies import Output,Input
from dash import dcc,html,dash_table
from app import app
from df import df
import plotly.graph_objects as go


listas_años=[{"label":x,"value":x}for x in sorted(df["Año"].unique())]
main_config = {
    "hovermode": "x unified",
    "hoverlabel": {
        "bgcolor": "rgba(0,0,0,0.5)",
        "font": {"color": "white"}
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
#------------------
df_max=df.groupby("Año")["Ventas"].sum()
añomax=df_max.idxmax()
añomin=df_max.idxmin()

df_variacion=df.groupby("Año")["Ventas"].sum().reset_index()

df_variacion["variacion"]=(df_variacion["Ventas"].pct_change()*100).round(2)
dfañomax=df_variacion["Año"].max()
dfmax=df_variacion[df_variacion["Año"]==dfañomax]
variacion_vta=dfmax["variacion"].iloc[0]
#------------------
dfumax=df.groupby("Año")["Utilidad"].sum()
utmax=dfumax.idxmax()
utmin=dfumax.idxmin()

uti_variacion=df.groupby("Año")["Utilidad"].sum().reset_index()
uti_variacion["variacion"]=(uti_variacion["Utilidad"].pct_change()*100).round(2)
año_max=uti_variacion["Año"].max()
df_utilidad=uti_variacion[uti_variacion["Año"]==año_max]
var_utilidad=df_utilidad["variacion"].iloc[0]

#------------------
df_envio=df.groupby("Año")["Id"].count()
enviomax=df_envio.idxmax()
enviomin=df_envio.idxmin()
#------------------Resumen de pedidos%
pedidos=df.groupby(["Año","N.MES"])["Id"].nunique().reset_index()
pedidos["%variacion"]=(pedidos["Id"].pct_change()*100).round(2)
dfz=pedidos[(pedidos["Año"]==pedidos["Año"].max())&(pedidos["N.MES"]==pedidos["N.MES"].max())]
pedido_variacion=dfz.iloc[0,3]
#------------------Resumen venta del mes actual
dfagrupada=df.groupby(["Año","N.MES"])["Ventas"].sum().reset_index()
df12=dfagrupada[(dfagrupada["Año"]==dfagrupada["Año"].max())&(dfagrupada["N.MES"]==dfagrupada["N.MES"].max())]
venta_mes=df12.iloc[0,2]
#------------------Resumen num.pdedios mes actual
agrupar_pedidos=df.groupby(["Año","N.MES"])["Id"].nunique().reset_index()
dfnum=agrupar_pedidos[(agrupar_pedidos["Año"]==agrupar_pedidos["Año"].max())&(agrupar_pedidos["N.MES"]==agrupar_pedidos["N.MES"].max())]
pedidoactual=dfnum.iloc[0,2]
#------------------Resumen num.pdedios mes anterior
mesmax=agrupar_pedidos["N.MES"].max()
mesanterior=mesmax-1
dfzx=pedidos[(agrupar_pedidos["Año"]==agrupar_pedidos["Año"].max())&(agrupar_pedidos["N.MES"]==mesanterior)]
pedidoanterior=dfzx.iloc[0,2]
#------------------Categoria mas vendida
dfcat=df.groupby(["Año","N.MES","Categoria"])["Ventas"].sum().reset_index()
dfww=dfcat[(dfcat["Año"]==dfcat["Año"].max())&(dfcat["N.MES"]==dfcat["N.MES"].max())]
catmasvendida=dfww["Ventas"].max()
dfmasvendidad=dfww[dfww["Ventas"]==catmasvendida]
vendiadmascat=dfmasvendidad.iloc[0,2]
#------------------Clientes nuevos
dfordenar=df.sort_values("Fecha_envio")
ordenagrupado=dfordenar.drop_duplicates(subset="Nombre_cliente",keep="first")
cliente_ordenado = ordenagrupado.groupby(["Año","N.MES"]).count().unstack(fill_value=0).stack(future_stack=True).reset_index()[["Año","N.MES","Nombre_cliente"]]

dfxx=cliente_ordenado[(cliente_ordenado["Año"]==cliente_ordenado["Año"].max())&(cliente_ordenado["N.MES"]==cliente_ordenado["N.MES"].max())]
nuevo_mes=dfxx.iloc[0,2]




layout=dbc.Container([
           html.Div([    
           html.Label("Paginas / Ventas totales",style={"font-size":"5px","margin-top":"10px"}),
           html.I(className="fas fa-user-alt",style={"margin-left":"790px","margin-top":"20px"}),
           html.I("Sign Out",style={"margin-left":"8px","margin-top":"20px","font-size":"14px",'font-weight': 'bold'}),
           html.I(className="fas fa-cog",style={"margin-left":"13px","margin-top":"20px"}),
           html.I(className="fas fa-bell",style={"margin-left":"12px","margin-top":"20px"}),
           ],style={"display":"flex"}),
           dbc.Row(
               html.Label("VENTAS TOTALES",style={'font-weight': 'bold',"font-size":"14px"})
           ),
           html.Br(),
           dbc.Row([
                  dbc.Col([
                   
                     dbc.Card([
                             html.Legend("Total Ventas", style={"font-size":"15px","padding-left":"130px","padding-top":"10px"}),
                             html.Label("2000", id="total_ventas", style={"font-size":"24px", "padding-left":"100px",'font-weight':'bold'})
                     ],style={"height": 135,"margin-right":"30px",'border-radius': '15px'}),
                     
                     dbc.Card(
                            html.I(className="fas fa-dollar-sign", style={"margin":"auto", "font-size":"42px", "color":"white"}),
                            style={"maxWidth": 64, "background-color":"red","height": 60,"top":"10px","margin-top":"-160px","margin-left":"10px",'border-radius': '15px'}
                     )
                  ],md=3),      
                 dbc.Col([
                  
                     dbc.Card([
                            html.Legend("Total Utilidad",style={"font-size":"15px","padding-left":"130px","padding-top":"10px"}),
                            html.Label("2000",id="total_utilidad",style={"font-size":"24px", "padding-left":"100px",'font-weight':'bold'})
                    ],style={"height": 135,"margin-right":"30px",'border-radius': '15px'}),
                    dbc.Card(
                            html.I(className="fas fa-university",style={"margin":"auto","font-size":"42px","color":"white"}),
                            style={"maxWidth": 64, "background-color":"black","height": 60,"top":"10px","margin-top":"-160px","margin-left":"10px",'border-radius': '15px'}
                     )
                   ],md=3),
                   
                 
                 
                   dbc.Col([
                        dbc.Card([
                            html.Legend("Total costo Envio",style={"font-size":"15px","padding-left":"105px","padding-top":"10px"}),
                            html.Label("2000",id="costo_envio",style={"font-size":"23px", "padding-left":"115px",'font-weight':'bold'})
                        ],style={"height": 135,"margin-right":"30px",'border-radius': '15px'}),
                        dbc.Card(
                            html.I(className="fas fa-truck",style={"margin":"auto","font-size":"42px","color":"white"}),
                            style={"maxWidth": 64, "background-color":"green","height": 60,"top":"10px","margin-top":"-160px","margin-left":"10px",'border-radius': '15px'}
                        )
                   ],md=3),
                 
                   dbc.Col([
                        dbc.Card([
                            html.Legend("Total Descuento",style={"font-size":"15px","padding-left":"105px","padding-top":"10px"}),
                            html.Label("2000",id="total_descuento",style={"font-size":"24px", "padding-left":"140px",'font-weight':'bold'})
                        ],style={"height": 135,"margin-right":"30px",'border-radius': '15px'}),
                        dbc.Card(
                            html.I(className="fas fa-money-check-alt",style={"margin":"auto","font-size":"42px","color":"white"}),
                            style={"maxWidth": 64, "background-color":"Purple","height": 60,"top":"10px","margin-top":"-160px","margin-left":"10px",'border-radius': '15px'}
                        )
                   ],md=3),
            ]),
           
            dbc.Row([
               dbc.Col([
                   dbc.Card([
                       html.Legend("Total Ventas",style={"padding-top": "205px","padding-left":"30px","font-size":"17px",'font-weight':'bold'}),
                       html.P( f"Año con Mayor Venta : {añomax} ",style={"padding-left":"30px","font-size":"14px"}),
                       html.P( f"Año con Menor Venta : {añomin} ",style={"padding-left":"30px","margin-top":"-14px","font-size":"14px"}),
                       html.P(F"Var % de Año actual vs Año anterior : {variacion_vta} %",style={"padding-left":"30px","margin-top":"-14px","font-size":"14px"})
                   ],style={"margin-top":"40px","height":340,'border-radius': '15px'}), 
                   dbc.Card(
                      dcc.Graph(id="ventas_por_año",style={"height":240}),
                      style={"width": "90%","margin-top":"-390px","margin-left":"20px",'border-radius': '25px'}  
                   )   
                 ],md=4),
               
                dbc.Col([        
                   dbc.Card([
                       html.Legend("Total Utilidad",style={"padding-top": "205px","padding-left":"30px","font-size":"17px",'font-weight':'bold'}),
                       html.P(f"Año con Mayor Utilidad : {utmax}",style={"padding-left":"30px","font-size":"14px"}),
                       html.P(f"Año con Menor Utilidad : {utmin}",style={"padding-left":"30px","margin-top":"-14px","font-size":"14px"}),
                       html.P(F"Var % de Año actual vs Año anterior : {var_utilidad} %",style={"padding-left":"30px","margin-top":"-14px","font-size":"14px"})   
                       
                   ],style={"margin-top":"40px","height":340,'border-radius': '15px'}),  
                   dbc.Card(     
                      dcc.Graph(id="utilidad_año",style={"height":240}),
                       style={"width": "90%","margin-top":"-390px","margin-left":"20px",'border-radius': '25px'}
                   )  
               ],md=4),
               dbc.Col([
                    dbc.Card([
                       html.Legend("Total Envio",style={"padding-top": "205px","padding-left":"30px","font-size":"17px",'font-weight':'bold'}),
                       html.P(f"Año con Mayor Envio : {enviomax}",style={"padding-left":"30px","font-size":"14px"}),
                       html.P(f"Año con Menor Envio : {enviomin}",style={"padding-left":"30px","margin-top":"-14px","font-size":"14px"})
                       
                    ],style={"margin-top":"40px","height":340,'border-radius': '15px'}),  
                    dbc.Card( 
                        dcc.Graph(id="envios_año",style={"height":240}),
                        style={"width": "90%","margin-top":"-390px","margin-left":"20px",'border-radius': '25px'}
                    )
               ],md=4)
               
           ],style={"margin-top":"135px"}),
           
          
              dbc.Row([
                 dbc.Col([
                     dbc.Card([
                        html.Legend(""),
                        html.Div(id="tabla-agrupada", className="dbc",style={"margin":"12px"}),
                     ])
                 ],md=8),
                 dbc.Col([
                     dbc.Card([
                          html.Div([
                          html.I(className="fas fa-tags",style={"font-size":"25px","color":"red","padding-left":"24px"}),
                          html.Legend("Resumen de pedidos",style={"font-size":"17px",'font-weight':'bold',"padding-left":"18px"}),
                         ],style={"display":"flex","margin-top":"25px"}) ,
                          html.Label(f" {pedido_variacion} % este mes" ,style={"font-size":"14px","padding-left":"75px"}),
                          html.Div([
                          html.I(className="fas fa-bell",style={"font-size":"25px","color":"green","padding-left":"24px"}),
                          html.Legend("Venta total actual",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label(f"{venta_mes:,.2f} este mes",style={"font-size":"14px","padding-left":"75px"}),
                          html.Div([
                          html.I(className="fas fa-cart-arrow-down",style={"font-size":"25px","color":"blue","padding-left":"24px"}),
                          html.Legend("Resumen Cantidad de pedidos",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label(f"{pedidoactual} este mes",style={"font-size":"14px","padding-left":"75px"}),
                          html.Div([
                          html.I(className="fas fa-cart-arrow-down",style={"font-size":"25px","color":"blue","padding-left":"24px"}),
                          html.Legend("Resumen Cantidad de pedidos",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label(f"{pedidoanterior} mes anterior",style={"font-size":"14px","padding-left":"75px"}),
                          html.Div([
                          html.I(className="fas fa-credit-card",style={"font-size":"25px","color":"black","padding-left":"24px"}),
                          html.Legend("Nuevo N° Cta agregada",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label("Banco Santander: 0049-1500-05-1234567892",style={"font-size":"14px","padding-left":"75px"}),
                        
                          html.Div([
                          html.I(className="fas fa-chart-line",style={"font-size":"25px","color":"red","padding-left":"24px"}),
                          html.Legend("Categoria mas Vendida",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label(f"({vendiadmascat}) este mes",style={"font-size":"14px","padding-left":"75px"}),
                          
                          html.Div([
                          html.I(className="fas fa-user-plus",style={"font-size":"25px","color":"green","padding-left":"24px"}),
                          html.Legend("# Clientes Nuevos",style={"font-size":"17px",'font-weight':'bold',"padding-left":"25px"}),
                         ],style={"display":"flex","margin-top":"30px"}),
                          html.Label(f"{nuevo_mes} este mes",style={"font-size":"14px","padding-left":"75px"}),
                     ],style={"height":"670px"})
                 ])
                     
              ],style={"margin-top":"175px"}),
          
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

def formatear_numero(num):
    if num >= 1000000000:
        return 'S/' + '{:,.0f}'.format(num/1000000000) + 'B'
    elif num >= 1000000:
        return 'S/' + '{:,.0f}'.format(num/1000) + 'M'
    else:
        return 'S/' + '{:,}'.format(round(num))

@app.callback([Output("total_ventas","children"),
               Output("total_utilidad","children"),             
               Output("costo_envio","children"),
               Output("total_descuento","children"),
               Output("ventas_por_año","figure"),
               Output("utilidad_año","figure"),
               Output("envios_año","figure"),
               Output('tabla-agrupada', 'children')],             
              [Input("lista1","value"),
               Input("lista2","value"),
               Input("lista3","value")]) 



def actualizar_datos(value1,value2,value3):
    
    df_temp=df.copy()
    if value1:
        df_temp=df_temp[df_temp["Subcategoria"].isin(value1)]
    
    if value2:
        df_temp=df_temp[df_temp["Empaque"].isin(value2)]
    
    if value3:
        df_temp=df_temp[df_temp["Region"].isin(value3)]
        
    
    
    total_ventas = formatear_numero(df_temp["Ventas"].sum())
    total_utilidad = formatear_numero(df_temp["Utilidad"].sum())
    total_costo_emvio = formatear_numero(df_temp["Costo_envio"].sum())
    total_descuento = formatear_numero(df_temp["Descuento"].sum())
    
    #-------------------------------------------------------------
    #------------------aca estan los hovertemplate para ventanas emergentes
    ventas_anual=df_temp.groupby("Año")["Ventas"].sum().reset_index()
    ventas_anual["Porcentaje"]=(ventas_anual["Ventas"].pct_change()*100).round(2)
    
    dropdown_lista={"Producto":value1,"Empaque":value2,"Pais":value3}
    hovertemplate="%{y:,.2f}<br>"+"".join([f'<b style="color:lime;">{key}:</b><br>{"-".join(map(str,val))}<br>'for key ,val in dropdown_lista.items()if val])
    hovertemplate1="Año: %{label}<br>Cantidad de Envios : %{value}<br>"+"".join([f'<b style="color:lime;">{key}:</b><br>{"-".join(map(str,val))}<br>'for key ,val in dropdown_lista.items()if val])
    
    #------------------
   
    fig_vts_anual=go.Figure()
    fig_vts_anual.add_trace(go.Bar(x=ventas_anual["Año"],y=ventas_anual["Ventas"],name="Ventas",hovertemplate=hovertemplate,marker=dict(color='rgb(255,255,255)')))
    fig_vts_anual.update_layout(yaxis2=dict(overlaying="y",side="right"))
    fig_vts_anual.add_trace(go.Scatter(x=ventas_anual["Año"],y=ventas_anual["Porcentaje"], mode='lines+markers', yaxis='y2',name='Variación %'))
    fig_vts_anual.update_layout(main_config,plot_bgcolor='#62A26E',paper_bgcolor='#62A26E')
    fig_vts_anual.update_layout(showlegend=False)
    fig_vts_anual.update_yaxes(showgrid=False) 
    
    # Cambiar el color de los valores de los ejes x e y a blanco
    fig_vts_anual.update_xaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje x
    fig_vts_anual.update_yaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje y

    
    utilidad_año=df_temp.groupby("Año")["Utilidad"].sum().reset_index()
    utilidad_año["Porcentaje"]=(utilidad_año["Utilidad"].pct_change()*100).round(2)
    
    fid_utilidad_año=go.Figure()
    fid_utilidad_año.add_trace(go.Bar(x=utilidad_año["Año"],y=utilidad_año["Utilidad"],name="Utilidad de Ventas",hovertemplate=hovertemplate,marker=dict(color='rgb(255,255,255)')))
    fid_utilidad_año.update_layout(yaxis2=dict(overlaying="y",side="right"))
    fid_utilidad_año.add_trace(go.Scatter(x=utilidad_año["Año"],y=utilidad_año["Porcentaje"],name="variacion %",yaxis="y2",mode="lines+markers"))
    fid_utilidad_año.update_layout(main_config,plot_bgcolor='#E7106F',paper_bgcolor='#E7106F')
    fid_utilidad_año.update_layout(showlegend=False)
    fid_utilidad_año.update_yaxes(showgrid=False) 
    # Cambiar el color de los valores de los ejes x e y a blanco
    fid_utilidad_año.update_xaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje x
    fid_utilidad_año.update_yaxes(tickfont=dict(color='rgb(255,255,255)'))  # Color blanco para los valores del eje y

    
  
    
    cantenvios_año=df_temp.groupby("Año")["Id"].count().reset_index()
    total_id = cantenvios_año["Id"].sum()
    fig_envio_año=go.Figure()
    fig_envio_año.add_trace(go.Pie(labels=cantenvios_año["Año"],values=cantenvios_año["Id"],hole=0.9,name="",hovertemplate=hovertemplate1,textfont=dict(color='white')))
    fig_envio_año.update_layout(main_config,plot_bgcolor='#060606',paper_bgcolor='#060606')
    # Agrega una anotación con la suma total al centro del gráfico y texto
    fig_envio_año.update_layout(
    annotations=[
        dict(text=str(total_id), x=0.5, y=0.55, font_size=25, showarrow=False, font=dict(color='white')),
        
        dict(text='Cantidad Total', x=0.5, y=0.45, font_size=12, showarrow=False,font=dict(color='white'))
    ],showlegend=False)
    
    df_tabla=df_temp.groupby(["Categoria","Subcategoria"])[["Cantidad","Ventas","Utilidad"]].sum().reset_index()
    
    # Luego, puedes crear la tabla utilizando este DataFrame agrupado:
    tabla_agrupada = dash_table.DataTable(
                     id='datatable-agrupada',
                     columns=[
                              {"name": "Categoria", "id": "Categoria", "deletable": False, "selectable": False},
                              {"name": "Subcategoria", "id": "Subcategoria", "deletable": False, "selectable": False},
                              {"name": "Ventas", "id": "Ventas", "deletable": False, "selectable": False,'type': 'numeric'},
                              {"name": "Utilidad", "id": "Utilidad", "deletable": False, "selectable": False,'type': 'numeric'},
                              {"name": "Cantidad", "id": "Cantidad", "deletable": False, "selectable": False,'type': 'numeric'}
                     ],
                     data=df_tabla.to_dict('records'),
                     filter_action="native",
                     sort_action="native",
                     sort_mode="single",
                     selected_columns=[],
                     selected_rows=[],
                     page_action="native",
                     page_current=0,
                     page_size=10,
                     style_cell={  # Estilo de las celdas
                                'border': 'none','padding-bottom': '28px', # Elimina las líneas divisorias
                                 'text-align': 'center',# Centra los valores de las celdas 
                                 
                     },
                           
                     
                     style_header={  # Estilo de los encabezados
                                     'text-align': 'center',  # Centra los títulos de las columnas
                    },
                     
                     row_selectable='single'  # Permite seleccionar una fila completa al hacer clic en un valor interno de la tabla
                     
                    )
    
    
    return (
        total_ventas,
        total_utilidad,
        total_costo_emvio,
        total_descuento,
        fig_vts_anual,
        fid_utilidad_año,
        fig_envio_año,
        tabla_agrupada

     )
    




 