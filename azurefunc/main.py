from api4jenkins import Jenkins
import requests

def trigger_job():
    print("triggering a job")
    job_name = "testpipeline"
    token = "piotrtoken"
    params = {'token': token, 'modelname': 'value2', 'modelversion': '2'}
    url = f"http://40.113.108.88:8080/job/{job_name}/buildWithParameters"
    r = requests.get(url, auth=('piotr', '1131adc10200992de137a49c5f95305c6e'), params=params)
    print(r.status_code)




if __name__ == "__main__":
    trigger_job()