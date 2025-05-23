import json
from rekognition.rekognition_service import detect_faces, detect_faces_and_pets
from bedrock.bedrock_service import generate_pet_tips, translate_animal_names

# Endpoint para verificar o status da função.
def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

# Endpoint para fornecer a descrição da versão 1 da API.
def v1_description(event, context):
    body = {
        "message": "VISION api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

# Endpoint para fornecer a descrição da versão 2 da API.
def v2_description(event, context):
    body = {
        "message": "VISION api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

# Filtra os rótulos dos animais específicos, para aceitar apenas 'Dog' e 'Cat', da lista fornecida.
def filter_specific_animals(labels):
    # Filtra apenas os rótulos específicos 'Dog' e 'Cat'
    specific_animals = []
    for label in labels:
        if label['Name'] in ['Dog', 'Cat']:
            specific_animals.append(label['Name'])
    return specific_animals

# Endpoint para detectar rostos em uma imagem usando o serviço Rekognition.
def faces(event, context):
    try:
        # Verifica a estrutura do evento
        body = json.loads(event.get('body', '{}'))
        
        # Obtém valores do corpo
        bucket_name = body.get('bucket')
        image_name = body.get('imageName')

        # Valida se os parâmetros necessários estão presentes
        if not bucket_name or not image_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'bucket' or 'imageName' in the request body"})
            }

        # Chama a função para detectar faces
        response_body = detect_faces(bucket_name, image_name)
        
        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return response

# Endpoint para detectar rostos e animais em uma imagem e gerar dicas para os animais detectados.
def facesPets(event, context):
    try:
        # Verifica a estrutura do evento
        body = json.loads(event.get('body', '{}'))
        
        # Obtém valores do corpo
        bucket_name = body.get('bucket')
        image_name = body.get('imageName')

        # Valida se os parâmetros necessários estão presentes
        if not bucket_name or not image_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'bucket' or 'imageName' in the request body"})
            }

        # Chama a função para detectar faces e pets
        response_body = detect_faces_and_pets(bucket_name, image_name)
        
        # Gera dicas para pets usando Bedrock
        if 'pets' in response_body:
            specific_animals = filter_specific_animals(response_body['pets'][0]['labels'])
            if specific_animals:
                response_body['pets'][0]['Dicas'] = generate_pet_tips(specific_animals)
            else:
                response_body['pets'][0]['Dicas'] = "Nenhum animal específico foi detectado."

        response = {
            "statusCode": 200,
            "body": json.dumps(response_body)
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return response
