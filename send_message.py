import boto3
import json
from botocore.config import Config

# Configurações do LocalStack
endpoint_url = 'http://localhost:4566'

# Configuração do boto3 para usar credenciais fictícias
config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Criação do cliente SQS com credenciais fictícias
sqs = boto3.client(
    'sqs',
    endpoint_url=endpoint_url,
    aws_access_key_id='fake_access_key',
    aws_secret_access_key='fake_secret_key',
    config=config
)

# Nome da fila
queue_name = 'my-queue'
response = sqs.create_queue(QueueName=queue_name)
queue_url = response['QueueUrl']

# Criação da fila
def create_messages(queue_url):
    # Mensagem a ser enviada
    message = {
        'id': 1,
        'message': 'Hello, this is a test message!'
    }

    # Envio da mensagem
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )

    print(f"Message ID: {response['MessageId']}")

# Função para listar mensagens da fila
def list_messages(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=1
    )
    
    messages = response.get('Messages', [])
    for message in messages:
        print(f"Message ID: {message['MessageId']}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        print(f"Body: {message['Body']}")
        print("------")

# Listar mensagens da fila
create_messages(queue_url)
list_messages(queue_url)