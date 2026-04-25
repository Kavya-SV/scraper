import requests
import time

def fetch_page(url):
    for attempt in range(3):
        try:
            response=requests.get(url)

            if response.status_code==200:
                return response.text
            elif response.status_code==404:
                print("Page not found:",url)
                return None
            elif response.status_code==403:
                print("Blocked!")
                return None
            else:
                print(f"Retring...Status {response.status_code}")
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print("Error: ",e)
            time.sleep(2)
    return None