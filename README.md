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


### <div align="center">Part 1 - Model Training and evaluation</div>

  - The objective is to create a sentence classification model that can categorize the contribution sentences of a research paper and use them to produce a summary.
  - The Text of research paper has been extracted and processed using **Grobid** followed by **Stanza** and each contribution sentences line number has been annotated and stored in **sentences.txt** file in the training dataset
  - The output of Stanza and line number of contribution sentences from sentences.txt file will be passed as a input to train the classification model pipeline
  - The model used here is [allenai/scibert_scivocab_uncased](https://huggingface.co/allenai/scibert_scivocab_uncased) which is specifically designed for use with scientific text, including research papers which widely matches with the training dataset of NLPContributionGraph to train a classification model
  - This can save a lot of time and effort compared to training a language model from scratch, as the pre-trained model has already learned a lot about the structure and language used in scientific text.
  - Trained Model will classify the contribution sentences and combines the classifed sentences to form a summary of the paper
  - The generated summary will be evaluvated against the abstarct of the paper as the reference summary



### Usage

  - [Model Training Notebook](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/Notebooks/ContribSentenceTraining.ipynb) This notebook contains the training and evaluvation code to train the model using NLPContributionGraph dataset
  - [Model Evaluvation](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/Notebooks/ContribSenEvaluvation.ipynb) used for evaluvating the generated summary by combining classifed contribution sentences
  - [Research paper](https://aclanthology.org/P19-1106/) used for evaluvation of the trained model




### <div align="center">Part 2 - Message broker based system using Kafka</div>
  - The PDF data will be converted into raw text using Grobid library
  - The abstract and paragraph Text will be extracted from Grobid XML output using beautiful soup
  - A producer will Create topic and sends the PDF data to the Consumer which hosts the ML model 
  - Consumer will recieve the data and convert the raw text into structured sentences using Stanza
  - The sentences will be passed to the text-classification pipeline model to classify the contributions sentences
  - The Classifed sentences will be combined to form a Summary
  - Generated summary will be evaluvated against the abstract to calcualte the rouge score
  - Abstract , Generated summary and the rouge score will be printed in the console
  
### Usage
  - [Producer](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/producer/producerkafka.py) will pass message (PDF Text and Abstract of the paper ) on topic **ContributeSentences** to the [Consumer](https://github.com/GouthamVicky/ResearchPaperSummarization/blob/main/MessageBrokerSystem/consumer/consumerkafka.py)

> The model was trained using Google Colab Pro and kafka message system has been implemented and tested on NVIDIA GeForce RTX™ 2060 SUPER GPU
> GPU is recommended for faster inference for Kafka message system

