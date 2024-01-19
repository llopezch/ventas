import pandas as pd
df=pd.read_excel("C:\\Users\\luis\\Desktop\\PYTHOM PROGRAMAS\\PRACTICA.PY\\parcticas2\\Plantilla.xlsx",sheet_name="Datos")
df["Año"]=df["Fecha_envio"].dt.year.astype(str)
df["N.MES"]=df["Fecha_envio"].dt.month

lat_long=pd.read_excel("C:\\Users\\luis\\Desktop\\PYTHOM PROGRAMAS\\PRACTICA.PY\\parcticas2\\lat_long.xlsx")
