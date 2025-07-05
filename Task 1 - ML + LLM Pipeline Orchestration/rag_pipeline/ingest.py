import pandas as pd
import pdfplumber

def ingest_csv(path):
    return pd.read_csv(path)

def ingest_pdf(path):
    with pdfplumber.open(path) as pdf:
        texts = [page.extract_text() for page in pdf.pages]
    return "\n".join(texts)