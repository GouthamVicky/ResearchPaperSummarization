### <div align="center">Part 2 - Message broker based system using Kafka</div>
  - The PDF data will be converted into raw text using Grobid library
  - The abstract and paragraph Text will be extracted from Grobid XML output using beautiful soup
  - A producer will Create topic and sends the PDF data to the Consumer which hosts the ML model 
  - Consumer will recieve the data and convert the raw text into structured sentences using Stanza
  - The sentences will be passed to the text-classification pipeline model to classify the contributions sentences
  - The Classifed sentences will be combined to form a Summary
  - Generated summary will be evaluvated against the abstract to calcualte the rouge score
  - Abstract , Generated summary and the rouge score will be printed in the console
