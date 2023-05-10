import boto3

# Cria uma instância do cliente S3
s3 = boto3.client('s3')

# Nome do bucket que contém os objetos que serão excluídos
bucket_name = 'silva-bucket-img-reko'

# Lista com os nomes dos objetos que serão excluídos
objects_to_delete = ['perfil1.jpeg', 'perfil2.jpg']

# Loop para excluir cada objeto
for obj in objects_to_delete:
    s3.delete_object(Bucket=bucket_name, Key=obj)
    print(f'O objeto {obj} foi excluído com sucesso do bucket {bucket_name}.')