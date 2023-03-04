import os
import json
from confluent_kafka import Producer
import logging


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Set up Kafka producer
producer = Producer({'bootstrap.servers':'localhost:9092'})

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

#####################
print('Kafka Producer has been initiated...')


def main():
    
    # Get list of PDF files in directory
    pdf_dir = 'pdfFiles'
    pdf_files = os.listdir(pdf_dir)

    # Send each PDF file to Kafka broker
    for file in pdf_files:
        with open(os.path.join(pdf_dir, file), 'rb') as f:
            pdf_data = f.read()
        message = {'filename': file, 'data': pdf_data}
        producer.poll(1)
        producer.produce('ContributeSentences', json.dumps(message).encode('utf-8'))
        producer.flush()

if __name__ == '__main__':
    main()