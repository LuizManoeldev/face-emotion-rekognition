import boto3

# Inicializa o cliente do Bedrock
bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")

# Traduz os nomes dos animais do inglês para o português, previnindo a geração de texto do Bedrock de retornar informações mistas em inglês e português
def translate_animal_names(animals):
    # Mapeamento de tradução dos nomes dos animais
    translation_map = {
        'Dog': 'Cachorro',
        'Cat': 'Gato'
    }
    return [translation_map.get(animal, animal) for animal in animals]

# Gera dicas sobre os animais específicos detectados utilizando o Bedrock.
def generate_pet_tips(specific_animals):
    # Traduz os nomes dos animais para português
    translated_animals = translate_animal_names(specific_animals)
    # Cria um prompt único apenas para os animais específicos detectados
    pet_description_combined = ", ".join(translated_animals)
    
    bedrock_prompt = f"""
    Você é um expert de pets. Me dê dicas sobre os seguintes pets: {pet_description_combined}. Retorne as respostas dos seguintes pontos para cada um, especificando o nome do animal na primeira linha. Por favor, responda em português:
    - Nível de energia e necessidades de exercícios
    - Temperamento e comportamento
    - Cuidados e necessidades
    - Problemas de saúde comuns
    """

    conversation = [
        {
            "role": "user",
            "content": [{"text": bedrock_prompt}],
        }
    ]

    # Chamada ao Bedrock para gerar as dicas
    response = bedrock_client.converse(
        modelId="amazon.titan-text-premier-v1:0",
        messages=conversation,
        inferenceConfig={"maxTokens": 1024, "stopSequences": [], "temperature": 0, "topP": 0.9},
        additionalModelRequestFields={}
    )

    # Extraia a resposta do Bedrock
    pet_tips = response["output"]["message"]["content"][0]["text"]
    
    return pet_tips
