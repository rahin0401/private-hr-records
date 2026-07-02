import pandas as pd 
from sdv.single_table import CTGANSynthesizer
from .metadata import create_metadata


def train_ctgan(df):
    metadata = create_metadata(df)
    synthesizer = CTGANSynthesizer(metadata)
    synthesizer.fit(df)
    return synthesizer

def generate_ctgan_data(synthesizer,rows):
    synthetic_df = synthesizer.sample(num_rows = rows)
    return synthetic_df