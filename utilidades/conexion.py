# librerias
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Funcion para conectar python a google drive y sheets
# usamos credenciales y un json creado desde google console cloud
def conexion_google(credenciales_json):

    # credenciales de acceso globales
    alcance = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credenciales = ServiceAccountCredentials.from_json_keyfile_name(
        credenciales_json, alcance
    )
    cliente = gspread.authorize(credenciales)

    return cliente
