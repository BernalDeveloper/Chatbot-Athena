import os
import requests
import openai
import re
import connection
import payloads
import products
import arrays
import documents
import time
import audios

def obtener(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
        if(text==None or text==' '):
          text = message['interactive']['list_reply']['description']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
        if(text==None or text==' '):
          text = message['interactive']['list_reply']['description']
    elif typeMessage == 'audio':
        text = audios.descargar_audio(message['audio']['id'])
        audios.eliminar_audio(message['audio']['id']+".mp3")
    elif typeMessage == 'sticker':
        text = 'unknow_sticker'
    else:
        text = 'mensaje no procesado'
        
    print(text)

    return text

def obtener_id(message):

    if 'type' not in message:
        id = 'Id no identificado'
        return id

    typeMessage = message['type']
    if typeMessage == 'text':
        id = message['id']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        id = message['interactive']['button_reply']['id']
    elif typeMessage == 'sticker':
        #id = message['sticker']['id']
        id = message['id']
    else:
        id = 'Id no reconocido'

    print(id)

    return id

def env_msj(data):
    try:
        whatsapp_token = os.environ.get('WHATSAPP_TOKEN')
        whatsapp_url = os.environ.get('WHATSAPP_URL')
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, headers=headers, data=data)
        if response.status_code == 200:
            return 'Mensaje enviado', 200
        else:
            print(f"Error en la respuesta: {response.text}")
            return 'Error al enviar el mensaje', response.status_code
        
    except Exception as e:
        return str(e)

def administrar_chatbot(text, number, messageId, name):

    message_list = []
    documentos = []
    movimientos = []
    
    if text in arrays.saludos:
        data = payloads.stck_msj(number, arrays.stickers["saludo"])
        message_list.append(data)
        body = "¡Hola! 👋🏻, soy Athena 👩‍💼, tu asistente virtual 🤖💙.\nPor favor, elige una opción del menú ✅ o sólo escribe 'Hola':"
        replyListData = payloads.listReply_Message(number, body, None, "sedd1", messageId)
        message_list.append(replyListData)

    elif "Consulta documentos" in text:
        data = payloads.txt_msj(number, "Por favor ingresa tu RFC o tu código de cliente si utilizas RFC genérico:")
        message_list.append(data)

    elif "Información que cura" in text:
        body = "📱 Facebook:\nhttps://www.facebook.com/profile.php?id=100095118663417\n🖥️ Sitio web:\ngrupo-cmp.com\n📥 E-mail:\ncontacto@escalerascopernico.com\n🪜 Curso de escaleras:\nhttps://www.grupo-cmp.com/curso-de-escaleras"
        ButtonDocs=payloads.buttonDocs_Message(number, body, "sedd2", None)
        message_list.append(ButtonDocs)
        ButtonsVideo=payloads.buttonDocs_Message(number, "Videos Athena:", "sedd3", None)
        message_list.append(ButtonsVideo)
        
    elif "Teléfonos y oficina" in text:
        data = payloads.txt_msj(number, "📱 Atención a clientes:\n3333333333\n📱 Logística:\n3333333333\n📱 Llamar a crédito y cobranza:\n3333333333\n📱 Gerencia de ventas:\n3333333333\n📱 Problemas sin resolver:\n3333333333")
        message_list.append(data)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif "Productos" in text:
        body = "Selecciona el tipo de producto:"  
        replyListData = payloads.listReply_Message(number, body, None, "sedd2", messageId)
        message_list.append(replyListData)
        
    elif "Quejas y sugerencias" in text:  
        data = payloads.txt_msj(number, "📱 Llamar o enviar whatsapp:\n3333333333")
        message_list.append(data)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif text in arrays.opt:
        data = payloads.txt_msj(number, "Por favor, espera unos segundos ⏰")
        env_msj(data)
        document=payloads.document_msj(number, text, "sedd1")
        env_msj(document)
        time.sleep(5)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif text in arrays.videos:
        document=payloads.video_msj(number, text, "sedd1")
        message_list.append(document)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif text in products.all_models():
        clasification = products.clasification(text)
        data = payloads.stck_msj(number, arrays.stickers[clasification])
        env_msj(data)
        data = payloads.img_msj(number, text)
        env_msj(data)
        time.sleep(1)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)


    elif validar_rfc(text)==True and (number in arrays.numbers or str(number)==products.tel(text)) or products.codigos(text.upper())!=None and (number in arrays.numbers or str(number)==products.tel(text)):

        if(products.codigos(text.upper())!=None):
            data = payloads.txt_msj(number, "Código valido")
            env_msj(data)
            data = payloads.txt_msj(number, "En unos segundos enviare la información de pedidos y facturas ⏰")
            env_msj(data)
            text=connection.idcliente(text.upper())
            if(text[0]==None):
                documentos=connection.docscdc(text[1])
            elif(text[1]==None):
                documentos=connection.docscmp(text[0])
            else:
                documentos = connection.docscmp(text[0])+connection.docscdc(text[1])
        else:
            data = payloads.txt_msj(number, "RFC valido")
            env_msj(data)
            data = payloads.txt_msj(number, "En unos segundos enviare la información de pedidos y facturas ⏰")
            env_msj(data)
            documentos = connection.docscmp(text)+connection.docscdc(text)

        if not documentos:
            data = payloads.txt_msj(number, "Por el momento no cuentas con pedidos ni facturas en los últimos 30 días ☺️.\nPara volver al menú principal por favor escribe Hola.")
            env_msj(data)
            ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
            env_msj(ButtonsVideo)
        else:
            for documento in documentos:
                if documento['CSERIEDOCUMENTO'] == 'PCIC1' or documento['CSERIEDOCUMENTO'] == 'PCIC2':
                    mensaje = f"*Pedido*: {int(documento['CFOLIO'])}\n*Estatus*: {documento['CESTATUS']}\n*Fecha*: {documento['CFECHA']}\n*Cliente*: {documento['CRAZONSOCIAL']}\n*Agente*: {documento['CNOMBREAGENTE']}\n*Total*: {documento['CTOTAL']}"
                if documento['CSERIEDOCUMENTO'] == 'FG401' or documento['CSERIEDOCUMENTO'] == 'FG402':
                    mensaje = f"*Factura*: {int(documento['CFOLIO'])}\n*Estatus*: Entregado\n*Fecha*: {documento['CFECHA']}\n*Cliente*: {documento['CRAZONSOCIAL']}\n*Agente*: {documento['CNOMBREAGENTE']}\n*Total*: {documento['CTOTAL']}"
                id = documento['CIDDOCUMENTO']
                ButtonDocs=payloads.buttonDocs_Message(number, mensaje, "sedd1", id)
                message_list.append(ButtonDocs)
            ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
            message_list.append(ButtonsVideo)
        
    elif validar_rfc(text)==True and (number not in arrays.numbers or str(number)!=products.tel(text)):
        data = payloads.txt_msj(number, "Al parecer hubo un error al ingresar tu RFC o este numero no tiene acceso a la informacion que estas solicitando, por favor solicita tu alta al 3333333333.")
        message_list.append(data)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif text in arrays.doc:
      
        if(text=="Ver productos"):
            data = payloads.txt_msj(number, "Por favor, espera unos segundos ⏰")
            env_msj(data)
            movimientos=connection.movimientos(messageId)
            mensaje = []
            for movimiento in movimientos:
                mensaje.append(f"{movimiento['CUNIDADES']}) {movimiento['CNOMBREPRODUCTO']}")
            mensaje_texto = '\n'.join(mensaje)
            data = payloads.txt_msj(number, mensaje_texto)
            message_list.append(data)
            ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
            message_list.append(ButtonsVideo)
        elif(text=="Descargar PDF"):
            data = payloads.txt_msj(number, "Por favor, espera unos segundos ⏰")
            env_msj(data)
            cc = connection.codigocliente(int(messageId)-1)
            link = documents.buscar_en_subcarpeta(os.environ.get('ID_CARPETA_DRIVE'), cc[0], "FFG401000000"+str(cc[1]).split(".")[0]+".pdf")
            if(link==None):
                link = documents.buscar_en_subcarpeta(os.environ.get('ID_CARPETA_DRIVE'), cc[1], "FFG402000000"+str(cc.CFOLIO).split(".")[0]+".pdf")
            documents.copiar_documento(link, os.environ.get('ID_CARPETA_CACHE'))
            time.sleep(1)
            link = documents.obtener_id_nuevo("FFG401000000"+str(cc[1]).split(".")[0]+".pdf", os.environ.get('ID_CARPETA_CACHE'))
            if(link==None):
                link = documents.obtener_id_nuevo("FFG402000000"+str(cc[1]).split(".")[0]+".pdf", os.environ.get('ID_CARPETA_CACHE'))
            data = payloads.document_msj(number, link, "sedd2")
            env_msj(data)
            ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
            env_msj(ButtonsVideo)
            documents.eliminar_doc("FFG401000000"+str(cc[1]).split(".")[0]+".pdf", os.environ.get('ID_CARPETA_CACHE'))
            documents.eliminar_doc("FFG402000000"+str(cc[1]).split(".")[0]+".pdf", os.environ.get('ID_CARPETA_CACHE'))
        else:
            data = payloads.txt_msj(number, "Por favor, espera unos segundos ⏰")
            env_msj(data)
            cc = connection.codigocliente(int(messageId)-2)
            link = documents.buscar_en_subcarpeta(os.environ.get('ID_CARPETA_DRIVE'), cc[0], "FFG401000000"+str(cc[1]).split(".")[0]+".xml")
            if(link==None):
                link = documents.buscar_en_subcarpeta(os.environ.get('ID_CARPETA_DRIVE'), cc[0], "FFG402000000"+str(cc[1]).split(".")[0]+".xml")
            documents.copiar_documento(link, os.environ.get('ID_CARPETA_CACHE'))
            time.sleep(1)
            link = documents.obtener_id_nuevo("FFG401000000"+str(cc[1]).split(".")[0]+".xml", os.environ.get('ID_CARPETA_CACHE'))
            if(link==None):
                link = documents.obtener_id_nuevo("FFG402000000"+str(cc[1]).split(".")[0]+".xml", os.environ.get('ID_CARPETA_CACHE'))
            data = payloads.video_msj(number, link, "sedd2")
            env_msj(data)
            ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
            env_msj(ButtonsVideo)

    elif text in products.list_menu():
        body = "Selecciona el subtipo del producto:"
        replyListData = payloads.listReply_Message(number, body, text, "sedd3", messageId)
        message_list.append(replyListData)

    elif text in products.list_submenu():
        body = "Selecciona el modelo/código:"
        replyListData = payloads.listReply_Message(number, body, text, "sedd4", messageId)
        message_list.append(replyListData)
    
    elif "unknow_sticker" in text:
        data = payloads.replyReaction_msj(number, messageId, "👍")
        message_list.append(data)
        data = payloads.stck_msj(number, arrays.stickers["no"])
        message_list.append(data)
        data = payloads.txt_msj(number, "Aún no soy capaz de procesar tu sticker, pero espero que sea divertido ☺️")
        message_list.append(data)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        message_list.append(ButtonsVideo)

    elif text in arrays.grcs:
        data = payloads.replyReaction_msj(number, messageId, "❤️")
        env_msj(data)
        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        env_msj(ButtonsVideo)

    elif text in arrays.despidos:

        data = payloads.replyReaction_msj(number, messageId, "❤️")
        env_msj(data)

        if(text=="No ❌"):
            data = payloads.txt_msj(number, "¡Hasta pronto! Cuídate mucho ✨☺️")
            env_msj(data)
        else:
            messages = [
                {'role': 'user', 'content': 'Responderás al nombre de Athena. Sé amable y utiliza respuestas breves. Cuando recibas "gracias", "ok", "saludos", "adiós" u otra despedida relacionada a las mismas, despídete emotivamente cálida y no ofrezcas mas ayuda. Responderas a los cumplidos y elogios con buen humor. En base a lo anterior contesta lo siguiente:'+text}
            ]
            response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            data = payloads.txt_msj(number, response.choices[0].message.content)
            env_msj(data)

        data = payloads.stck_msj(number, arrays.stickers["despedida"])
        env_msj(data)
        
    else:

        openai.api_key = os.environ.get('OPENAI_KEY')

        messages = [
            {'role': 'user', 'content': 'Responderás al nombre de Athena. Sé amable en todas las respuestas y utiliza respuestas breves. Eres asistente virtual y fuiste diseñada, creada y desarrollada por Grupo CMP. Toda información que se te pida respecto a precios, descuentos, catálogo de productos (escaleras, domos, malla sombra y otros productos de ferreteria), características, pedidos, facturas y más servicios, me responderas que está en el menú de opciones y que para acceder a él debo de escribir “Hola”. Atención personalizada se puede conseguir comunicándose a los teléfonos del directorio seleccionando la opción “Teléfonos y oficina”. Más información de Grupo CMP se encuentra disponible en www.grupo-cmp.com. Responderás a las palabras desconocidas conformadas por números y letras sin espacios con un "Código incorrecto, por favor verifícalo y vuelve a intentarlo ☺️". Responderas a los cumplidos y elogios con buen humor.'}
        ]
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        messages.append({"role": "user", "content": text})

        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        data = payloads.txt_msj(number, response.choices[0].message.content)
        env_msj(data)

        ButtonsVideo=payloads.buttonDocs_Message(number, "¿Hay algo más en lo que pueda ayudarte? 🤔", "sedd4", None)
        env_msj(ButtonsVideo)

    for message_data in message_list:
        result = env_msj(message_data)
        print(result)

    return 'enviado'

def validar_rfc(texto):

    texto = texto.upper()
    
    if (len(texto) == 12 and re.match(r'^[A-Z]{3}', texto)) or \
       (len(texto) == 13 and re.match(r'^[A-Z]{4}', texto)):

        if re.match(r'^[0-9]{6}', texto[len(texto) - 9:]):
            return True
        else:
            return False
    else:
        return False

def replace_start(s):
  if s.startswith("521"):
      return "52" + s[3:]
  else:
      return s