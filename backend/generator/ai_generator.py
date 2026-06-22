import pandas as pd 
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from faker import Faker
import random 

fake = Faker()

def generate_synthetic_data(csv_path,fields,  rows=100):
    print("AI GENERATOR RUNNING")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    ctgan_columns=[]
    faker_columns=[]
    for field in fields:
        if field.generation_method =="ctgan":
            ctgan_columns.append(field.field_name.lower())
        elif field.generation_method =="faker":
            faker_columns.append(field)
    
    df_ctgan = df[ctgan_columns]

    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df_ctgan)

    synthesizer =CTGANSynthesizer(metadata)
    synthesizer.fit(df_ctgan)

    synthetic_df = synthesizer.sample(num_rows = rows)
    print("faker columns")
    for field in faker_columns:
        print(field.field_name, field.field_type)  

    for field in faker_columns:
        if field.field_type == 'email':
            synthetic_df[field.field_name]= [fake.email() 
                                             for _ in range(rows)]
        elif field.field_type == "number":
            synthetic_df[field.field_name]= [random.randint(100000,999999)
                                            for _ in range(rows)]
        elif field.field_type == 'date':
            synthetic_df[field.field_name] = [fake.date()
                                              for _ in range(rows)]
        elif field.field_type == 'string':
            synthetic_df[field.field_name]= [fake.name()
                                             for _ in range(rows)]
        elif field.field_type == 'boolean':
            synthetic_df[field.field_name]= [random.choice([True,False])
                                             for _ in range(rows)]
    
    print("final synthetic columns")
    print(list(synthetic_df.columns))
    print('original columns')
    print(list(df.columns))

    print("faker columns")
    for field in faker_columns:
        print(field.field_name, field.field_type)    

    for col in df.columns:
        if col not in synthetic_df.columns:
            synthetic_df[col]= None        
    synthetic_df = synthetic_df[df.columns]
    return synthetic_df
                    