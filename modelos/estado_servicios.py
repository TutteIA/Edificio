# Librerias
import pandas as pd


# Funcion que genera df para el estado de rentabilidad por servicio del negocio
# permite saber el ingreso estimado, el gasto mensual, y la rentabilidad mensual por servicio
def generar_estado_servicios(df_ficha_mes, df_gastos):

    # formateo de fechas
    df_ficha_mes["fecha"] = pd.to_datetime(df_ficha_mes["fecha"], format="%d/%m/%Y")
    df_gastos["fecha"] = pd.to_datetime(df_gastos["fecha"], format="%d/%m/%Y")

    # columna para numero del mes
    df_ficha_mes["num_mes"] = df_ficha_mes["fecha"].dt.month
    df_gastos["num_mes"] = df_gastos["fecha"].dt.month

    # seleccion de columnas de servicios-ingreso
    cols_servicios_ingreso = ["agua", "gas", "internet", "expensas", "luz"]

    # calcula el ingreso estimado del mes por servicio
    df_ingresos_servicios = (
        df_ficha_mes.groupby("num_mes")[cols_servicios_ingreso].sum().reset_index()
    )

    # pivoteo para generar el orden deseado
    df_ingresos_servicios = df_ingresos_servicios.melt(
        id_vars="num_mes", var_name="servicio", value_name="monto_estimado"
    )

    # mapeo de servicio con gastos
    mapeo_servicios = {
        "edea": "luz",
        "limpieza": "expensas",
        "personal flow": "internet",
        "par garrafas de 45": "gas",
        "obras sanitarias": "agua",
    }

    # columna nueva para asignar servicio-ingreso al gasto
    df_gastos["servicio"] = df_gastos["gasto"].map(mapeo_servicios)

    # filtro de servicios y gastos seleccionados
    df_gastos_filtrado = df_gastos[df_gastos["servicio"].notna()].copy()

    # agrupa por mes, servicio y suma el monto
    df_gastos_por_servicio = (
        df_gastos_filtrado.groupby(["num_mes", "servicio"])["monto"].sum().reset_index()
    )

    # renombra columna
    df_gastos_por_servicio.rename(columns={"monto": "monto_gasto"}, inplace=True)

    # genera df con ingresos y gastos por servicio
    df_comparativo = pd.merge(
        df_ingresos_servicios,
        df_gastos_por_servicio,
        on=["num_mes", "servicio"],
        how="outer",
    ).fillna(0)

    # calcula la rentabilidad
    df_comparativo["rentabilidad_servicio"] = (
        df_comparativo["monto_estimado"] - df_comparativo["monto_gasto"]
    )

    # retorna df final
    return df_comparativo
