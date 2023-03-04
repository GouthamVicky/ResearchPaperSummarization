# Research Paper Summarization using Contribution Sentences

## Dataset

NLPContributionGraph was introduced as Task 11 at SemEval 2021 for the first time. The task is defined on a dataset of Natural Language Processing (NLP) scholarly articles with their contributions structured to be integrable within Knowledge Graph infrastructures such as the Open Research Knowledge Graph. 

## Prerequisite

Clone repo and install [requirements.txt]([https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/prerequisite/requirements.txt](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/prerequisite/requirements.txt)) in a
[**Python>=3.7.0**](https://www.python.org/) environment

```bash
git clone https://github.com/GouthamVicky/ResearchPaperSummarization  # clone
cd prerequisite
pip install -r requirements.txt  # install
```
Refer this Link to install Docker - [Installation steps](https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-20-04/) 

**To Start the Kafka Producer , Consumer and Grobid Container**

```bash
cd prerequisite
sudo docker-compose up -d
```
## Propsosed Solution

In the Training Dataset for every Research paper, The Raw Text has been extracted from the PDF using [Grobid](https://github.com/kermitt2/grobid) and passed to [Stanza](https://github.com/stanfordnlp/stanza) which provides formatted text in the text file format and contribution sentences from the paper has been annoted and stored as a seperate text file


Our Task is to build model to classify the contribution sentences from the paper and generate a summary using the contribution sentences


**Required Dataset**

  - [articlename].pdf                      # scholarly article pdf
       
  - [articlename]-Grobid-out.txt           # plaintext output from the [Grobid parser](https://github.com/kermitt2/grobid)
       
  - [articlename]-Stanza-out.txt           # plaintext preprocessed output from [Stanza](https://github.com/stanfordnlp/stanza)
         
  - sentences.txt                          # annotated Contribution sentences in the file


### **Part 1 - Model Training and evaluation**
  - [Model Training Notebook](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/Notebooks/ContribSentenceTraining.ipynb) This notebook contains the training and evaluvation code to train the model using NLPContributionGraph dataset
  - [Model Evaluvation](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/Notebooks/ContribSenEvaluvation.ipynb) used for evaluvating the generated summary by combining classifed contribution sentences
  - [Research paper](https://aclanthology.org/P19-1106/) used for evaluvation of the trained model

### Model Card

#### Model Card Link - https://huggingface.co/Goutham-Vignesh/ContributionSentClassification-scibert

Performs sentence classification to determine whether a given sentence is a contribution sentence or not from the research paper

### Model Description

- **Model type:** text-classification
- **Language(s) (NLP):** EN
- **Finetuned from model:** allenai/scibert_scivocab_uncased


### How to Get Started with the Model

Use the code below to get started with the model.
```bash
from transformers import pipeline
from transformers import BertTokenizer, BertForSequenceClassification
model = BertForSequenceClassification.from_pretrained("Goutham-Vignesh/ContributionSentClassification-scibert")

tokenizer=BertTokenizer.from_pretrained('Goutham-Vignesh/ContributionSentClassification-scibert')
text_classification = pipeline('text-classification', model=model, tokenizer=tokenizer)
```


### **Part 2 - Message broker based system using Kafka**
#### Producer Pipeline

  - [Producer](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/producer/producerkafka.py) will pass message (PDF Text and Abstract of the paper ) on topic **ContributeSentences** to the [Consumer](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/consumer/consumerkafka.py)
  - [PDF Files](https://github.com/GouthamVicky/ResearchPaperSummarization/tree/main/MessageBrokerSystem/producer/pdfFiles) directory containing PDF files to be passed to the consumer
  - [Gradio Parser](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/producer/grobidparser.py) is used to extract Abstract and paragraph text from the PDF using beautiful soup parsed on Gradio XML output

#### Consumer Pipeline

  - [Consumer](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/consumer/consumerkafka.py) which hosts the ML model will extract the contribution statements and generates summary along with various ROUGE scores by comparison with abstract of the paper.


### **Usage**

   - Place the PDF inside the [pdfFiles](https://github.com/GouthamVicky/ResearchPaperSummarization/tree/main/MessageBrokerSystem/producer/pdfFiles)

   - Open a Terminal and run the following command to intialize the producer/publisher
```bash
cd MessageBrokerSystem/producer/
python producerkafka.py
```

   - Open New Terminal and run the following command to start the consumer pipeline which hosts the ML model
```bash
cd MessageBrokerSystem/consumer/
python consumerkafka.py
```

> The model was trained using Google Colab Pro and kafka message system has been implemented and tested on NVIDIA GeForce RTX™ 2060 SUPER GPU
> GPU is recommended for faster inference for Kafka message system

