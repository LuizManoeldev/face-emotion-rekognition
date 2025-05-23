import boto3
from datetime import datetime

# Criação do cliente para o serviço Rekognition da AWS
client = boto3.client('rekognition')

# Criação do cliente para o serviço S3 da AWS
s3_client = boto3.client('s3')

# Detecta faces em uma imagem armazenada em um bucket S3 e retorna informações sobre essas faces.
def detect_faces(bucket_name, image_name):

    # Obtém a resposta da análise facial
    rek_response = rekognition_facial_analysis(bucket_name, image_name)

    # Para analise no CloudWatch
    print(rek_response)

    # Filtra os dados das faces detectadas
    faces_data = faces_response_filter(rek_response)

    response_data = {
        "url_to_image": s3_url_formatter(bucket_name, image_name),
        "created_image": get_s3_metadata(bucket_name, image_name).strftime("%d-%m-%Y %H:%M:%S"),
        "faces": faces_data
    }

    return response_data

# Detecta faces e animais em uma imagem armazenada em um bucket S3 e retorna informações sobre esses objetos.
def detect_faces_and_pets(bucket_name, image_name):
    
    # Obtém a resposta da detecção de rótulos (labels)
    rek_response = rekognition_label_detection(bucket_name, image_name)

    #print(rek_response)

    # Filtra rótulos detectados para animais
    detected_pets = label_filter(rek_response, ["Animal", "Dog", "Cat", "Pet"])

    # Filtra rótulos detectados para pessoas
    detected_persons = label_filter(rek_response, ["Person", "Human"])

    response_data = {}

    # Verifica a presença de pessoas e pets e organiza a resposta
    pet_info = ""

    #  Quando são detectadas pessoas e animais na imagem, o dicionário 'response_data' é preenchido com informações sobre as pessoas e animais detectados na imagem.
    if (detected_persons and detected_pets):
        response_data = {
            "persons": detect_faces(bucket_name, image_name),
            "pets": [
                {
                    "labels": pets_response_filter(detected_pets),
                    "Dicas": pet_info
                }
            ]
        }
    # Quando são detectadas apenas pessoas na imagem, o dicionário 'response_data' é preenchido apenas com informações sobre as pessoas detectadas na imagem.
    if (detected_persons and not detected_pets):
        response_data = detect_faces(bucket_name, image_name)
    
    # Quando são detectados apenas animais na imagem, o dicionário 'response_data' é preenchido com a URL da imagem armazenada no S3, a data de criação da imagem e informações sobre os animais detectados.
    if (detected_pets and not detected_persons):
        response_data = {
            "url_to_image": s3_url_formatter(bucket_name, image_name),
            "created_image": get_s3_metadata(bucket_name, image_name).strftime("%d-%m-%Y %H:%M:%S"),
            "pets": [
                {
                    "labels": pets_response_filter(detected_pets),
                    "Dicas": pet_info
                }
            ]
        }
        
    return response_data
 
# Realiza a detecção de faces em uma imagem usando o serviço Rekognition.
def rekognition_facial_analysis(bucket_name, image_name):
    response = client.detect_faces(
    Image={
        'S3Object': {
            'Bucket': bucket_name,  
            'Name': image_name,           
        }
    },
    Attributes=[
        'ALL'  # Usa 'ALL' para obter todos os atributos faciais possíveis, incluindo emoções
    ])

    return response

# Realiza a detecção de rótulos em uma imagem usando o serviço Rekognition.
def rekognition_label_detection(bucket_name, image_name):
    response = client.detect_labels(
    Image={
        'S3Object': {
            'Bucket': bucket_name, 
            'Name': image_name,           
        }
    })

    return response

# Filtra e organiza os dados das faces detectadas.
def faces_response_filter(response):
    faces_data = []
    for face in response['FaceDetails']:
        emotions = face['Emotions']
        classified_emotion = max(emotions, key=lambda e: e['Confidence'])
        face_data = {
            "position": face['BoundingBox'],
            "classified_emotion": classified_emotion['Type'],
            "classified_emotion_confidence": classified_emotion['Confidence']
        }
        faces_data.append(face_data)

    return faces_data

def pets_response_filter(response):
    pets_data = []
    for label in response:
        # Verifica se o nome do rótulo está na lista de interesse
        if label['Name'] in ['Animal', 'Dog', 'Pet', 'Cat']:
            pet_data = {
                "Confidence": label['Confidence'],
                "Name": label['Name'],
            }
            pets_data.append(pet_data)

    return pets_data

def label_filter(response, labels):
    detected_labels = [label for label in response['Labels'] if label['Name'] in labels]
    return detected_labels

# Formata a URL para acessar uma imagem armazenada em um bucket S3.
def s3_url_formatter(bucket_name, image_name):
    return f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

# Obtém os metadados da imagem armazenada em um bucket S3, incluindo a data de criação.
def get_s3_metadata(bucket_name, image_name):
    s3_object = s3_client.head_object(Bucket=bucket_name, Key=image_name)
    return s3_object['LastModified']


detect_faces_and_pets("galeria-grupo-7", "dog.jpg")