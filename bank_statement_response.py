import http.client
import json
from requests import post,get
import time

#change region
model_id = "chase_wellsfargo_model"
apim_key = r"5505b2fd16fc4d5fb3616b0cae3dcb7e"
endpoint = "https://poc-fws.cognitiveservices.azure.com/"
source_base_path = 'D:/Sample PDFs/Bank Statements/'
filename = 'FR_studio_179921064133_2.pdf'
source =  source_base_path+ filename+'.json'
post_url = endpoint + "/formrecognizer/documentModels/chase_wellsfargo_model:analyze?api-version=2021-09-30-preview&stringIndexType=textElements"
payload = json.dumps({
  "urlSource": "https://flatworldpocstorage.blob.core.windows.net/bs-wells-fargo/WF_110020436544_1.pdf?sp=r&st=2021-11-15T11:01:10Z&se=2022-11-15T19:01:10Z&spr=https&sv=2020-08-04&sr=b&sig=Jj%2FSUI%2BwbhU48jHIOGQ053keRIgDb0zaOOhzhAmtxUc%3D"
})
headers = {
  'Ocp-Apim-Subscription-Key': apim_key,
  'Content-Type': 'application/json'
}
#conn.request("POST", "/formrecognizer/documentModels/chase_wellsfargo_model:analyze?api-version=2021-09-30-preview&stringIndexType=textElements", payload, headers)
# res = conn.getresponse()
# print(res.headers)
# print(res.headers["Operation-Location"])
# print(res.status)

with open(source, "rb") as f:
    data_bytes = f.read()

try:
    resp = post(url = post_url, data = payload, headers = headers)
    if resp.status_code != 202:
        print("POST analyze failed:\n%s" % resp.text)
        quit()
    print("POST analyze succeeded:\n%s" % resp.headers)
    get_url = resp.headers["operation-location"]
except Exception as e:
    print("POST analyze failed:\n%s" % str(e))
    quit()


# GET the analyzed results and store it in a JSON format.
n_tries = 10
n_try = 0
wait_sec = 6
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        #Make another line to convert the JSON into a JSON file 
        out_file = open("myfile.json", "w") 
        resp_json = json.loads(resp.text)
        json.dump(resp_json, out_file, indent = 6) 
        out_file.close() 
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