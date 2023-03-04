from transformers import BartTokenizer, BartModel
import torch.nn.functional as F
import torch

# Load a pre-trained BART model and tokenizer
model = BartModel.from_pretrained('facebook/bart-large')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')


abstract = "Automatically validating a research artefact is one of the frontiers in Artificial Intelligence (AI) that directly brings it close to competing with human intellect and intuition. Although criticised sometimes, the existing peer review system still stands as the benchmark of research validation. The present-day peer review process is not straightforward and demands profound domain knowledge, expertise, and intelligence of human reviewer(s), which is somewhat elusive with the current state of AI. However, the peer review texts, which contain rich sentiment information of the reviewer, reflecting his/her overall attitude towards the research in the paper, could be a valuable entity to predict the acceptance or rejection of the manuscript under consideration. Here in this work, we investigate the role of reviewer sentiment embedded within peer review texts to predict the peer review outcome. Our proposed deep neural architecture takes into account three channels of information: the paper, the corresponding reviews, and the review’s polarity to predict the overall recommendation score as well as the final decision. We achieve significant performance improvement over the baselines (∼ 29% error reduction) proposed in a recently released dataset of peer reviews. An AI of this kind could assist the editors/program chairs as an additional layer of confidence, especially when non-responding/missing reviewers are frequent in present-day peer reviews."
reference = "The evaluation shows that our proposed model successfully outperforms the earlier reported results in PeerRead.Finally, we fuse the extracted review sentiment feature and joint paper + review representation together to generate the overall recommendation score ( Decision - Level Fusion ) using the affine transformation asWe employ a grid search for hyperparameter optimization.For Task 1 , F is 256 , l is 5 . ReLU is the non-linear function g( ) , and the learning rate is 0.007. We train the model with SGD optimizer and set momentum as 0.9 and batch size as 32 . We keep dropout at 0.5. Again we train the model with Adam Optimizer, keep the batch size as 64 and use 0.7 as the dropout rate to prevent overfitting . With only using review + sentiment information, we are still able to outperform Kang et al. ( 2018 ) by a margin of 11 % in terms of RMSE. However, we also find that our approach with only Review + Sentiment performs inferior to the Paper + Review method in Kang et al. ( 2018 ) for ACL 2017. Transformation-based Models of Video SequencesAct are the output activations from the final layer of MLP Senti which are augmented to the decision layer for final recommendation score prediction."

# Tokenize the sentences
inputs = tokenizer([abstract, reference], return_tensors='pt', padding=True, truncation=True)

# Generate embeddings for the sentences
outputs = model(**inputs)[0]
sentence1_embedding = outputs[0, 1, :]
sentence2_embedding = outputs[0, 0, :]

# Calculate the cosine similarity between the embeddings
cosine_similarity = F.cosine_similarity(sentence1_embedding.unsqueeze(0), sentence2_embedding.unsqueeze(0)).item()

print("BART score:", cosine_similarity)

#Bart Score :  0.9999998211860657