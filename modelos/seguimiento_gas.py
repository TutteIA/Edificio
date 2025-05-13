# Librerias
import pandas as pd


# Funcion que genera df para el seguimiento de un gasto del negocio
# trabaja con las fechas de activacion y finalizacion
# permite saber que par se encuentra activo
def generar_seguimiento_gas(df_seg_gas):

    # formatea fechas (inicio y fin)
    df_seg_gas["fecha_inicio"] = pd.to_datetime(
        df_seg_gas["fecha_inicio"], format="%d/%m/%Y"
    )
    df_seg_gas["fecha_fin"] = pd.to_datetime(df_seg_gas["fecha_fin"], format="%d/%m/%Y")

    # crea columna mes
    df_seg_gas["num_mes"] = df_seg_gas["fecha_inicio"].dt.month

    # calcula el par activo
    ult_fecha_inicio = df_seg_gas["fecha_inicio"].max()
    df_seg_gas["par_activo"] = df_seg_gas["fecha_inicio"].apply(
        lambda x: "activo" if x == ult_fecha_inicio else "inactivo"
    )

    # retornar df final
    return df_seg_gas
