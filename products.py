import gspread
import arrays
from google.oauth2.service_account import Credentials

Scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
Keys = 'keys.json'

credentials = Credentials.from_service_account_file(Keys, scopes=Scopes)

cliente = gspread.authorize(credentials)

hoja = cliente.open('Escaleras').sheet1

def get_filled_rows():

    return [row for row in hoja.get_all_values() if any(cell for cell in row)]

def list_menu():

    options=[]
    seen_values = set()
    
    for row in get_filled_rows():
        value = row[0]
        if value not in seen_values and value != 'Clasificación':
            seen_values.add(value)
            options.append(value)
    
    return options
  
def list_submenu():
    sub_opt=[]
    seen_values = set()

    for row in get_filled_rows():
        value = row[2]
        value_two = row[0]
        if value not in seen_values and value != 'Grupo':
            seen_values.add(value)
            sub_opt.append(value)
    
    return sub_opt
  
def list_products(group):
    products=[]
    seen_values=set()

    for row in get_filled_rows():
        value=row[2]
        value_two=row[0]
        if value not in seen_values and value != 'Grupo' and value_two==group:
            seen_values.add(value)
            products.append(value)

    return products
  
def list_models(group):
    models=[]
    arr_models=[]
    seen_values=set()

    for row in get_filled_rows():
        value=row[3]
        description=row[5]
        value_two=row[2]
        if value not in seen_values and value != 'Código iterno' and value_two==group:
            seen_values.add(value)
            models.append({"title": value, "description": description})
            arr_models.append(value)

    return models, arr_models
  
def all_models():
    all_model=[]
    seen_values=set()

    for row in get_filled_rows():
        value=row[3]
        if value not in seen_values and value != 'Código iterno':
            all_model.append(value)
    
    return all_model
  
def codigos(codigo):
    book = cliente.open('Escaleras')
    worksheet = book.get_worksheet(4)

    columna_a = worksheet.col_values(1)

    for valor in columna_a:
        if codigo == valor:
            return valor
        
    return None

def tel(codigo):
    book = cliente.open('Escaleras')
    worksheet = book.get_worksheet(4)

    columna_a = worksheet.col_values(1)
    columna_c = worksheet.col_values(4)

    if codigo in columna_a:
        i = columna_a.index(codigo)
        if i < len(columna_c):
            valor_celda = columna_c[i]
            if valor_celda:
                return valor_celda

    return None

def clasification(codigo):

    for row in get_filled_rows():
        value=row[3]
        if value == codigo:
            clase=row[0]
            return clase

    return None

def desc(modelo):
    try:
        flat_data = hoja.range('A2:J142')

        all_data = [flat_data[i:i+10] for i in range(0, len(flat_data), 10)]

        for row in all_data:
            if modelo == row[3].value:
                descripcion = f"*Código*\n{row[3].value}\n\n" + \
                              f"*Modelo*\n{row[4].value}\n\n" + \
                              f"*Descripción*\n{row[5].value}\n\n" + \
                              f"*Características*\n{row[6].value}\n\n" + \
                              f"*Precio de lista (IVA incluido)*\n{row[7].value}"
                return descripcion
                break
    except Exception as e:
        print(e)

def iddrive(id):

    for producto in arrays.ids:
        if producto["codigo"] == id:
            return producto["id"]

    return None