import logging
import pandas as pd
from abc import ABC, abstractmethod
from selenium import webdriver

class Scraper(ABC):
    def __init__(self):
        self.driver =  webdriver.Edge()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
    @abstractmethod
    def fetch_content(self) -> None:
        pass
    
    @abstractmethod
    def parse_content(self, content: str) -> pd.DataFrame:
        pass
    
    def save_data(self, data: pd.DataFrame, file_name: str) -> None:
        logging.getLogger(__name__).info(f"Saving data to {file_name}...")
        data.to_csv(file_name, index=False)
        logging.getLogger(__name__).info(f"Data saved to {file_name}.")