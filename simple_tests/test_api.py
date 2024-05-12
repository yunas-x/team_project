import os
import requests

api_url = os.getenv("API_URL")
api_token = os.getenv("API_TOKEN")

def test_programs():

    r = requests.get(  
                        f"{api_url}/programs",
                        headers={"Authorization": f"Bearer {api_token}"}
                    )
    
    assert r.status_code == 200

def test_fields():

    r = requests.get(  
                        f"{api_url}/fields",
                        headers={"Authorization": f"Bearer {api_token}"}
                    )
    
    assert r.status_code == 200
    
def test_universities():

    r = requests.get(  
                        f"{api_url}/universities",
                        headers={"Authorization": f"Bearer {api_token}"}
                    )
    
    assert r.status_code == 200
    
def test_infographics():

    r = requests.get(  
                        f"{api_url}/infographics?first_program_id=1&second_program_id=2",
                        headers={"Authorization": f"Bearer {api_token}"}
                    )
    
    assert r.status_code == 200
