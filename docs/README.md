# Building the documentation

- install MkDocs: `pip install mkdocs`
- install MKDocs material theme: `pip install mkdocs-material`, `pip install pygments`, and `pip install pymdown-extensions` 
- `cd` to the `docs/` folder and run:
    - `python generate_doc.py`
    - `mkdocs build`    # Builds a static site in "site" directory
    - `mkdocs serve`    # Starts a local webserver:  [localhost:8000](localhost:8000)
