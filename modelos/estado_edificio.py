# Librerias
import pandas as pd


# Funcion que genera df para conocimiento general del estado del negocio
# trabaja con dos hojas auxiliares del libro
# genera una sola tabla para saber que espacios estan libres, ocupados, y demas informacion
def generar_estado_edificio(df_estado_deptos, df_estado_cochera):

    # seleccion de columnas para deptos
    df_estado_deptos = df_estado_deptos[
        ["id_depto", "funcion", "estado", "ultimo_precio"]
    ]

    # seleccion de columnas para cochera
    df_estado_cochera = df_estado_cochera[
        ["id_cochera", "vehiculo", "estado", "ultimo_precio"]
    ]

    # renombrar columnas
    df_estado_deptos = df_estado_deptos.rename(
        columns={"id_depto": "id", "funcion": "utilidad"}
    )
    df_estado_cochera = df_estado_cochera.rename(
        columns={"id_cochera": "id", "vehiculo": "utilidad"}
    )

    # agregar columna de especificacion
    df_estado_deptos["sector"] = "depto"
    df_estado_cochera["sector"] = "cochera"

    # unir tablas
    df_estado_edificio = pd.concat(
        [df_estado_deptos, df_estado_cochera], ignore_index=True
    )

    # retorna df final
    return df_estado_edificio
