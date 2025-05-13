# librerias
import pandas as pd


# Funcion que genera hoja auxiliar para rentabilidad
# trabaja con los df's creados de ingresos y gastos mensuales
# calcula el total por mes de cada df y calcula la respectiva rentabilidad
def generar_rentabilidad(df_ingresos_mensuales, df_gastos_mensuales):

    # calcular total ingresos x mes
    df_ingresos_mensuales_totales = (
        df_ingresos_mensuales.groupby("num_mes")["total_pagado"].sum().reset_index()
    )

    # calcular total gastos x mes
    df_gastos_mensuales_totales = (
        df_gastos_mensuales.groupby("num_mes")["monto"].sum().reset_index()
    )

    # genera df rentabilidad integrando ingresos con gastos
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

    # calcula rentabilidad
    df_rentabilidad["rentabilidad"] = (
        df_rentabilidad["total_ingresos"] - df_rentabilidad["total_gastos"]
    )

    # retorna df final
    return df_rentabilidad
