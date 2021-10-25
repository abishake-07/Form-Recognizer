import json 
import time
from typing import Text 
import re
with open('1004d _1.pdf.json','r') as f:
    data = json.load(f)
    
   
   
#print(type(data))
#for result in data['readResults'][]

print(data['analyzeResult']['readResults'][0]['lines'][32]['text'])
print(len(data['analyzeResult']['readResults'][0]['lines'][32]['text']))
# Length of the number of lines in each page.
print(len(data['analyzeResult']['readResults'][0]['lines']))


pattern_company= re.compile(r'Company\s(Name||Name\s\w*)')
pattern_name = re.compile(r'Name||(Name\s)\w*')
pattern_signature = re.compile(r'Signature||signature')
i=0
companyName=[]
personName=[]
signatureName=[]

while i < len(data['analyzeResult']['readResults']):
    start = time.time()
    for j in range(0,len(data['analyzeResult']['readResults'][i]['lines'])):
        #print(len(data['analyzeResult']['readResults'][i]['lines']))
        #print(data['analyzeResult']['readResults'][i]['lines'][j]['text'])
        text = data['analyzeResult']['readResults'][i]['lines'][j]['text']
        #RegEx functions used here.
        matches_company = pattern_company.finditer(data['analyzeResult']['readResults'][i]['lines'][j]['text'])
        matches_name = pattern_name.finditer(data['analyzeResult']['readResults'][i]['lines'][j]['text'])
        matches_signature = pattern_signature.finditer(data['analyzeResult']['readResults'][i]['lines'][j]['text'])
        for match in matches_company:
            if text == match[0]:
                #print(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])
                print('Data has been added to the list!!')
                companyName.append(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])

        for match in matches_name: 
            if text == match[0]:
                #print(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])
                print('Data has been added to the list!!')
                personName.append(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])

        for match in matches_signature: 
            if text == match[0]:
                #print(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])
                print('Data has been added to the list!!')
                signatureName.append(data['analyzeResult']['readResults'][i]['lines'][j+1]['text'])
            
        else:
            print("Searching.........")
    i+=1
end = time.time()
#print(start-end)
print(companyName)
print(personName)
print(signatureName)


        
















            
