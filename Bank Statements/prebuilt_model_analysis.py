from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas as pd 
from IPython.display import display


'''
This basically follows the azure-formrecognizer version:3.1, Hence we see difference in classes. (Not a lot of variance)
'''
endpoint = "https://poc-fws.cognitiveservices.azure.com/"
key = "5505b2fd16fc4d5fb3616b0cae3dcb7e"

formUrl = "https://flatworldpocstorage.blob.core.windows.net/bstrain/110020436544_2.pdf?sp=rcwd&st=2021-10-20T07:39:55Z&se=2022-10-20T15:39:55Z&spr=https&sv=2020-08-04&sr=b&sig=I%2F7oL32LkJRnhmRyfTqpoV9WXOPiYLzdOj1sOkBvr7k%3D"

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", formUrl)
result = poller.result()


for table in result.tables:
    print('Number of rows:%d' %table.row_count)
    print('Number of columns:%d' %table.column_count)
    tableList =[[None for x in range(table.column_count)] for y in range (table.row_count)]
    for cell in table.cells:
        tableList[cell.row_index][cell.column_index] = cell.content

    df = pd.DataFrame.from_records(tableList)
    display(df)






# print("----Key-value pairs found in document----")
# for kv_pair in result.key_value_pairs:
#     if kv_pair.key and kv_pair.value:
#         print("Key '{}': Value: '{}'".format(kv_pair.key.content, kv_pair.value.content))
#     else:
#         print("Key '{}': Value:".format(kv_pair.key.content))
            
# print("\n----Entities found in document----")
# for entity in result.entities:
#     print("Category '{}': Sub-category: '{}': Content: '{}'".format(entity.category, entity.sub_category,entity.content))

print("----------------------------------------")

