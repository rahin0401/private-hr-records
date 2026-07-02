import logging 
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder
logger = logging.getLogger(__name__)


def load_dataset(dataset_path: str)->pd.DataFrame:
    path =Path(dataset_path)
    if not path.exists():
        logger.error("dataset not found %s", dataset_path)
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    try: 
        df = pd.read_csv(path)

        if df.empty: 
            logger.error("Dataset is empty")
            raise ValueError("dataset is empty")
        
        logger.info("dataset loaded succesfully. rows %s columns: %s", len(df), len(df.columns),)
        return df 
    except Exception as e: 
        logger.exception("failed to load dataset.")
        raise RuntimeError(f"Unable to load dataset:{e}")