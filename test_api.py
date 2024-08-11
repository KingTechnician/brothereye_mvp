from dotenv import load_dotenv
import os 
import requests
load_dotenv()


api_key = os.getenv("BROTHEREYE_API_KEY")

brothereye_url =  "https://brothereye-cloud.onrender.com"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_current_job(job_id,job_type):
    base_url = f"{brothereye_url}/api_job_status"

    data = {
        "job_id": job_id,
        "job_type": job_type
    }

    print(data)

    response = requests.get(base_url, headers=headers, json=data)

    return response.json()


job_id = 4880078191433693
job_type="people"

print(get_current_job(job_id,job_type))
