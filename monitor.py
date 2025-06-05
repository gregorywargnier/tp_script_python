import logging

import dotenv
import requests
import os


logging.basicConfig(
    level=logging.INFO, # Jusque quel level on affiche les logs
    format='%(asctime)s [%(levelname)s] %(message)s Data: %(args)s', # Format des logs
    handlers=[ # Quelles sont les destinations des logs
        # logging.StreamHandler(), # Affichage dans la console
        logging.FileHandler('log.log'), # Affichage dans un fichier
    ],
)


dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
timeout=0.5

def fast_api():
    try:

        response = requests.get(f'{API_URL}',
                                headers=headers,
                                timeout=timeout)

        response.raise_for_status()
        if 500 < response.status_code <= 599:
            raise Exception(f'Erreur {response.status_code} sur l\'API {response.reason}')

        if 400 < response.status_code <= 499:
            raise Exception(f'Erreur {response.status_code} sur l\'API {response.reason}')

        return response
    except Exception as e:
        logging.error(e.args[0])
        return 'Erreur sur l\'API'

print(fast_api())
