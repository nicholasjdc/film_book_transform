import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(".env")
API_URL = os.environ.get("API_URL")
with open('data_test.json') as user_file:
  file_contents = user_file.read()
  
parsed_json = json.loads(file_contents)
#print(parsed_json)
postHeaders = {"Content-Type": "application/json"}
for entry in parsed_json['entries']:
    p = requests.post(API_URL, data=json.dumps(entry), headers=postHeaders)
print("finished")
