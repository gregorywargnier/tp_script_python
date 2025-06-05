import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

import dotenv
import requests
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s Data: %(args)s',
    handlers=[
         logging.StreamHandler(),
        RotatingFileHandler("logs/app.log", maxBytes=10000, backupCount=10)

    ],
)

dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
timeout=5

now = datetime.datetime.now().strftime('%Y%m%d')

#Ne pas afficher le token
token = API_TOKEN
hide = token.replace(token, '***')

def fast_api():
    try:

        response = requests.get(f'{API_URL}',
                                headers=headers,
                                timeout=timeout)

        #Json save

        result = response.json()

        data = f'{now}-result.json'

        file = "reports"

        os.makedirs(file, exist_ok=True)

        route = os.path.join(file, data)

        # Sauvegarde des données en format JSON
        with open(route, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)

        print(f"Results saved in folder {route}")

        logging.info(f'HTTP response from {API_URL},{hide} with status code {response.status_code}')
        response.raise_for_status()
        if 500 < response.status_code <= 599:
            raise Exception(f'Error {response.status_code} in API {response.reason}')

        if 400 < response.status_code <= 499:
            raise Exception(f'Error {response.status_code} in API {response.reason}')

        return response
    except requests.exceptions.HTTPError as e:
        logging.error(f'HTTP error: {hide}')
        return e
    except requests.exceptions.RequestException as e:
        logging.error(f'Network error on {API_URL}, {hide}')
        return e
    except Exception as e:
        logging.error(e.args[0])
        return 'Error in API'

print(fast_api())
