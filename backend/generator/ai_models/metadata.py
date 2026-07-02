import pandas as pd 
from sdv.metadata import SingleTableMetadata

def create_metadata(df):
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)
    return metadata