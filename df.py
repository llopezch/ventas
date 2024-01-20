import pandas as pd
url_plantilla = 'https://github.com/kont123456/datosventas/raw/master/Plantilla.xlsx'
df=pd.read_excel(url_plantilla,sheet_name="Datos")
df["Año"]=df["Fecha_envio"].dt.year.astype(str)
df["N.MES"]=df["Fecha_envio"].dt.month

url_lat_long = 'https://github.com/kont123456/datosventas/raw/master/lat_long.xlsx'
lat_long = pd.read_excel(url_lat_long)





