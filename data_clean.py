import numpy as np
import pandas as pd

def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/combined_dfall.csv?token=GHSAT0AAAAAACOCXHGSI6BPZBCW5EFDC2OIZPIB4IA.csv")
    
    return df