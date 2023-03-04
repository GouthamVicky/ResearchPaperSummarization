import json
import requests

import numpy as np
from confluent_kafka import Consumer,Producer
from grobidparser import detectAbstractParagraph
from generateSummaryandMetrics import summaryGenerator,summaryMetrics

from sentencebreak import process_stanza


# Set up Kafka consumer
consumer = Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})

print('Available topics to consume: ', consumer.list_topics().topics)

consumer.subscribe(['ContributeSentences'])
# Set up Kafka producer
producer = Producer({'bootstrap.servers':'localhost:9092'})



# Set up the Grobid API endpoint
grobid_url = 'http://localhost:8070/api/processFulltextDocument'


def main():
    
    while True:
        message=consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            print('Error: {}'.format(message.error()))
            continue
        # Extract PDF data from message
        pdf_message = json.loads(message.value.decode('utf-8'))
        pdf_data = pdf_message['data']
        pdf_filename = pdf_message['filename']
        
        # Extract text from PDF using Grobid
        headers = {'Content-Type': 'application/pdf'}
        response = requests.post(grobid_url, headers=headers, data=pdf_data)
        
        abstract,paragraphText=detectAbstractParagraph(response)
        
        
        #Sentence processing using Stanza
        sentences=process_stanza(paragraphText)
        
        # Extract contributions using ML model
        summary= summaryGenerator(sentences)
        
        # Publish results to Kafka broker
        
        rouge_scores=summaryMetrics(summary,abstract)
        
        
        result_message = {'filename': pdf_filename, 'Abstract':abstract,'generatedSummary': summary, 'rouge_scores': rouge_scores}
        producer.poll(1)
        producer.produce('ContributeSentences', json.dumps(result_message).encode('utf-8'))
        producer.flush()
        
        # Print results to console 
        print(result_message)