# Librerias
import pandas as pd


# Funcion que genera df de rentabilidad mensual del negocio
# compara el total ingresado por el total gastado por mes
def generar_rentabilidad(df_ingresos_mensuales, df_gastos_mensuales):

    # calcula total ingresos x mes
    df_ingresos_mensuales_totales = (
        df_ingresos_mensuales.groupby("num_mes")["total_pagado"].sum().reset_index()
    )

    # calcula total gastado x mes
    df_gastos_mensuales_totales = (
        df_gastos_mensuales.groupby("num_mes")["monto"].sum().reset_index()
    )

    # genera df rentabilidad con ingresos y gastos por mes
    df_rentabilidad = pd.merge(
        df_ingresos_mensuales_totales,
        df_gastos_mensuales_totales,
        on="num_mes",
        how="left",
    )

    # renombra columnas
    df_rentabilidad = df_rentabilidad.rename(
        columns={"total_pagado": "total_ingresos", "monto": "total_gastos"}
    )

    # calcula rentabilidad mensual
    df_rentabilidad["rentabilidad"] = (
        df_rentabilidad["total_ingresos"] - df_rentabilidad["total_gastos"]
    )

    # retorna df final
    return df_rentabilidad
