import pandas as pd
import pdfplumber

# Schema/context descriptions for both datasets
TITANIC_SCHEMA = """Pclass: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
Sex: Sex
Age: Age in years
SibSp: # of siblings / spouses aboard the Titanic
Parch: # of parents / children aboard the Titanic
Fare: Passenger fare
Cabin: Cabin number
Embarked: Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)
Survived: Survival (0 = No; 1 = Yes)
"""

WINE_SCHEMA = """fixed acidity: most acids involved with wine or fixed or nonvolatile (do not evaporate readily)
volatile acidity: the amount of acetic acid in wine, which at too high of levels can lead to an unpleasant, vinegar taste
citric acid: found in small quantities, citric acid can add 'freshness' and flavor to wines
residual sugar: the amount of sugar remaining after fermentation stops, it's rare to find wines with less than 1 gram/liter and wines with greater than 45 grams/liter are considered sweet
chlorides: the amount of salt in the wine
free sulfur dioxide: the free form of SO2 exists in equilibrium between molecular SO2 (as a dissolved gas) and bisulfite ion; it prevents microbial growth and the oxidation of wine
total sulfur dioxide: amount of free and bound forms of SO2; at free SO2 concentrations over 50 ppm, wines may be subject to unpleasant odors
density: the density of water is close to that of water depending on the percent alcohol and sugar content
pH: describes how acidic or basic a wine is on a scale from 0 (very acidic) to 14 (very basic)
sulphates: a wine additive which can contribute to sulfur dioxide gas (SO2) levels, acts as an antimicrobial and antioxidant
alcohol: the percent alcohol content of the wine
quality: output variable (score between 0 and 10)
"""

def ingest_csv(path, dataset=None):
    """
    Ingest CSV for both Titanic and Wine Quality datasets.
    - Adds a schema/context chunk as the first chunk for best RAG performance.
    - dataset: str, either "titanic" or "wine" (case-insensitive)
    """
    df = pd.read_csv(path)
    # Each row as a string for chunking (header included in every row for more context)
    header = " ".join(list(df.columns))
    row_chunks = df.astype(str).apply(lambda row: header + " " + " ".join(row), axis=1).tolist()

    # Add dataset schema/context as the first chunk
    schema_chunk = ""
    if dataset is not None:
        if dataset.lower() == "titanic":
            schema_chunk = TITANIC_SCHEMA
        elif dataset.lower() == "wine":
            schema_chunk = WINE_SCHEMA

    # Always add schema as the first chunk if present
    if schema_chunk:
        chunks = [schema_chunk] + row_chunks
    else:
        chunks = row_chunks

    return chunks

def ingest_pdf(path):
    """
    Ingest PDF for any dataset, extracts text page by page.
    """
    with pdfplumber.open(path) as pdf:
        texts = [page.extract_text() for page in pdf.pages if page.extract_text()]
    return texts