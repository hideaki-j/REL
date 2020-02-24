import requests
from REL.training_datasets import TrainingEvaluationDatasets
import numpy as np

np.random.seed(seed=42)

base_url = "C:/Users/mickv/desktop/data_back/"
wiki_version = "wiki_2019"
datasets = TrainingEvaluationDatasets(base_url, wiki_version).load()['aida_testB']

random_docs = np.random.choice(list(datasets.keys()), 100)

docs = {}
for i, doc in enumerate(random_docs):
    sentences = []
    for x in datasets[doc]:
        if x['sentence'] not in sentences:
            sentences.append(x['sentence'])
    text = '. '.join([x for x in sentences])
    docs[doc] = [text, []]
    # Demo script that can be used to query the API.
    myjson = {
        "text": text,
        "spans": [
            # {"start": 41, "length": 16}
        ],
    }
    print('----------------------------')
    print('Input API:')
    print(myjson)

    print('Output API:')
    print(requests.post("http://localhost:5555", json=myjson).json())
    print('----------------------------')


# --------------------- Now total --------------------------------
import flair
import torch

from flair.models import SequenceTagger

from REL.mention_detection import MentionDetection
from REL.entity_disambiguation import EntityDisambiguation
from time import time

base_url = "C:/Users/mickv/desktop/data_back/"

flair.device = torch.device('cpu')

mention_detection = MentionDetection(base_url, wiki_version)

# Alternatively use Flair NER tagger.
tagger_ner = SequenceTagger.load("ner-fast")

start = time()
mentions_dataset, n_mentions = mention_detection.find_mentions(docs, tagger_ner)
print('MD took: {}'.format(time() - start))

# 3. Load model.
config = {
    "mode": "eval",
    "model_path": "{}/{}/generated/model".format(
        base_url, wiki_version
    ),
}
model = EntityDisambiguation(base_url, wiki_version, config)

# 4. Entity disambiguation.
start = time()
predictions, timing = model.predict(mentions_dataset)
print('ED took: {}'.format(time() - start))