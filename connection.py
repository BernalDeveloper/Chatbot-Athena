import pymssql
import os

def connectCMP():
    try:
        conexion = pymssql.connect(os.environ.get('CLOUD_SERVER_NAME'), os.environ.get('CLOUD_SQL_USERNAME'), os.environ.get('CLOUD_SQL_PASSWORD'), os.environ.get('CLOUD_SQL_DATABASE_CMP'))
        print('Conexion exitosa...')
        return conexion
    except Exception as e:
        print(e)
        return None
      
def connectCDC():
    try:
        conexion = pymssql.connect(os.environ.get('CLOUD_SERVER_NAME'), os.environ.get('CLOUD_SQL_USERNAME'), os.environ.get('CLOUD_SQL_PASSWORD'), os.environ.get('CLOUD_SQL_DATABASE_CDC'))
        print('Conexion exitosa...')
        return conexion
    except Exception as e:
        print(e)
        return None
      
def execut(conexion, consulta, params):
    try:
        cursor = conexion.cursor()
        cursor.execute(consulta, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
      
def docscmp(rfc):

    conexion=connectCMP()
    
    if(len(str(rfc))>10):
        consulta = "SELECT [CIDDOCUMENTO], [CFECHA], [CFOLIO], [CSERIEDOCUMENTO], [CTOTAL], [CPENDIENTE], dbo.admDocumentos.[CTOTALUNIDADES], dbo.admDocumentos.[CUNIDADESPENDIENTES], dbo.admDocumentos.[CIDAGENTE], dbo.admAgentes.[CNOMBREAGENTE], CASE WHEN dbo.admDocumentos.[CRAZONSOCIAL] = 'Público General' OR dbo.admDocumentos.[CRAZONSOCIAL] = 'Publico General' THEN dbo.admClientes.[CTEXTOEXTRA3] ELSE dbo.admDocumentos.[CRAZONSOCIAL] END AS [CRAZONSOCIAL], CASE WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC1' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC1' THEN 'En ruta' WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG401' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG401' THEN 'Por cargar' END AS [CESTATUS] FROM dbo.admDocumentos INNER JOIN dbo.admClientes ON dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = dbo.admClientes.[CIDCLIENTEPROVEEDOR] INNER JOIN dbo.admAgentes ON dbo.admDocumentos.[CIDAGENTE] = dbo.admAgentes.[CIDAGENTE] WHERE dbo.admDocumentos.[CRFC] = %s AND ([CSERIEDOCUMENTO] = 'PCIC1' OR [CSERIEDOCUMENTO] = 'FG401') AND [CFECHA] >= DATEADD(MONTH, -1, GETDATE());"
    else:
        consulta = "SELECT [CIDDOCUMENTO], [CFECHA], [CFOLIO], [CSERIEDOCUMENTO], [CTOTAL], [CPENDIENTE], dbo.admDocumentos.[CTOTALUNIDADES], dbo.admDocumentos.[CUNIDADESPENDIENTES], dbo.admDocumentos.[CIDAGENTE], dbo.admAgentes.[CNOMBREAGENTE], CASE WHEN dbo.admDocumentos.[CRAZONSOCIAL] = 'Público General' OR dbo.admDocumentos.[CRAZONSOCIAL] = 'Publico General' THEN dbo.admClientes.[CTEXTOEXTRA3] ELSE dbo.admDocumentos.[CRAZONSOCIAL] END AS [CRAZONSOCIAL], CASE WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC1' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC1' THEN 'En ruta' WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG401' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG401' THEN 'Por cargar' END AS [CESTATUS] FROM dbo.admDocumentos INNER JOIN dbo.admClientes ON dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = dbo.admClientes.[CIDCLIENTEPROVEEDOR] INNER JOIN dbo.admAgentes ON dbo.admDocumentos.[CIDAGENTE] = dbo.admAgentes.[CIDAGENTE] WHERE dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = %s AND ([CSERIEDOCUMENTO] = 'PCIC1' OR [CSERIEDOCUMENTO] = 'FG401') AND [CFECHA] >= DATEADD(MONTH, -1, GETDATE());"

    if conexion:
      
        resultado = execut(conexion, consulta, rfc)

        if resultado:
            rows_as_dicts = []
            for fila in resultado:
                fila_dict = {
                  'CIDDOCUMENTO': fila[0],
                  'CFECHA': fila[1].strftime('%Y-%m-%d %H:%M:%S'),
                  'CFOLIO': fila[2],
                  'CESTATUS': fila[11],
                  'CRAZONSOCIAL': fila[10],
                  'CSERIEDOCUMENTO': fila[3],
                  'CNOMBREAGENTE': fila[9],
                  'CTOTAL': fila[4],
                  'CPENDIENTE': fila[5]
                }
                rows_as_dicts.append(fila_dict)
                print(f'CIDDOCUMENTO: {fila[0]}, FECHA: {fila[1]}, Nombre: {fila[10]}, Serie: {fila[3]}')

            return rows_as_dicts
        else:
            return []

    return None
  
def docscdc(rfc):

    conexion=connectCDC()

    if(len(str(rfc))>10):
        consulta = "SELECT [CIDDOCUMENTO], [CFECHA], [CFOLIO], [CSERIEDOCUMENTO], [CTOTAL], [CPENDIENTE], dbo.admDocumentos.[CTOTALUNIDADES], dbo.admDocumentos.[CUNIDADESPENDIENTES], dbo.admDocumentos.[CIDAGENTE], dbo.admAgentes.[CNOMBREAGENTE], CASE WHEN dbo.admDocumentos.[CRAZONSOCIAL] = 'Público General' OR dbo.admDocumentos.[CRAZONSOCIAL] = 'Publico General' THEN dbo.admClientes.[CTEXTOEXTRA3] ELSE dbo.admDocumentos.[CRAZONSOCIAL] END AS [CRAZONSOCIAL], CASE WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC2' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC2' THEN 'En ruta' WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG402' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG402' THEN 'Por cargar' END AS [CESTATUS] FROM dbo.admDocumentos INNER JOIN dbo.admClientes ON dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = dbo.admClientes.[CIDCLIENTEPROVEEDOR] INNER JOIN dbo.admAgentes ON dbo.admDocumentos.[CIDAGENTE] = dbo.admAgentes.[CIDAGENTE] WHERE dbo.admDocumentos.[CRFC] = %s AND ([CSERIEDOCUMENTO] = 'PCIC2' OR [CSERIEDOCUMENTO] = 'FG402') AND [CFECHA] >= DATEADD(MONTH, -1, GETDATE());"
    else:
        consulta = "SELECT [CIDDOCUMENTO], [CFECHA], [CFOLIO], [CSERIEDOCUMENTO], [CTOTAL], [CPENDIENTE], dbo.admDocumentos.[CTOTALUNIDADES], dbo.admDocumentos.[CUNIDADESPENDIENTES], dbo.admDocumentos.[CIDAGENTE], dbo.admAgentes.[CNOMBREAGENTE], CASE WHEN dbo.admDocumentos.[CRAZONSOCIAL] = 'Público General' OR dbo.admDocumentos.[CRAZONSOCIAL] = 'Publico General' THEN dbo.admClientes.[CTEXTOEXTRA3] ELSE dbo.admDocumentos.[CRAZONSOCIAL] END AS [CRAZONSOCIAL], CASE WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC2' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'PCIC2' THEN 'En ruta' WHEN [CUNIDADESPENDIENTES] != [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG402' THEN 'Entregado' WHEN [CUNIDADESPENDIENTES] = [CTOTALUNIDADES] AND [CSERIEDOCUMENTO] = 'FG402' THEN 'Por cargar' END AS [CESTATUS] FROM dbo.admDocumentos INNER JOIN dbo.admClientes ON dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = dbo.admClientes.[CIDCLIENTEPROVEEDOR] INNER JOIN dbo.admAgentes ON dbo.admDocumentos.[CIDAGENTE] = dbo.admAgentes.[CIDAGENTE] WHERE dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = %s AND ([CSERIEDOCUMENTO] = 'PCIC2' OR [CSERIEDOCUMENTO] = 'FG402') AND [CFECHA] >= DATEADD(MONTH, -1, GETDATE());"
    
    if conexion:
      
        resultado = execut(conexion, consulta, rfc)

        if resultado:
            rows_as_dicts = []
            for fila in resultado:
                fila_dict = {
                  'CIDDOCUMENTO': fila[0],
                  'CFECHA': fila[1].strftime('%Y-%m-%d %H:%M:%S'),
                  'CFOLIO': fila[2],
                  'CESTATUS': fila[11],
                  'CRAZONSOCIAL': fila[10],
                  'CSERIEDOCUMENTO': fila[3],
                  'CNOMBREAGENTE': fila[9],
                  'CTOTAL': fila[4],
                  'CPENDIENTE': fila[5]
                }
                rows_as_dicts.append(fila_dict)
                print(f'CIDDOCUMENTO: {fila[0]}, FECHA: {fila[1]}, Nombre: {fila[10]}, Serie: {fila[3]}')

            return rows_as_dicts
        else:
            return []

    return None
  
def movimientos(iddoc):

  conexion=connectCMP()
  consulta = "SELECT dbo.admMovimientos.[CIDPRODUCTO], dbo.admMovimientos.[CUNIDADES], dbo.admProductos.[CNOMBREPRODUCTO] FROM dbo.admMovimientos INNER JOIN dbo.admProductos ON dbo.admMovimientos.[CIDPRODUCTO] = dbo.admProductos.[CIDPRODUCTO] WHERE dbo.admMovimientos.[CIDDOCUMENTO] = %s;"

  if conexion:
      resultado = execut(conexion, consulta, iddoc)

      if resultado:
          rows_as_dicts = []
          for fila in resultado:
              fila_dict = {
                  'CIDPRODUCTO': fila[0],
                  'CNOMBREPRODUCTO': fila[2],
                  'CUNIDADES': fila[1]
              }
              rows_as_dicts.append(fila_dict)
              print(f'ID-PRODUCTO: {fila[0]}, NOMBRE: {fila[2]}, UNIDADES: {fila[1]}')

          return rows_as_dicts
      else:
        conexion=connectCDC()
        if conexion:
            resultado = execut(conexion, consulta, iddoc)
            if resultado:
                rows_as_dicts = []
                for fila in resultado:
                    fila_dict = {
                        'CIDPRODUCTO': fila[0],
                        'CNOMBREPRODUCTO': fila[2],
                        'CUNIDADES': fila[1]
                    }
                    rows_as_dicts.append(fila_dict)
                    print(f'ID-PRODUCTO: {fila[0]}, NOMBRE: {fila[2]}, UNIDADES: {fila[1]}')

                return rows_as_dicts
            else:
                return []
  return None

def idcliente(cc):

    conexion = connectCMP()
    consulta = "SELECT [CIDCLIENTEPROVEEDOR] FROM dbo.admClientes WHERE [CCODIGOCLIENTE] = %s"
    id = [None, None]

    if conexion:
        resultado = execut(conexion, consulta, cc)
        if resultado:
            id[0]=resultado[0]
        else:
            id[0]=None

    conexion = connectCDC()
    if conexion:
        resultado = execut(conexion, consulta, cc)
        if resultado:
            id[1]=resultado[0]
        else:
            id[1]=None

    return id
  
def codigocliente(iddoc):

    conexion = connectCMP()
    consulta = "SELECT dbo.admClientes.[CCODIGOCLIENTE], dbo.admDocumentos.[CFOLIO] FROM dbo.admDocumentos JOIN dbo.admClientes ON dbo.admDocumentos.[CIDCLIENTEPROVEEDOR] = dbo.admClientes.[CIDCLIENTEPROVEEDOR] WHERE dbo.admDocumentos.[CIDDOCUMENTO] = %s"

    if conexion:
        resultado = execut(conexion, consulta, iddoc)
        if resultado:
            return resultado[0]
        else:
            conexion = connectCDC()
            if conexion:
                resultado = execut(conexion, consulta, iddoc)
                if resultado:
                    return resultado[0]
            else:
                return None
    else:
        return None