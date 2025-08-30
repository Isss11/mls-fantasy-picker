import logging
import re
import pandas as pd
from Scraper import Scraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PlayerScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url = "https://fbref.com/en/comps/22/stats/Major-League-Soccer-Stats"
    
    def fetch_content(self):
        self.logger.info(f"Fetching content from {self.url}...")
        
        self.driver.get(self.url)
        content =  WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "div_stats_standard"))
        )
        
        self.logger.info("Content fetched successfully.")
        
        return "\n".join(content.text.splitlines()[1:])
        
    def parse_content(self, content) -> pd.DataFrame:
        column_names = content.splitlines()[0].split(" ")
        column_names.pop(5)
        column_names = column_names[:-11] # Eliminating the bith date and per 90 minutes data

        rows = content.splitlines()
        data_rows = rows[1:]
        row = data_rows[0]
        
        # Using regex to split the rows up
        regexes = [r'\s', r'\s[a-z]*\s', r'\s', r'\s', r'\s\d\d-\d\d\d\s']
        
        for i in range(20):
            regexes.append(r'\s')
            
        data = {}
        
        for row in data_rows:
            self.update_data_with_row_vals(data, row, column_names, regexes)  
            
        return pd.DataFrame(data)
            
    def update_data_with_row_vals(self, data: dict, row: str, col_names: list[str], regexes: list[str]):
        if "Rk" == row[0:2] or not re.search(r'\s[a-z]*\s', row):
            return
        
        cp_row = row
        
        for col, regex in zip(col_names, regexes):
            row_split = re.split(regex, cp_row, maxsplit=1)
            
            # Add values to the array list
            if data.get(col) == None:
                data[col] = [row_split[0]]
            else:
                data[col] += [row_split[0]]
            
            cp_row = row_split[1]
    
if __name__ == "__main__":
    scraper = PlayerScraper()
    content = scraper.fetch_content()
    df = scraper.parse_content(content)
    scraper.save_data(df, "fbref_player_stats.csv")