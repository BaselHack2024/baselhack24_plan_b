
import time, json, os

data_folder_path = './data'

def run_process_analysis(process_id: str):
    time.sleep(30)
    process_folder = f"{data_folder_path}/{process_id}" 
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True)
    data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "is_active": True,
    "hobbies": ["reading", "traveling", "coding"]
    }
    with open(f"{process_folder}/result.json", "w") as json_file:
        json.dump(data, json_file, indent=4)