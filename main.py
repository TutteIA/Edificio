# ----------------------------
# FUNCIONES EXTRAIDAS

# para obtener variables privadas
from dotenv import load_dotenv
import os

# para conexion con google
from utilidades.conexion import conexion_google

# para obtener y cargar hojas de calculo
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

# conexion al libro de carga de datos
cliente = conexion_google("credenciales-proyecto-mendoza.json")
NOMBRE_LIBRO = os.getenv("NOMBRE_LIBRO")

# conexion al libro auxiliar para conexion looker
cliente_nuevo = conexion_google("credenciales-proyecto-mendoza-looker.json")
KEY_LIBRO_NUEVO = os.getenv("KEY_LIBRO_NUEVO")


# ----------------------------
# DATAFRAMES

# de hojas de calculo a df's
# para pagina uno
df_ficha_mes = obtener_sheet(cliente, NOMBRE_LIBRO, "Mensualidad")
df_ingresos = obtener_sheet(cliente, NOMBRE_LIBRO, "Ingresos")
df_clientes = obtener_sheet(cliente, NOMBRE_LIBRO, "Clientes")
df_gastos = obtener_sheet(cliente, NOMBRE_LIBRO, "Gastos")
df_seguimiento_gas = obtener_sheet(cliente, NOMBRE_LIBRO, "Seguimiento Gas")

# para pagina dos
df_estado_deptos = obtener_sheet(cliente, NOMBRE_LIBRO, "Deptos")
df_estado_cochera = obtener_sheet(cliente, NOMBRE_LIBRO, "Cochera")


# guardado de df's como proteccion de datos
# para pagina uno
df_ficha_mes.to_csv("data_backup/ficha_mes.csv", index=False)
df_ingresos.to_csv("data_backup/ingresos.csv", index=False)
df_clientes.to_csv("data_backup/clientes.csv", index=False)
df_gastos.to_csv("data_backup/gastos.csv", index=False)
df_seguimiento_gas.to_csv("data_backup/seguimiento_gas.csv", index=False)

# para pagina dos
df_estado_deptos.to_csv("data_backup/estado_deptos.csv", index=False)
df_estado_cochera.to_csv("data_backup/estado_cochera.csv", index=False)

# ----------------------------
# GENERACION DE MODELOS

# creacion de df's para hojas de calculo auxiliares
# para pagina uno
df_ingresos_mensuales = generar_ingresos_mensuales(
    df_ficha_mes, df_ingresos, df_clientes
)
df_gastos_mensuales = generar_gastos_mensuales(df_gastos)
df_rentabilidad = generar_rentabilidad(df_ingresos_mensuales, df_gastos_mensuales)
df_seguimiento_gas = generar_seguimiento_gas(df_seguimiento_gas)

# para pagina dos
df_estado_edificio = generar_estado_edificio(df_estado_deptos, df_estado_cochera)
df_estado_servicios = generar_estado_servicios(df_ficha_mes, df_gastos)

# ----------------------------
# CREACION DE HOJAS AUXILIARES

# creacion y carga de sheets en el libro auxiliar
# para pagina uno
cargar_sheet(
    cliente_nuevo, KEY_LIBRO_NUEVO, "Ingresos Mensuales", df_ingresos_mensuales
)
cargar_sheet(cliente_nuevo, KEY_LIBRO_NUEVO, "Gastos Mensuales", df_gastos_mensuales)
cargar_sheet(cliente_nuevo, KEY_LIBRO_NUEVO, "Rentabilidad", df_rentabilidad)
cargar_sheet(cliente_nuevo, KEY_LIBRO_NUEVO, "Seguimiento Gas", df_seguimiento_gas)

# para pagina dos
cargar_sheet(cliente_nuevo, KEY_LIBRO_NUEVO, "Estado Edificio", df_estado_edificio)
cargar_sheet(cliente_nuevo, KEY_LIBRO_NUEVO, "Estado Servicios", df_estado_servicios)
# ----------------------------
