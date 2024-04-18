import products
import json
import arrays

def txt_msj(number, text):

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text":{
                "body": text
            }
        }
    )
    return data

def img_msj(number, codigo):

    id = str(products.iddrive(codigo))
    description = products.desc(codigo)

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "image",
            "image": {
                "caption": description,
                "link": "https://drive.google.com/uc?export=download&id="+id
            }
        }
    )
    return data
  
def stck_msj(number, sticker):

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker
            }
        }
    )
    return data
  
def document_msj(number, body, sedd):

    id=""
    name=""

    if(sedd=="sedd1"):
        if(body=="Descargar manual"):
            id="1kcl1qsTiNP8iUOcBCem2H7DkCY33b4cy"
            name="Manual"
        if(body=="Descargar catálogo"):
            id="152Ohy5TMWeTS4Lk763pzItlbvTx4CRG7"
            name="Catalogo"
        if(body=="Descargar cobertura"):
            id="1UJMK5Hpo3-T3mCv_lzQObgelnFJwiYg-"
            name="Cobertura"
    if(sedd=="sedd2"):
        id=body
        name="Factura"

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": "https://drive.google.com/uc?export=download&id="+id,
                "filename": name
            }
        }
    )

    return data
  
def replyReaction_msj(number, id, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction":{
                "message_id": id,
                "emoji": emoji
            }
        }
    )
    return data

def video_msj(number, body, sedd):

    if(sedd=="sedd1"):
        for i in range(len(arrays.videos)):
            if(body==arrays.videos[i]):
                if(i>0):
                    link="https://drive.google.com/uc?export=download&id=xxxxx"
                else:
                    link="https://drive.google.com/uc?export=download&id=xxxxx"
    if(sedd=="sedd2"):
        link="https://drive.google.com/file/d/"+body+"/view"
        body="XML"

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": body+":\n"+link
            }
        }
    )
    return data

def buttonDocs_Message(number, body, sedd, id):

    options = []

    if(sedd=="sedd1"):
        if(body.startswith("*Pedido*:")):
            options.append(
                {
                    "type": "reply",
                    "reply": {
                    "id": id,
                    "title": arrays.doc[0]
                    }
                }
            )
        else:
            sum=0
            for i in arrays.doc:
                options.append(
                    {
                        "type": "reply",
                        "reply": {
                        "id": id+sum,
                        "title": i
                        }
                    }
                )
                sum=sum+1
    if(sedd=="sedd2"):
        for i in arrays.opt:
            options.append(
                {
                    "type": "reply",
                    "reply": {
                    "id": str(i),
                    "title": i
                    }
                }
            )
    if(sedd=="sedd3"):
        for i in arrays.videos:
            options.append(
                {
                    "type": "reply",
                    "reply": {
                    "id": str(i),
                    "title": i
                    }
                }
            )
    if(sedd=="sedd4"):
        for i in arrays.resp:
            options.append(
                {
                    "type": "reply",
                    "reply": {
                    "id": str(i),
                    "title": i
                    }
                }
            )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "action": {
                    "buttons": options
                }
            }
        }
    )
    return data

def listReply_Message(number, body, option, sedd, messageId):

    options = []

    if(sedd=="sedd1"):
        for i in arrays.opc:
            options.append(
                {
                    "id": str(i),
                    "title": i["title"],
                    "description": i["description"]
                }
            )
    if(sedd=="sedd2"):
        for i in products.list_menu():
            options.append(
                {
                    "id": str(i),
                    "title": i
                }
            )
    if(sedd=="sedd3"):
        for i in products.list_products(option):
            options.append(
                {
                    "id": str(i),
                    "title": " ",
                    "description": i
                }
            )
    if(sedd=="sedd4"):
        for i in products.list_models(option)[0]:
            options.append(
                {
                    "id": str(i),
                    "title": i["title"],
                    "description": i["description"]
                }
            )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {
                "message_id": "<MSGID_OF_PREV_MSG>"
            },
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "action": {
                    "button": "Menú",
                    "sections": [
                        {
                            "title": "Opciones",
                            "rows": options
                        }
                    ]
                }
            }
        }
    )
    return data