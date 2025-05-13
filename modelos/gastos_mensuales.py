# Librerias
import pandas as pd


# Funcion que genera un df con los gastos del negocio
def generar_gastos_mensuales(df_gastos):

    # formatear fechas
    df_gastos["fecha"] = pd.to_datetime(df_gastos["fecha"], format="%d/%m/%Y")

    # crear columna mes
    df_gastos["num_mes"] = df_gastos["fecha"].dt.month

    # retornar df final
    return df_gastos
