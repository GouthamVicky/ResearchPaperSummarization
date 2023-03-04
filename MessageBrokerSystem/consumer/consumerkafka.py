import json
import requests

import numpy as np
from confluent_kafka import Consumer,Producer
from generateSummaryandMetrics import summaryGenerator,summaryMetrics

from sentencebreak import process_stanza


# Set up Kafka consumer
consumer = Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest','message.max.bytes': 1000000})

print('Available topics to consume: ', consumer.list_topics().topics)

consumer.subscribe(['ContributeSentences'])


def main():
    
    while True:
        message=consumer.poll(1.0)
        if message is None:
            print('No message received')
            continue
        if message.error():
            print('Error: {}'.format(message.error()))
            continue
        # Extract PDF data from message
        pdf_message = json.loads(message.value().decode('utf-8'))
        
        pdf_filename = pdf_message['filename']
        
        paragraphText=pdf_message['paragraphText']
        abstract=pdf_message['abstract']
        
        
        
        
        #Sentence processing using Stanza
        sentences=process_stanza(paragraphText)
        
        # Extract contributions using ML model
        summary= summaryGenerator(sentences)
        
        # Publish results to Kafka broker
        
        rouge_scores=summaryMetrics(summary,abstract)
        
        
        result_message = {'filename': pdf_filename, 'Abstract':abstract,'generatedSummary': summary, 'rouge_scores': rouge_scores}
        
        
        # Print results to console 
        print(result_message)
       
    main()