#pip install azure-ai-formrecognizer

import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

#Test Form Source
formUrl = "your_test_image(form)_url"

# Endpoint URL
endpoint = r"your_endpoint"
# Subscription Key
key = "your_key" 
# Model ID
model_id = "your_modelid"

form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))

poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
    model_id=model_id, form_url=formUrl)
result = poller.result()

for recognized_form in result:
    print("Form type: {}".format(recognized_form.form_type))
    for name, field in recognized_form.fields.items():
        print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
            name,
            field.label_data.text if field.label_data else name,
            field.value,
            field.confidence
        ))
