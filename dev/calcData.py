import pandas as pd
import requests
from io import StringIO
import numpy as np

orig_url='https://drive.google.com/file/d/1FW9JcMoovgV3pEq4TJiqQ4DqSWC0JbfE/view'

file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id

class calcData:
    def __init__(self):
        pass
    def GloBal_Total(self):
        url = requests.get(dwn_url).text
        csv_raw = StringIO(url)
        dfs = pd.read_csv(csv_raw)
        max_date = max(dfs["Date"])
        total_cases = np.sum(dfs[dfs["Date"]==max_date]["Confirmed"])
        new_cases = np.sum(dfs[dfs["Date"]==max_date]["newConfirmed"])
        total_deaths = np.sum(dfs[dfs["Date"]==max_date]["Death"])
        new_deaths = np.sum(dfs[dfs["Date"]==max_date]["newDeath"])
        total_recovered = np.sum(dfs[dfs["Date"]==max_date]["Recovered"])
        new_recovered = np.sum(dfs[dfs["Date"]==max_date]["newRecovered"])
        total_active = (total_cases-total_deaths) - total_recovered
        return [total_cases, new_cases, total_deaths, new_deaths, total_recovered,new_recovered, total_active]

    def country_data(self, country_name):
        url = requests.get(dwn_url).text
        csv_raw = StringIO(url)
        dfs = pd.read_csv(csv_raw)
        dfs["Country"] =  dfs["Country"].apply(lambda x: x.lower()) 
        country_q = country_name.lower()
        max_date = max(dfs[dfs["Country"]==country_q]["Date"])
        cond1 = dfs["Country"]==country_q 
        cond2 = dfs["Date"]==max_date
        total_cases = np.sum(dfs[cond1 & cond2]["Confirmed"])
        new_cases = np.sum(dfs[cond1 & cond2]["newConfirmed"])
        total_deaths = np.sum(dfs[cond1 & cond2]["Death"])
        new_deaths = np.sum(dfs[cond1 & cond2]["newDeath"])
        total_recovered = np.sum(dfs[cond1 & cond2]["Recovered"])
        new_recovered = np.sum(dfs[cond1 & cond2]["newRecovered"])
        total_active = (total_cases-total_deaths) - total_recovered
        return [total_cases, new_cases, total_deaths, new_deaths, total_recovered, new_recovered, total_active, country_q]
    
    def country_list(self):
        url = requests.get(dwn_url).text
        csv_raw = StringIO(url)
        dfs = pd.read_csv(csv_raw)
        list_cntry = dfs["Country"].unique()
        text_cntry = ["Countries: \n"]
        for index, item in enumerate(list_cntry):
            text_cntry.append(str(index + 1)+ ": "+ item +"\n")
        message_cntry = " ".join(text_cntry)
        return message_cntry
        
        
