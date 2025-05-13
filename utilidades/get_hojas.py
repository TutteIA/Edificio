# Librerias
from gspread_dataframe import get_as_dataframe
from gspread_dataframe import set_with_dataframe
import gspread


# Funcion para extraer hoja de calculo de un Libro
# lo retorna como df
def obtener_sheet(cliente, key_libro, nombre_hoja):

    libro = cliente.open_by_key(key_libro)
    hoja = libro.worksheet(nombre_hoja)
    df = get_as_dataframe(
        hoja, evaluate_formulas=True
    )  # convierte contenido de hoja en df
    df.dropna(
        how="all", inplace=True
    )  # elimina las filas que estan completamente vacias

    return df


# Funcion para pasar un df a una hoja de calculo en un Libro
def cargar_sheet(cliente, key_libro, nombre_hoja, df):

    libro = cliente.open_by_key(key_libro)

    try:
        hoja = libro.worksheet(nombre_hoja)
    except gspread.exceptions.WorksheetNotFound:
        # Si la hoja no existe, la creamos
        hoja = libro.add_worksheet(
            title=nombre_hoja, rows=df.shape[0] + 10, cols=df.shape[1] + 5
        )

    # Limpiar la hoja antes de escribir
    hoja.clear()

    # Escribir DataFrame
    set_with_dataframe(hoja, df)
