import json
import logging

import dotenv
import requests
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s Data: %(args)s',
    handlers=[
         logging.StreamHandler(),
        logging.FileHandler('logs/app.log'),
    ],
)


dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
timeout=5

def fast_api():
    try:
        #Ne pas afficher le token
        token = API_TOKEN
        hide = token.replace(token, '***')

        response = requests.get(f'{API_URL}',
                                headers=headers,
                                timeout=timeout)

        # json save

        result = response.json()

        data = "result.json"

        dossier = "reports"

        os.makedirs(dossier, exist_ok=True)

        route = os.path.join(dossier, data)

        # Sauvegarde des données en format JSON
        with open(route, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Résultats sauvegardés dans le dossier {route}")

        logging.info(f'HTTP response from {API_URL},{hide} with status code {response.status_code}')
        response.raise_for_status()
        if 500 < response.status_code <= 599:
            raise Exception(f'Erreur {response.status_code} sur l\'API {response.reason}')

        if 400 < response.status_code <= 499:
            raise Exception(f'Erreur {response.status_code} sur l\'API {response.reason}')

        return response
    except requests.exceptions.HTTPError as e:
        logging.error(f'HTTP error: {hide}')
    except Exception as e:
        logging.error(e.args[0])
        return 'Erreur sur l\'API'

print(fast_api())
