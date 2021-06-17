# %%
# importar librerias de analisis y visualización
import pandas as pd
import matplotlib.pyplot as plt
import folium
#import numpy as np
#import calmap
#import seaborn as sns
#import datetime

# -------------------------------------------------------------------
# Default config | insert code here
# -------------------------------------------------------------------
# put the default path here
path_ = "E:/PROGRAMACION/PYTHON/PROYECTOS_PYTHON/ANALISIS_DATOS/"

# put here last date from new data for instance "2021-09-23"
end_date_in = "2020-10-17"  # default "2020-10-17"

# if you change the start date for any reason put it here
start_date_in = "2020-01-22"  # default "2020-01-22"

# if you want to change the default country put ir here
country_in = "Colombia"  # default Colombia
# -------------------------------------------------------------------

print("""        ********************************************************
        +                                                      +
        +    Script para visualización de datos de Covid-19    +
        +                      COVIS 1.0                       +
        +                                                      +
        ********************************************************\n""")

# -------------------------------------------------------------------
# File type config | insert code here
# -------------------------------------------------------------------
try:
    path = input("Selecciona la ruta o ENTER para ruta default: ")
    # CARGAR ARCHIVO active para habilitar diferente formato
    # df = pd.read_csv(f'{path}COVIS/input/Covid_confirmed.csv', delimiter=';') # csv
    df = pd.read_excel(f'{path}COVIS/input/Covid_template.xlsx')  # xlsx
    print("Ruta cargada leyendo datoos...\n")
except:
    path = path_
    # CARGAR ARCHIVO
    # df = pd.read_csv(f'{path}COVIS/input/Covid_confirmed.csv', delimiter=';') # csv
    df = pd.read_excel(f'{path}COVIS/input/Covid_template.xlsx')  # xlsx
    print("Ruta default cargada leyendo datoos...\n")

# -------------------------------------------------------------------

print(">>> Cargando datos...\n")

print(">>> Creando dataframe global...\n")

# muestra el dataframe original cargado
with pd.option_context('display.max_rows', 5, 'display.max_columns', 5):
    print(df)

# crear copia de dataframe para trabajar sin dañar el original
copy_df = df.copy()

print("\n>>> Creando dataframe casos mensuales por pais...")

# creando nuevas columnas para visualizcion en GDS
# cambiar valores nulos a str
copy_df.fillna("", inplace=True)

# creando columna para regiones en GDS
copy_df["Region"] = copy_df["Province/State"] + " " + copy_df["Country/Region"]

# creando columna para coordenadas en GDS
copy_df["lat_long"] = copy_df["Lat"].astype(
    str) + "," + copy_df["Long"].astype(str)

# reeordenar columnas del df para mejor visualización
cols_2 = copy_df.columns.to_list()
cols_2 = cols_2[0:4] + cols_2[-2:] + cols_2[4:-2]
df_completo = copy_df[cols_2]

# almacenar data de casos por fecha
casos = df_completo.iloc[:, 6:]

# crear nuevos dataframe para graficas
casos_pais = pd.concat([df_completo["Country/Region"], casos], axis=1)
casos_regiones = pd.concat([df_completo["Region"], casos], axis=1)
casos_coord = pd.concat([df_completo["lat_long"], casos], axis=1)

# cambiar  index de dataframe
tem_regiones = casos_regiones.set_index('Region')
tem_regiones.rename_axis(index=None, inplace=True)

# cambiar  index de dataframe
tem_coord = casos_coord.set_index('lat_long')
tem_coord.rename_axis(index=None, inplace=True)

# sumar los datos por regiones para encontrar el total por paises
tem_pais = casos_pais.groupby(["Country/Region"]).sum()
# eliminar nombre del index del df
tem_pais.rename_axis(index=None, inplace=True)

# transponer df para tener fechas en columnas
tem_pais_t = tem_pais.T
tem_regiones_t = tem_regiones.T
tem_coord_t = tem_coord.T

# lista para ciclos
list_tem_t = [tem_pais_t, tem_regiones_t, tem_coord_t]

# asignar nombre al index del df
for item in list_tem_t:
    item.rename_axis(index="index", inplace=True)

# crear nuevo indice para el dataframe y pasar la columna de date a valores
for item in list_tem_t:
    item["date"] = item.index

# crear copia de columna date para mappear meses
tem_pais_t['months'] = tem_pais_t['date']

# cambiar tipo de dato de la columna date
for item in list_tem_t:
    item['date'] = pd.to_datetime(item['date'])

# hasta aca estan listos los datos para crear cada una de las distintas graficas solicitadas, de este punto en adelante se mostrara la creacion de cada codigo

# 2. crear df para gráfica de casos acumulados de covid por meses por país

# reeordenar columnas del df para mejor visualización
cols = tem_pais_t.columns.to_list()
cols = cols[-2:] + cols[:-2]
tem_pais_t = tem_pais_t[cols]

# lista de paies del df
pais_list = tem_pais_t.columns.to_list()
pais_list = pais_list[2:]

# almacenando datos en diccionarios para crear dataframe
dict_pais = {}
for pais in pais_list:
    pais_sort = tem_pais_t[["date", "months", pais]]
    pais_sort_ = pais_sort.rename(columns={pais: 'casos/dia'})
    pais_sort_["Country/Region"] = pais
    pais_sort_.index = pais_sort_["date"]

    dict_pais[pais] = dict_pais.get(pais, pais_sort_)

# reduciendo datos de fechas para valores acumulados
list_country = []
for key, values in dict_pais.items():
    values_ = values.resample('M').max()

    list_country.append(values_)

# creado nuevo dataframe
final_df_meses = list_country[0].append(list_country[1:])
final_df_meses.rename_axis(index="index", inplace=True)


# creando columna meses para cada fecha en el dataframe
arr_tem = final_df_meses["months"].unique()
arr_tem.tolist().sort()
limiter = len(arr_tem)

# meses del año a mappear
'''meses = ["Enero","Febrero", "Marzo", 
        "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre",
        "Octubre", "noviembre", "Diciembre"]
'''

# el valor de los meses debe ser numerico para que lo carge GoogleDataStudio
meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


# creamos un diccionario para mappear los valores de los meses a reemplazar
map_meses = {}
for key, values in zip(arr_tem, meses[0:limiter]):
    map_meses[key] = map_meses.get(key, values)

# reemplzamos meses en el dataframe
final_df_meses.months.replace(map_meses, inplace=True)

print(">>> Dataframe de casos mensuales creado \n")

# muestra el dataframe original cargado
with pd.option_context('display.max_rows', 5, 'display.max_columns', 5):
    print(final_df_meses)

print(">>> Guardando datos...")

# exportamos el data frame paravisualizarlo fuera de python meses
final_df_meses.to_csv(
    fr'{path_}COVIS\output\monthcases_CV19_by_country_2020.csv')

final_df_meses.to_excel(
    fr'{path_}COVIS\output\monthcases_CV19_by_country_2020.xlsx')

print(">>> Datos de casos mensuales por país guardados\n")

# %%
# ------------------------------------------------------------------
# 3. Crear dataframe para vizualizar casos de covid por días y regiones

# definir funcion para crear data frame a partir de una columna especifica
print(">>> Creando dataframe casos diarios por país")


def col_to_df(df_col):

    # lista de elementos en el df
    col_list = df_col.columns.to_list()
    list_col = col_list[:-1]
    list_df = []

    # almacenando datos en diccionarios para crear dataframe
    for item in list_col:
        # indexador
        ind = list_col.index(item)
        list_sort = df_col.iloc[:, [-1, ind]]
        list_sort_2 = list_sort.rename(columns={item: "casos/dia"})
        list_sort_2["default"] = item
        list_sort_2.index = list_sort_2["date"]
        list_df.append(list_sort_2)

    # creado nuevo dataframe casos por día
    final_df = list_df[0].append(list_df[1:])
    final_df.rename_axis(index="index", inplace=True)

    return final_df


# llamamos a la funcion para crear el cada df que necesitemos
regiones_df = col_to_df(tem_regiones_t)
coordenadas_df = col_to_df(tem_coord_t)

# cambiar nombre columna default
regiones_df.rename(columns={'default': 'region'}, inplace=True)
coordenadas_df.rename(columns={'default': 'Lat/long'}, inplace=True)

# ordenar dataframe
drop_reg = regiones_df.drop(["date", "casos/dia"], axis=1)
frames = [drop_reg, coordenadas_df]

full_dias_df = pd.concat(frames, axis=1)

print(">>> Dataframe de casos diarios por país creados\n")

# muestra el dataframe original cargado
with pd.option_context('display.max_rows', 5, 'display.max_columns', 5):
    print(full_dias_df)

print(">>> Guardando casos diarios por país ...")

# exportamos el data frame paravisualizarlo fuera de python dias
full_dias_df.to_csv(
    fr'{path_}COVIS\output\dailycases_CV19_by_country_large.csv')

full_dias_df.to_excel(
    fr'{path_}COVIS\output\dailycases_CV19_by_country_large.xlsx')

print(">>> Datos de casos diarios por país guardados\n")

# ----------------------------------------------------------------
# %%
# # 4. Crear dataframe para ver casos totales por país

# variables para ingreso de datos de usuario
cols_2 = df_completo.columns.to_list()
list_user = df_completo["Country/Region"].unique()
size_list = len(list_user)

print("-"*30)
print("\nGRAFICA DE CASOS DIARIOS POR PAIS")
print(f"""\nSi desea cambiar la fecha y el país de la gráfica de casos diarios, inroduzca un numero para selecionar fecha y el nombre del país:
    -> Fechas entre 6-{len(cols_2)}, 6-> {cols_2[6]} {len(cols_2)}-> {cols_2[-1]}
    -> Nombre país, Ejem: Colombia\n""")

print(
    f"¿Desea ver la lista de paises almacenados?, hay {size_list} paises en la lista.\n")

try:
    answer = str(input("Y/N o enter para default:")).upper()
    if answer == "Y":
        print(list_user)
    else:
        print("No se mostrará la lista de paises\n")
except:
    print("Default cargado\n")

print("\n>>> Ingrese datos de fecha y pais, o enter para cargar default: ")

try:
    # determina fecha de grafica
    date_g = int(input(f"Fechas (6-{len(cols_2)}): "))
    country_ = str(input("Nombre pais (Colombia): ")).capitalize()
    tester_var = tem_pais_t[country_]
    print(country_, date_g)
    print("\nDatos cargados\n")
except:
    print("**Valores errones, se cargarán datos defualt \n")
    date_g = -1  # -1 last date
    country_ = country_in
    print("País ->", country_)

indice = cols_2[date_g]
print(f"Fecha -> {indice}\n")

# -----------------------------------------------------------------
# 4.1 Grafica de casos acumulados de covid por pais

# creamos una funcion para vizulizar por pais

print(">>> Creando gráfica de acumulado de casos por día por país\n")


def country_graph(country, df, graph_tittle, x_label,
                  y_label, st_d, end_dt, s_fig, s_fig2):

    # filtering dataframe
    filtered_df = df[["date", country]].loc[df["date"].between(st_d, end_dt)]
    total_cases = filtered_df[country].loc[filtered_df["date"] == end_dt]
    total_cases = total_cases.iloc[0]

    # line plot
    plt.plot("date", country, data=filtered_df, markersize=7,
             color='skyblue', linewidth=2)

    # x values
    plt.xticks(
        horizontalalignment='right',
        fontweight='light',
        fontsize='9',
        rotation=90
    )

    # graph tittle
    plt.title(graph_tittle,
              fontweight='bold',
              fontsize=13,
              color='black'
              )

    # labels
    plt.xlabel(x_label, fontweight='bold', color='black',
               fontsize='11', horizontalalignment='center')
    plt.ylabel(y_label, fontweight='bold', color='black',
               fontsize='11', horizontalalignment='center')

    # graph padding
    plt.subplots_adjust(top=0.7)

    plt.savefig(s_fig, bbox_inches='tight')
    plt.savefig(s_fig2, bbox_inches='tight')

    plt.show()

    print(
        f"+ El total de casos de Covid-19 en {country} para el {end_dt} fue de {total_cases} infectados")

    return filtered_df


# generar grafica de casos por dia por pais segun se requiera
country = country_
data = tem_pais_t
tittle = f"Acumulado casos Covid-19 por día en {country} 2020"
y_label = "Casos por dia"
x_label = "Fecha"
start_date = start_date_in   # default date:  2020-01-22
end_date = end_date_in  # default date:  2020-10-17
save_fig = f"{path_}COVIS\output\{country}_dailycases_CV19_{start_date}_{end_date}.svg"
save_fig_2 = f"{path_}COVIS\output\{country}_dailycases_CV19_{start_date}_{end_date}.png"

print(f"País graficado -> {country}")
print(f"Fecha -> {indice}\n")

save_country = country_graph(
    country, data, tittle, x_label,
    y_label, start_date, end_date,
    save_fig, save_fig_2)

# guardando datos de grafica
save_country.to_csv(
    fr'{path_}COVIS\output\{country}_dailycases_CV19_{start_date}_{end_date}.csv')

save_country.to_excel(
    fr'{path_}COVIS\output\{country}_dailycases_CV19_{start_date}_{end_date}.xlsx')

print("\n>>> Datos y gráfica de acumulados de casos totales por país guardados en carpeta output")

print("-"*60)


# %%

# 5. creando data frame y grafica de casos totales por pais para vizualizar en folium leaflet

# como leaflet no tiene filtro se deja codigo listo para poder cambiar la grafica introduciendo un numero que corresponde a una fecha en el punto cuadro variable    date_g

print(">>> Creando dataframe de casos totales por país\n")

tem_3 = df_completo.copy()

# creando dataframe para visualizar
tem_3 = tem_3.iloc[:, [0, 1, 2, 3, 4, 5,  date_g]]

tem_3.fillna("", inplace=True)
tem_3.rename(columns={indice: 'Casos totales '}, inplace=True)

total_cases = tem_3

# colocando nombre al index para evitar error en GDS
total_cases.rename_axis(index="index", inplace=True)

save = indice.replace("/", '-')

print(">>> Dataframe de casos totales por país creados\n")

# muestra el dataframe original cargado
with pd.option_context('display.max_rows', 5, 'display.max_columns', 5):
    print(total_cases)

print(">>> Guardando casos totales por país ...\n")

# exportamos el data frame para visualizarlo fuera de python dias
total_cases.to_csv(
    rf"{path_}COVIS\output\totalcases_country_date_{save}.csv")

total_cases.to_excel(
    rf'{path_}COVIS\output\totalcases_country_date_{save}.xlsx')

print(">>> Datos de casos totales por país guardados\n")

# %%
# ----------------------------------------------------------------------

# 5.1 Crear bubble map de Leaflet y casos totales por país

print("\nGRAFICA DE CASOS GLOBALES ACUMULADOS")
print(f"""\nSe cargará la fecha seleccionada anteriormente para generar esta gráfica\n""")
print(f"Fecha de grafica -> {indice}\n")

resp = input("ENTER para continuar...")

print(">>> Creando mapa de Leaflet...")

# creamos plantilla de mapa
map = folium.Map(location=[4.5709, -74.2973],
                 tiles="OpenStreetMap", zoom_start=2)

# añadimos marcadores al mapa uno por uno por cada dato del df
for i in range(0, len(total_cases)):
    # parametros de ingreso de funcion mapa
    radio = total_cases.iloc[i]['Casos totales ']/230000
    locacion = [total_cases.iloc[i]['Lat'], total_cases.iloc[i]['Long']]
    reg, cas = total_cases.iloc[i][['Region', "Casos totales "]]
    pop = f" Región: {reg} | Casos Totales: {cas} infectados"

    folium.CircleMarker(
        location=locacion,
        popup=pop,
        radius=float(radio),
        color='crimson',
        fill=False,
        fill_color='crimson'
    ).add_to(map)

titulo = f"Casos totales de covid por paises en el {indice}."
title_html = f'''
             <h3 align="center" style="font-size:16px"><b>{titulo}</b></h3>
             '''
map.get_root().html.add_child(folium.Element(title_html))

print(">>> Mapa de Leaflet creado \n")
print(map)


print("\n>>> Guardando mapa en formato html...")

# guardar mapa en formato html para visualizar en navegador
map.save(
    fr'{path_}COVIS\output\map_totalcases_country_date_{save}.html')

print(">>> El mapa de Leaflet ha sido guardado en la carpeta output puede visulizarlo en su navegador predeterminado\n")

# %%
print("Fin del análisis por ahora vaya a su carpeta output para ver los resultados | Disfruta => ...\n")

print("-"*60)
print("-"*60)

print("   *Script made by Hardroco | 2021 - MIT license.")

print("-"*60)
print("-"*60)


fin = input("Presione cualquier tecla para finalizar")

# fin
