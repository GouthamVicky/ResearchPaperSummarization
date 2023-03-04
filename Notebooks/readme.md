### <div align="center">Part 1 - Model Training and evaluation</div>

  - The objective is to create a sentence classification model that can categorize the contribution sentences of a research paper and use them to produce a summary.
  - The Text of research paper has been extracted and processed using **Grobid** followed by **Stanza** and each contribution sentences line number has been annotated and stored in **sentences.txt** file in the training dataset
  - The output of Stanza and line number of contribution sentences from sentences.txt file will be passed as a input to train the classification model pipeline
  - The model used here is [allenai/scibert_scivocab_uncased](https://huggingface.co/allenai/scibert_scivocab_uncased) which is specifically designed for use with scientific text, including research papers which widely matches with the training dataset of NLPContributionGraph to train a classification model
  - This can save a lot of time and effort compared to training a language model from scratch, as the pre-trained model has already learned a lot about the structure and language used in scientific text.
  - Trained Model will classify the contribution sentences and combines the classifed sentences to form a summary of the paper
  - The generated summary will be evaluvated against the abstarct of the paper as the reference summary
