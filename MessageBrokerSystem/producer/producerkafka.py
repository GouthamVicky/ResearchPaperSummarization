import os
import json
from confluent_kafka import Producer
import logging
import base64
from grobidparser import detectAbstractParagraph
import time
import requests

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Set up Kafka producer
producer = Producer({'bootstrap.servers':'localhost:9092','message.max.bytes': 10485880 })

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} \n'.format(msg.topic())
        logger.info(message)
        print(message)

#####################
print('Kafka Producer has been initiated...')
# Set up the Grobid API endpoint
grobid_url = 'http://localhost:8070/api/processFulltextDocument'

def main():
    
    # Get list of PDF files in directory
    pdf_dir = 'pdfFiles'
    pdf_files = os.listdir(pdf_dir)

    # Send each PDF file to Kafka broker
    for file in pdf_files:
        with open(os.path.join(pdf_dir, file), 'rb') as f:
            pdf_data = f.read()
        
        headers = {'Content-Type': 'application/pdf'}
        response = requests.post(grobid_url, headers=headers, data=pdf_data)
        abstract,paragraphText=detectAbstractParagraph(response)
        
        message = {'filename': file, 'abstract': abstract, "paragraphText": paragraphText}
        
        producer.poll(1)
        producer.produce('ContributeSentences', json.dumps(message).encode('utf-8'),callback=receipt)
        producer.flush()

if __name__ == '__main__':
    main()