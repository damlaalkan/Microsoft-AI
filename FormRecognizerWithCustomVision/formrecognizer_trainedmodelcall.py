########### Python Form Recognizer Async Analyze #############
import json
import time
import getopt
import sys
import os
from requests import get, post

def runAnalysis(input_file, output_file):
    # Endpoint URL
    endpoint = r"<endpoint url>"
    # Subscription Key
    apim_key = "<fr key>"
    # Model ID
    model_id = "<id>"
    post_url = endpoint + "/formrecognizer/v2.0/custom/models/%s/analyze" % model_id
    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': 'image/jpeg',
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    try:
        with open(input_file, "rb") as f:
            data_bytes = f.read()
    except IOError:
        print("Inputfile not accessible.")
        sys.exit(2)

    try:
        print('Initiating analysis...')
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        print("POST analyze succeeded:\n%s" % resp.headers)
        print
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    print()
    print('Getting analysis results...')
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = resp.json()
            if resp.status_code != 200:
                print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                if output_file:
                    with open(output_file, 'w') as outfile:
                        json.dump(resp_json, outfile, indent=2, sort_keys=True)
                print("Analysis succeeded:\n%s" % json.dumps(resp_json, indent=2, sort_keys=True))
                quit()
            if status == "failed":
                print("Analysis failed:\n%s" % json.dumps(resp_json))
                quit()
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2*wait_sec, max_wait_sec)     
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            print(msg)
            quit()
    print("Analyze operation did not complete within the allocated time.")

input_file = 'test1.jpeg'
output_file = 'fr.txt'

runAnalysis(input_file, output_file)
