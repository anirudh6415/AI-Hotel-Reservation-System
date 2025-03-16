import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.config = read_yaml(config_path)

        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)


    def preprocess_data(self,df):
        try:
            logger.info("Starting our Data Processing Step")

            logger.info("Dropping the columns")

            df.drop(columns=['Unnamed: 0','Booking_ID'], inplace =True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_colums"]

            logger.info("Applying Label Encoding")
            labelencoder = LabelEncoder()
            mapping = {}

            for col in cat_cols:
                df[col] = labelencoder.fit_transform(df[col])
                mapping[col] = {label: code for label,code in zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_))}

            logger.info("Label Mappings are:")    
            for label,code in mapping.items():
                logger.info(f"{label} : {code}")
                
            logger.info("Skewness Handling:")
            skewness_thrs =  self.config["data_processing"]["skewness_thresold"]

            skewness= df[num_cols].apply(lambda x:x.skew())
            
            for col in skewness[skewness>skewness_thrs].index:
                df[col] = np.log1p(df[col])

            return df

        except Exception as e:
            logger.error(f"Error during preprocess step{e}")
            raise CustomException(f"Error while preprocessing data",e)
    
    def balance_data(self,df):
        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data Balanced Successfully")

            return balanced_df

        except Exception as e:
            logger.error(f"Error during handling imbalanced data step {e}")
            raise CustomException(f"Error while balancing data",e)
        
    def select_features(self,df):
        try:
            logger.info("Starting our feature selection step")
            
            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importances_df = pd.DataFrame({
                                        'feature' : X.columns,
                                        'importance': feature_importance
                                    })
            num_features = self.config["data_processing"]["no_of_features"]

            top_feature_df = feature_importances_df.sort_values(by= "importance", ascending= False)

            top_10_features = top_feature_df['feature'].head(num_features).values
            logger.info(f"Top 10 Features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ['booking_status']]

            logger.info("Feature selection completed Successfully")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException(f"Error while selecting features",e)
        
    
    def save_data(self,df,file_path):
        try:
            logger.info("saving our data in processed folder")

            df.to_csv(file_path, index=False)

            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data step {e}")
            raise CustomException(f"Error while saving data",e)
        
    def process(self):
        try: 
            logger.info("Starting data processing step")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            
            train_df =self.balance_data(train_df)
            test_df =self.balance_data(test_df)
            
            train_df= self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(train_df,PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException :{str(ce)}")

        finally:
            logger.info("Data processing Completed")
        
if __name__ == "__main__":

    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()