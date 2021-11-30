import json
import logging
import requests
import azure.functions as func


def main(event: func.EventGridEvent):
    data = event.get_json()
    result = json.dumps({
        'id': event.id,
        #'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })
    logging.info('Python EventGrid trigger processed an event: %s', result)

    print("triggering a job")
    job_name = "testpipeline"
    token = "piotrtoken"

    model_name = data['modelName']
    model_version = data['modelVersion']

    params = {'token': token, 'modelname': model_name, 'modelversion': model_version}
    print(params)
    url = f"http://40.113.108.88:8080/job/{job_name}/buildWithParameters"
    r = requests.get(url, auth=('piotr', '1131adc10200992de137a49c5f95305c6e'), params=params)
    print(r.status_code)

