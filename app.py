from flask import Flask, request
import os
from services import obtener, obtener_id, administrar_chatbot, replace_start

app = Flask(__name__);

@app.route('/', methods=['GET'])
def bienvenido():
    return  'Hola Mundo'

@app.route('/webhook', methods=['GET'])
def token():
    try:
        token=request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == os.environ.get('WHATSAPP_TOKEN') and challenge != None:
            return  challenge
        else:
            return 'Token incorrecto', 403
    except Exception as e:
        return e, 403

@app.route('/webhook', methods=['POST'])
def recibir():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = replace_start(message['from'])
        messageId = obtener_id(message)
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = obtener(message)

        administrar_chatbot(text, number, messageId, name)

        return 'enviado'
    
    except Exception as e:
        return 'no enviado ' + str(e)

if __name__ == '__main__':
    app.run()