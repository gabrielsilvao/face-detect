import os
from flask import Flask, request
import boto3

app = Flask(__name__)

# Configuração do cliente S3
s3_client = boto3.client('s3')

# Configuração do cliente Rekognition
rek_client = boto3.client('rekognition')

@app.route('/')
def index():
    return '''
        <html>
            <body>
                <form action="/verificar_rosto" method="post" enctype="multipart/form-data">
                    <input type="file" name="file1">
                    <input type="file" name="file2">
                    <input type="submit" value="Verificar">
                </form>
            </body>
        </html>
    '''

@app.route('/verificar_rosto', methods=['POST'])
def verificar_rosto():
    # Obtém as imagens enviadas pelo usuário
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Verifica se as imagens foram enviadas
    if file1 and file2:
        # Define os nomes dos arquivos que serão salvos no bucket
        filename1 = file1.filename
        filename2 = file2.filename

        # Define o nome do bucket da AWS onde serão salvos os arquivos
        bucket_name = 'silva-bucket-img-reko'

        # Faz o upload das imagens para o S3
        s3_client.upload_fileobj(file1, bucket_name, filename1)
        s3_client.upload_fileobj(file2, bucket_name, filename2)

        # Define os parâmetros de comparação de rostos
        parameters = {
            'SimilarityThreshold': 90,
            'SourceImage': {
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': filename1
                }
            },
            'TargetImage': {
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': filename2
                }
            }
        }

        # Executa a comparação de rostos usando o Amazon Rekognition
        response = rek_client.compare_faces(**parameters)

        objects_to_delete = [
                filename1,
                filename2
            ]

        for obj in objects_to_delete:
            s3_client.delete_object(Bucket=bucket_name, Key=obj)

        # Verifica se as imagens contêm o mesmo rosto
        if response['FaceMatches']:
            return 'As imagens contêm a mesma pessoa.'
        else:
            return 'As imagens contêm pessoas diferentes.'


    else:
        return 'Selecione duas imagens para verificar.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')