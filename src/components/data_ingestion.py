import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')
    raw_data_path: str=os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Read the data in stud.csv as dataframe
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            dir_path = os.path.dirname(self.ingestion_config.train_data_path)
            print(f"Creating directory: {dir_path}") 
            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Splitting data into train and test
            logging.info('Train test split initiated')
            train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Ingestion of the data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__=="__main__":
    # Creating an instance of a DataIngestion and initiate data ingestion
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_array, test_array, _ =data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    output_r2_score = model_trainer.initiate_model_trainer(train_array=train_array, test_array=test_array)
    print(output_r2_score)

