<h1 align="center" style="font-weight: bold;">Emotion & Pet Recognizer API 🖼️🐾</h1> <p align="center"> <i>Uma API inovadora que utiliza Amazon Rekognition para identificar emoções humanas e detectar animais de estimação em imagens(exclusivo para cachorros e gatos). Para pets, a API também gera dicas personalizadas utilizando o Amazon Bedrock, proporcionando uma experiência completa e interativa para os usuários.</i> </p>


## 📖 Índice

1. [🏛️ Arquitetura](#️-arquitetura)
2. [🛠️ Tecnologias utilizadas](#️-tecnologias-utilizadas)
3. [🚀 Execução e Utilização](#-execução-e-utilização)
4. [🧱 Estrutura de Pastas](#-estrutura-de-pastas)
5. [🚧 Desafios e Dificuldades](#-desafios-e-soluções)
6. [👥 Contribuidores](#-contribuidores)

## 🏛️ Arquitetura 
Este projeto utiliza uma arquitetura serverless na AWS, integrando serviços como Rekognition e Bedrock para criar uma solução completa de reconhecimento visual e geração de informação.


<hr>
 
## 🖥 API Endpoints

### *Rota 4*: Análise de Emoções - /v1/vision
- *Método*: POST
- *URL*: /v1/vision
- *Descrição*:
Recebe uma imagem armazenada no S3 e utiliza o Amazon Rekognition para detectar emoções em faces humanas na imagem. Retorna a emoção principal para cada face detectada.

### *Rota 5*: Análise de Emoções - /v2/vision
- *Método*: POST
- *URL*: /v2/vision
- *Descrição*:
Recebe uma imagem armazenada no S3, utiliza o Amazon Rekognition para detectar emoções em faces humanas e pets. Caso um pet seja detectado, o Amazon Bedrock gera dicas baseadas nas características do pet detectado. As dicas somente serão geradas se o animal detectado for um gato ou cachorro, caso outra espécie de animal seja identificada o retorno será "Nenhum animal específico foi detectado".

## 🛠️ Tecnologias Utilizadas 
<div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=amazon&logoColor=white" />
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" />
  <img src="https://img.shields.io/badge/Amazon_Rekognition-559999?style=for-the-badge&logo=amazon&logoColor=white" />
  <img src="https://img.shields.io/badge/Amazon_Bedrock-232F3E?style=for-the-badge&logo=amazon&logoColor=white" />
  <img src="https://img.shields.io/badge/Serverless-000000?style=for-the-badge&logo=serverless&logoColor=white" />
</div>


## 🚀 Execução e Utilização
  1. Instale o framework serverless em seu computador.
     
     ```bash 
      npm install -g serverless 
     ```
     
  2. Gere suas credenciais (AWS Acess Key e AWS Secret) na console AWS pelo IAM.
     
  3. Configure o serverless com suas credenciais e conta usando o comando:
     
     ```
     serverless
     ```
     
  4. Para efetuar o deploy da solução na sua conta aws execute (acesse a pasta api):
     
     ```
     serverless deploy
     ```

  5. Resposta esperada do deploy:
      ```
     endpoints:
         GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
         GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1
         GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2
         POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1/vision
         POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v2/vision
     functions:
         health: computer-vision-api-dev-health (4 kB)
         v1Description: computer-vision-api-dev-v1Description (4 kB)
         v2Description: computer-vision-api-dev-v2Description (4 kB)
         faces: computer-vision-api-dev-faces (4 kB)
         facesPets: computer-vision-api-dev-facesPets (4 kB)
      ```
     
  6. Crie uma bucket S3 e faça o upload manual das imagens a ser analisadas.

  7. Exemplo de requisição *Rota 4*: Análise de Emoções - /v1/vision:

     ```
     {
      "bucket": "bucket-name",
      "imageName": "happy-woman.jfif"
     }
     ```

  8. Exemplo de resposta esperada:

     ```
       {
        "url_to_image": "https://bucket-name.s3.amazonaws.com/happy-woman.jfif",
        "created_image": "22-08-2024 12:30:00",
        "faces": [
          {
            "position": {
              "Width": 0.288613885641098,
              "Height": 0.6879695653915405,
              "Left": 0.35631734132766724,
              "Top": 0.10273034870624542
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 99.67448425292969
          }
        ]
      }
     ```

  9. Exemplo de requisição *Rota 5*: Análise de Emoções - /v2/vision:

     ```
     {
      "bucket": "bucket-name",
      "imageName": "cat.jfif"
     }
     ```
  10. Exemplo de resposta esperada:

     ```
       {
        "url_to_image": "https://bucket-name.s3.amazonaws.com/cat.jfif",
        "created_image": "23-08-2024 12:11:57",
        "pets": [
          {
            "labels": [
              {
                "Name": "Animal",
                "Confidence": 98.71717071533203,
                "Instances": [],
                "Parents": [],
                "Aliases": [],
                "Categories": [
                  {
                    "Name": "Animals and Pets"
                  }
                ]
              },
              {
                "Name": "Cat",
                "Confidence": 98.71717071533203,
                "Instances": [
                  {
                    "BoundingBox": {
                      "Width": 0.6766279339790344,
                      "Height": 0.8841034173965454,
                      "Left": 0.16865569353103638,
                      "Top": 0.012142295017838478
                    },
                    "Confidence": 90.90341186523438
                  }
                ],
                "Parents": [
                  {
                    "Name": "Animal"
                  },
                  {
                    "Name": "Mammal"
                  },
                  {
                    "Name": "Pet"
                  }
                ],
                "Aliases": [],
                "Categories": [
                  {
                    "Name": "Animals and Pets"
                  }
                ]
              },
              {
                "Name": "Pet",
                "Confidence": 98.71717071533203,
                "Instances": [],
                "Parents": [
                  {
                    "Name": "Animal"
                  }
                ],
                "Aliases": [],
                "Categories": [
                  {
                    "Name": "Animals and Pets"
                  }
                ]
              }
            ],
            "Dicas":
               "Gato:\n
                 - Nível de energia e necessidades de exercícios: Os gatos são conhecidos por serem independentes e ativos, mas o nível de energia pode variar de acordo com a raça e a personalidade individual. Eles precisam de tempo para brincar e se exercitar, mas geralmente são mais ativos durante a noite. Recomenda-se que os gatos tenham acesso a brinquedos e áreas de escalada para manter sua saúde física e mental.\n
                 - Temperamento e comportamento: Os gatos são animais sociais, mas também são independentes. Eles podem ser amigáveis e afetuosos, mas também podem ser mais reservados e ter seus próprios horários. É importante socializar os gatos desde tenra idade para que eles sejam mais amigáveis e afetuosos com as pessoas e outros animais.\n
                 - Cuidados e necessidades: Os gatos precisam de uma dieta balanceada e nutritiva, bem como água fresca e limpa. Eles também precisam de uma caixa de areia limpa e confortável para fazer suas necessidades. É importante cuidar das unhas do gato e dar-lhes uma escovação regular para manter sua saúde e aparência.\n
                 - Problemas de saúde comuns: Os gatos podem sofrer de uma variedade de problemas de saúde, incluindo infecções do trato urinário, doenças do fígado e do rim, e doenças do sistema respiratório. É importante levar o gato ao veterinário regularmente para exames de rotina e vacinas para evitar doenças e manter sua saúde."
          }
        ]
      }
     ```
     
## 🧱 Estrutura de Pastas 

- `api/`: Handlers e configuração do Serverless para a API.
- `rekognition/`: Lógica relacionada ao consumo do Amazon Rekognition.
- `bedrock/`: Lógica relacionada ao consumo do Amazon Bedrock.
- `assets/`: Imagens.

```
│
├── api/
│   ├── bedrock
|       └── bedrock_service.py
│   ├── rekognition
|       └── rekognition_service.py
│   ├── handler.py
│   └── serverless.yml
│
├── assets/
│   ├── arquitetura-base.jpg
└── README.md

```

## 🚧 Desafios e Dificuldades

Durante o desenvolvimento deste projeto, encontramos algumas dificuldades:

1. **Integração de AWS Rekognition e Bedrock:** Garantir que os dois serviços se comuniquem eficientemente, especialmente ao lidar com diferentes tipos de dados (emoções e dicas de animais).

2. **Gerenciamento de Erros:** Tratamento de possíveis erros durante a detecção de imagens e a geração de dicas para garantir a robustez da API.

3. **Formato de Saída:** Garantir que as dicas sejam retornadas de forma legível e que as quebras de linha funcionem corretamente nos formatos JSON.

## 👥 Contribuidores
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/SilasLeao" title="GitHub">
        <img src="https://avatars.githubusercontent.com/u/89739174?v=4" width="100px;" alt="Foto de Silas Leão"/><br>
        <sub>
          <b>Silas Leão</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/LuizManoeldev" title="GitHub">
        <img src="https://avatars.githubusercontent.com/u/88911543?v=4" width="100px;" alt="Foto de Luiz Manoel"/><br>
        <sub>
          <b>Luiz Manoel</b>
        </sub>
      </a>
    </td> 
    <td align="center">
      <a href="https://github.com/RicardoLuiz05" title="GitHub">
        <img src="https://avatars.githubusercontent.com/u/105940717?v=4" width="100px;" alt="Foto de Ricardo Luiz"/><br>
        <sub>
          <b>Ricardo Luiz</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
