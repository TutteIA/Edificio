# ----------------------------
# LIBRERIAS
from dotenv import load_dotenv
import os


# ----------------------------
# FUNCIONES AUXILIARES

# conexion con google
from utilidades.conexion import conexion_google

# obtener y cargar hojas de calculo
from utilidades.get_hojas import obtener_sheet, cargar_sheet

# generar hojas auxiliares (para pagina uno)
from modelos.ingresos_mensuales import generar_ingresos_mensuales
from modelos.gastos_mensuales import generar_gastos_mensuales
from modelos.rentabilidad import generar_rentabilidad
from modelos.seguimiento_gas import generar_seguimiento_gas

# generar hojas auxiliares (para pagina dos)
from modelos.estado_edificio import generar_estado_edificio
from modelos.estado_servicios import generar_estado_servicios


# ----------------------------
# CONEXION PYTHON - GOOGLE

load_dotenv()
# libro principal
cliente_origen = conexion_google(os.getenv("CRED_ORIGEN"))
LIBRO_ORIGEN = os.getenv("LIBRO_ORIGEN")

# libro auxiliar
cliente_destino = conexion_google(os.getenv("CRED_DESTINO"))
LIBRO_DESTINO = os.getenv("LIBRO_DESTINO")


# ----------------------------
# DATAFRAMES

# de hojas de calculo a df's (para pagina uno)
df_ficha_mes = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Mensualidad")
df_ingresos = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Ingresos")
df_clientes = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Clientes")
df_gastos = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Gastos")
df_seguimiento_gas = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Seguimiento Gas")
df_estado_deptos = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Deptos")
df_estado_cochera = obtener_sheet(cliente_origen, LIBRO_ORIGEN, "Cochera")

# guardado de df's como proteccion de datos (para pagina uno)
df_ficha_mes.to_csv("data_backup/ficha_mes.csv", index=False)
df_ingresos.to_csv("data_backup/ingresos.csv", index=False)
df_clientes.to_csv("data_backup/clientes.csv", index=False)
df_gastos.to_csv("data_backup/gastos.csv", index=False)
df_seguimiento_gas.to_csv("data_backup/seguimiento_gas.csv", index=False)
df_estado_deptos.to_csv("data_backup/estado_deptos.csv", index=False)
df_estado_cochera.to_csv("data_backup/estado_cochera.csv", index=False)


# ----------------------------
# GENERACION DE MODELOS

# creacion de df's para hojas de calculo auxiliares
df_ingresos_mensuales = generar_ingresos_mensuales(
    df_ficha_mes, df_ingresos, df_clientes
)
df_gastos_mensuales = generar_gastos_mensuales(df_gastos)
df_rentabilidad = generar_rentabilidad(df_ingresos_mensuales, df_gastos_mensuales)
df_seguimiento_gas = generar_seguimiento_gas(df_seguimiento_gas)
df_estado_edificio = generar_estado_edificio(df_estado_deptos, df_estado_cochera)
df_estado_servicios = generar_estado_servicios(df_ficha_mes, df_gastos)


# ----------------------------
# CREACION DE HOJAS AUXILIARES

# creacion y carga de sheets en el libro auxiliar (para pagina uno)
cargar_sheet(
    cliente_destino, LIBRO_DESTINO, "Ingresos Mensuales", df_ingresos_mensuales
)
cargar_sheet(cliente_destino, LIBRO_DESTINO, "Gastos Mensuales", df_gastos_mensuales)
cargar_sheet(cliente_destino, LIBRO_DESTINO, "Rentabilidad", df_rentabilidad)
cargar_sheet(cliente_destino, LIBRO_DESTINO, "Seguimiento Gas", df_seguimiento_gas)
cargar_sheet(cliente_destino, LIBRO_DESTINO, "Estado Edificio", df_estado_edificio)
cargar_sheet(cliente_destino, LIBRO_DESTINO, "Estado Servicios", df_estado_servicios)


# ----------------------------
# FIN DEL PROGRAMA
