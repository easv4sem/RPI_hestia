import requests
import json
#from services.hestia_logger import setup_logger

#logger = setup_logger(name)


def api_GET(get_url):

	headers = {
		"Content-Type": "application/json"
	}

	try:
		response = requests.get(get_url, headers=headers, timeout=5)

		if response.status_code == 200:

			#logger.info(f"Data received: {data}")
			#print(f"Data received: {response.json()}")
			pass

		else:
			#logger.error(f"api GET request failed with status code {response.status_code}: {response.text}")
			#print(f"api GET request failed with status code {response.status_code}: {response.text}")
			pass

		return response.status_code



	except requests.exceptions.RequestException as e:
		#logger.error(f"api GET error: {e}")
		print(f"api GET error : {e}")

		return None




def api_POST(post_url, payload):

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(post_url, data=json.dumps(payload), headers=headers, timeout=5)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Data sent successfully (api post): {response.json()}")
            #logger.info(f"Data sent successfully (api POST): {response.json()}")

        else:
            #logger.error(f"api POST request failed with status code {response.status_code}: {response.text}")
            print(f"api POST request failed with status code {response.status_code}: {response.text}")

        return response.status_code


    except requests.exceptions.RequestException as e:
        #logger.error(f"api POST error : {e}")
        print(f"api POST error: {e}")

        return None
