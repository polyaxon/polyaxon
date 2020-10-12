import random
import spacy
from spacy.util import minibatch, compounding

from polyaxon import tracking

TRAIN_DATA = [
    ("Polyaxon is a Data Science Platform", {"entities": [(0, 8, "ORG")]}),
    (
        "Polyaxon provides painless experimentation process with minimal infrastructure work",
        {"entities": [(0, 8, "ORG")]},
    ),
]


def train_model(n_iter: int = 100) -> None:

    # You can load other languages if specificied in Dockerfile
    nlp = spacy.load("en_core_web_sm")

    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    # only train NER
    with nlp.disable_pipes(*other_pipes):
        nlp.begin_training()
        for step_n in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(1.0, 4.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts, annotations, drop=0.5, losses=losses,
                )
            print("Losses: ", losses)
            tracking.log_metrics(step=step_n, **losses)

    nlp.to_disk("custom_spacy_model")


if __name__ == "__main__":

    tracking.init()

    _ = train_model(n_iter=50)

    custom_model = spacy.load("custom_spacy_model")

    for text, _ in TRAIN_DATA:
        doc = custom_model(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    tracking.log_dir_ref("custom_spacy_model")
