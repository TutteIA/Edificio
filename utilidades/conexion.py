# Librerias
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Funcion para conectar python con google drive y sheets
# usamos las credenciales publicas y json de google console cloud
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
