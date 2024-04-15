from elasticsearch import Elasticsearch
import config as c
import requests
import openai
from openai import OpenAI
import json
import pandas as pd
import re

def connect_es(ES_ID,ES_PASS):
    client=Elasticsearch("https://localhost:9200",
    ca_certs="C:/Users/SowmyaDevaraj/http_ca.crt",
    basic_auth=(c.ES_ID, c.ES_PASS)
)
    index_names=client.indices.get_alias().keys()
    return client.ping(),list(index_names)

def get_columns(index_name):
    ca_cert_path="C:/Users/SowmyaDevaraj/http_ca.crt"
    url = "https://localhost:9200/"+index_name+"/_mapping"
    response = requests.get(url,verify=ca_cert_path,auth=("elastic","au-70MrSRtdDD1M9U=-I"))
    mapping = response.json()
    col_names=list(mapping[index_name]['mappings']['properties'].keys())
    return col_names,mapping


def get_completion(apikey,role,prompt,model="gpt-3.5-turbo-1106", temperature = 0):
    openai_client = OpenAI(api_key=apikey)
    delimiter="###"
    messages =  [ {'role':'system', 'content': role},
                {'role':'user', 'content': f"{delimiter}{prompt}{delimiter}"},]
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

#Convert to json and fetch result
def convert_json(text,index_name):
    start_index = text.find('{')
    end_index = text.rfind('}')
    json_part = text[start_index:end_index+1]
    data = json.loads(json_part)
    client=Elasticsearch("https://localhost:9200",
    ca_certs="C:/Users/SowmyaDevaraj/http_ca.crt",
    basic_auth=(c.ES_ID, c.ES_PASS))
    res=client.search(index=index_name,body=data)
    return res

def sample_records(json_df):
    data_dict = json.loads(json_df)
    # Access the data using the dictionary
    data_list = data_dict['data']
    df = pd.json_normalize(data_list)
    return df

def extract_code(vis_f):
    # Use regular expression to extract code between backticks with language identifier 'python'
    code_match = re.search(r'```python(.*?)```', vis_f, re.DOTALL)

    if code_match:
        extracted_code = code_match.group(1).strip()
    return extracted_code