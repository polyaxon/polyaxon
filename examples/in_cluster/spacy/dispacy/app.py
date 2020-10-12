import spacy
from spacy import displacy

from polyaxon import tracking

nlp = spacy.load("en_core_web_sm")


if __name__ == "__main__":

    tracking.init()

    doc = nlp(
        """ To succeed, planning alone is insufficient.
           One must improvise as well. - Asimov
        """
    )

    html = displacy.render(doc, style="dep")

    tracking.log_html(html=html)

    displacy.serve(doc, style="dep")
