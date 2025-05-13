# librerias
import pandas as pd


# Funcion que genera hoja auxiliar para seguimiento de gas
# trabaja con las fechas de activacion y finalizacion
# calcula el par activo usando la ultima fecha de inicio registrada
def generar_seguimiento_gas(df_seg_gas):

    # formatear fechas
    df_seg_gas["fecha_inicio"] = pd.to_datetime(
        df_seg_gas["fecha_inicio"], format="%d/%m/%Y"
    )
    df_seg_gas["fecha_fin"] = pd.to_datetime(df_seg_gas["fecha_fin"], format="%d/%m/%Y")

    # crear columna mes
    df_seg_gas["num_mes"] = df_seg_gas["fecha_inicio"].dt.month

    # calcula par activo
    ult_fecha_inicio = df_seg_gas["fecha_inicio"].max()
    df_seg_gas["par_activo"] = df_seg_gas["fecha_inicio"].apply(
        lambda x: "activo" if x == ult_fecha_inicio else "inactivo"
    )

    # retornar df final
    return df_seg_gas
