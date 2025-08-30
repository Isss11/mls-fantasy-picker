import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_player_statistics():
    """
    Obtain player statistics 
    """
    print("Creating driver...")
    driver = webdriver.Edge()
    print("Created driver.")

    url = "https://fbref.com/en/comps/22/stats/Major-League-Soccer-Stats"
    driver.get(url)

    print("Waiting...")
    player_stats_table = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "div_stats_standard"))
    )
    print("Done waiting.")

    text = "\n".join(player_stats_table.text.splitlines()[1:])
    column_names = text.splitlines()[0].split(" ")
    column_names.pop(5)
    column_names = column_names[:-11] # Eliminating the bith date and per 90 minutes data
    
    print(column_names)

    rows = text.splitlines()
    data_rows = rows[1:]
    row = data_rows[0]
    
    fp = open("rows.txt", "w")
    fp.write(str(rows))
    fp.close()
    
    # Using regex to split the rows up
    regexes = [r'\s', r'\s[a-z]*\s', r'\s', r'\s', r'\s\d\d-\d\d\d\s']
    
    for i in range(20):
        regexes.append(r'\s')
        
    data = {}
    
    for row in data_rows:
        update_data_with_row_vals(data, row, column_names, regexes)
        
    print(data)
    
    return pd.DataFrame(data)

def update_data_with_row_vals(data: dict, row: str, col_names: list[str], regexes: list[str]):
    print(row)
    if "Rk" == row[0:2] or not re.search(r'\s[a-z]*\s', row):
        return
    
    cp_row = row
    
    for col, regex in zip(col_names, regexes):
        row_split = re.split(regex, cp_row, maxsplit=1)
        print(cp_row)
        
        # Add values to the array list
        if data.get(col) == None:
            data[col] = [row_split[0]]
        else:
            data[col] += [row_split[0]]
        
        cp_row = row_split[1]

if __name__ == "__main__":
    df = get_player_statistics()
    
    print(df)
    df.to_csv("test.csv", index=False)