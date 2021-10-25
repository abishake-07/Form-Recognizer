import json 
import time
from typing import Text 
import re
import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import json
import time
from requests import get, post
import sys



endpoint = "https://poc-fws.cognitiveservices.azure.com/"
key = "5505b2fd16fc4d5fb3616b0cae3dcb7e"

source_path = 'D:/Sample PDFs/Bank Statements/'
filename = 'Layout-Result-110021044426_3.pdf'

with open(source_path+filename+'.json','r') as f:
    data =json.load(f)


#print(data['analyzeResult']['readResults'][0]['lines'][32]['text'])
i=0
accountNames=[]
accountNumbers=[]
address =[]
acc_num=''
acc_num_split_list=[]
acc_num_split_json_list=[]
df_list_acc_1 =[]
df_list_acc_2=[]
while i < len(data['analyzeResult']['readResults']):
    start = time.time()
    for j in range(0,len(data['analyzeResult']['readResults'][i]['lines'])):
        text = data['analyzeResult']['readResults'][i]['lines'][j]['text']

        # Get the account names and  account number for joint accounts.
        #Wells Fargo
        if 'Account number' in text:
            accountNumbers.append(data['analyzeResult']['readResults'][i]['lines'][j]['text'])
        
        #First account name
        if 'Questions?' in text:
            accountNames.append(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])

        # Second account name if present.(Joint account)
        if 'Deposits/Additions' in text:
            second_name = data['analyzeResult']['readResults'][i]['lines'][j+2]['text']
            # accountNames.append(second_name)
            if len(second_name.split())>5:
                pass
            else:
                accountNames.append(second_name)
        #Address of the primary acount holder.
        if 'Available by phone 24 hours a day, 7 days a week:' in text:
            address.append(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])
            address.append(data['analyzeResult']['readResults'][i]['lines'][j+2]['text'])
        
        #CHASE
        #Chase account number:
        if 'Account Number' in text:
            accountNumbers.append( data['analyzeResult']['readResults'][i]['lines'][j]['text']) 

        # Get the account names:
        if 'Hard of Hearing' in text:
            accountNames.append( data['analyzeResult']['readResults'][i]['lines'][j+2]['text'])
        #Second account name if present
        if 'Para Espanol' in text:
            second_name = second_name = data['analyzeResult']['readResults'][i]['lines'][j+2]['text']
            if len(second_name.split())>5:
                pass
            else:
                accountNames.append( data['analyzeResult']['readResults'][i]['lines'][j+2]['text'])
            
        # Address of the primary holder.
        if 'International Calls:' in text:
            address.append(data['analyzeResult']['readResults'][i]['lines'][j+2]['text'])
            address.append(data['analyzeResult']['readResults'][i]['lines'][j+3]['text'])

    #Seperating DataFrames according to their page number and account number. (Chase)
        for pageresult in data['analyzeResult']['pageResults']:
            for acc in accountNumbers:
                if 'Primary Account:' in text:
                        acc_num = data['analyzeResult']['readResults'][i]['lines'][j]['text'][16:]
                        primary_account = acc[-16:]
                        #print(len(acc_num),len(primary_account),sep=',')

                        if primary_account == acc_num:
                            for  table in pageresult['tables']:
                                tableList = [[None for x in range(table['columns'])] for y in range(table['rows'])]
                                for cell in table['cells']:
                                    tableList[cell['rowIndex']][cell['columnIndex']] = cell['text']
                                    
                                df = pd.DataFrame.from_records(tableList)
                                df_list_acc_1.append(df)
                            
                        # Tables not related to the primary account number.
                        else:
                           for  table in pageresult['tables']:
                                tableList = [[None for x in range(table['columns'])] for y in range(table['rows'])]
                                for cell in table['cells']:
                                    tableList[cell['rowIndex']][cell['columnIndex']] = cell['text']
                                    
                                df = pd.DataFrame.from_records(tableList)
                                df_list_acc_2.append(df)
                
                    
                       


                           
                   
        
    i+=1


 
print(accountNumbers)
print(accountNames)

if len(accountNames)>1:
    print('It is a joint account')
else:
    print('It is a primary account')

print(address)
print(len(accountNumbers))
print(len(df_list_acc_1),len(df_list_acc_2))
print(df_list_acc_1)
print('-'*100)
print(df_list_acc_2)

