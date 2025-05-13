# Librerias
import pandas as pd


# Funcion que genera un df con el estado general de ingresos del negocio
# contiene el total pagado por mes y por cliente, la diferencia (total estimado) y el estado de pago
def generar_ingresos_mensuales(df_ficha_mes, df_ingresos, df_clientes):

    # formatear fechas
    df_ficha_mes["fecha"] = pd.to_datetime(df_ficha_mes["fecha"], format="%d/%m/%Y")
    df_ingresos["fecha"] = pd.to_datetime(df_ingresos["fecha"], format="%d/%m/%Y")

    # crear columna mes
    df_ficha_mes["num_mes"] = df_ficha_mes["fecha"].dt.month
    df_ingresos["num_mes"] = df_ingresos["fecha"].dt.month

    # calcula el total pagado por mes y por cliente
    df_ingresos_mensual = (
        df_ingresos.groupby(["id_cliente", "num_mes"])
        .agg(total_pagado=("monto", "sum"), fecha_pago=("fecha", "max"))
        .reset_index()
    )

    # genera df integrando ficha-mes con ingresos
    df_ficha_U_ingresos = pd.merge(
        df_ficha_mes, df_ingresos_mensual, on=["id_cliente", "num_mes"], how="left"
    )

    # rellena con cero donde el cliente no haya pagado
    df_ficha_U_ingresos["total_pagado"] = df_ficha_U_ingresos["total_pagado"].fillna(0)

    # calcula diferencia de pago y  su estado de pago
    df_ficha_U_ingresos["diferencia"] = (
        df_ficha_U_ingresos["total"] - df_ficha_U_ingresos["total_pagado"]
    )
    df_ficha_U_ingresos["estado_pago"] = df_ficha_U_ingresos["diferencia"].apply(
        lambda x: "pago" if x <= 0 else "debe"
    )

    # integra al df informacion de clientes
    df_ficha_U_ingresos = pd.merge(
        df_ficha_U_ingresos,
        df_clientes[["id_cliente", "nombre", "id_depto"]],
        on="id_cliente",
        how="left",
    )

    # calcula mes
    df_ficha_U_ingresos["num_mes"] = df_ficha_U_ingresos["fecha"].dt.month

    # seleccion de columnas
    cols_finales = [
        "id_cliente",
        "nombre",
        "total",
        "total_pagado",
        "diferencia",
        "fecha_pago",
        "estado_pago",
        "id_depto",
        "num_mes",
    ]

    # retornar df final
    return df_ficha_U_ingresos[cols_finales]
