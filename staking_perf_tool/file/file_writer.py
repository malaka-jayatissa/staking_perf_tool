import state
import os
import pandas as pd
from dataclasses import  asdict
from datetime import datetime

def generate_results(parent_folder:str, sub_folder:str, state: state.State, vaidator_count: int):
    combined_path = os.path.join(parent_folder,'results' ,sub_folder)
    if not os.path.exists(combined_path):
        os.makedirs(combined_path)
    df = pd.DataFrame([asdict(obj) for obj in state.results])
    df['vaidator_count'] = vaidator_count
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = os.path.join(combined_path, f'result_{timestamp}') 
    os.makedirs(folder_name)
    file_name = os.path.join(folder_name, 'raw_data.csv') 
    df.to_csv(file_name,index=False)


