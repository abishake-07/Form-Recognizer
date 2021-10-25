import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
import json
import time
from requests import get, post
import pandas as pd 
from IPython.display import display 

# endpoint = "https://poc-fws.cognitiveservices.azure.com/"
# key = "5505b2fd16fc4d5fb3616b0cae3dcb7e"

# #Authenticating the client
# form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
# form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))

# #Retrieving pdf from the blob container using SAS URL.
# formUrl = "https://flatworldpocstorage.blob.core.windows.net/1120s/1120-S_1.pdf?sv=2020-08-04&st=2021-10-07T08%3A03%3A04Z&se=2022-10-08T08%3A03%3A00Z&sr=b&sp=rwd&sig=hZI04XiUD26eX0xHkdEMuaKPf7ho5TtydTqqItfUhV4%3D"
# poller = form_recognizer_client.begin_recognize_content_from_url(formUrl)
# page = poller.result()


# table = page[0].tables[0] # page 1, table 1
# print(table)
# print("Table found on page {}:".format(table.page_number))
# for cell in table.cells:
#     print("Cell text: {}".format(cell.text))
#     print("Location: {}".format(cell.bounding_box))
#     print("Confidence score: {}\n".format(cell.confidence))

#print(page)



# Endpoint URL
endpoint = r"https://poc-fws.cognitiveservices.azure.com/"
apim_key = "5505b2fd16fc4d5fb3616b0cae3dcb7e"
post_url = endpoint + "/formrecognizer/v2.1/layout/analyze"
source = "D:\Python Analysis\PDF's\Credit report 1.pdf"

headers = {
    # Request headers
    # Change Content-Type as appropriate
    'Content-Type': 'application/pdf',
    'Ocp-Apim-Subscription-Key': apim_key,
}
with open(source, "rb") as f:
    data_bytes = f.read()

try:
    resp = post(url = post_url, data = data_bytes, headers = headers)
    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % resp.text)
        quit()
    print("POST analyze succeeded:\n%s" % resp.headers)
    get_url = resp.headers["operation-location"]
except Exception as e:
    print("POST analyze failed:\n%s" % str(e))
    quit()

n_tries = 10
n_try = 0
wait_sec = 6
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            print("GET Layout results failed:\n%s" % resp_json)
            quit()
        status = resp_json["status"]
        if status == "succeeded":
            print("Layout Analysis succeeded:\n%s" % resp_json)
            quit()
        if status == "failed":
            print("Layout Analysis failed:\n%s" % resp_json)
            quit()
        # Analysis still running. Wait and retry.
        time.sleep(wait_sec)
        n_try += 1
    except Exception as e:
        msg = "GET analyze results failed:\n%s" % str(e)
        print(msg)

pd.options.display.max_columns = None 

for read_result in resp_json['analyzeResult']['pageResults']:
    print('Page Number:%s' %read_result['page'])
    print('----------------------Page %d: Extracted OCR--------------------'%read_result['page'])
    for line in read_result['lines']:
        print(line['text'])

    
for pageresult in resp_json['analyzeResult']['pageResults']:
    for table in pageresult['tables']:
        print('------------ Page %d: Extracted table--------------'% pageresult['page'])
        print('Number of rows:%d' %table['rows'])
        print('Number of columns:%d' %table['columns'])
        tableList = [[None for x in range(table['columns'])] for y in range(table['rows'])]
        for cell in table['cells']:
            tableList[cell['rowIndex']][cell['columnIndex']] = cell['text']
       
        df = pd.DataFrame.from_records(tableList)
        display(df)
                
