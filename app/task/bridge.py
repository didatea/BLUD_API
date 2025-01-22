import json
import os

import requests

from app.utils import logger

baseUrlScheme = os.environ.get('BASE_URL_SCHEME')
baseUrl = os.environ.get('BASE_URL')
baseUrlPort = os.environ.get('BASE_URL_PORT')


def getBaseUrl():
    url = f"{baseUrlScheme}://{baseUrl}"
    if baseUrlPort != '':
        url = f"{baseUrlScheme}://{baseUrl}:{baseUrlPort}"
    return url


def internalApi_byUrl(data, baseUrlDef=None):
    logger.info('----------------------------------------------------------------TASK BEGIN')
    logger.info('TASK : internalApi_byUrl START')
    currentServerUrl = 'https://aset.api.insaba.co.id'
    if baseUrlDef:
        currentServerUrl = baseUrlDef
    if 'url' in data:
        url = f"https://aset.api.insaba.co.id/internal/{data['url']}"
        r = requests.post(url, data=json.dumps(data['payload'] if 'payload' in data else {}),
                          headers=data['headers'] if 'headers' in data else {})
        logger.info('TASK : internalApi_byUrl RESULT -> ' + str(r.status_code) + ' ' + r.reason + ' ' + r.text)
    else:
        logger.info('TASK : internalApi_byUrl FAILED : url not in payload!')
    logger.info('TASK : internalApi_byUrl FINISH')
    logger.info('----------------------------------------------------------------TASK END')


def api_byUrl(data):
    logger.info('----------------------------------------------------------------TASK BEGIN')
    logger.info('TASK : api_byUrl START')
    if 'url' in data:
        url = f"https://aset.api.insaba.co.id/api/{data['url']}"
        r = requests.post(url, data=json.dumps(data['payload']), headers=data['headers'])
        logger.info('TASK : api_byUrl RESULT -> ' + str(r.status_code) + ' ' + r.reason + r.text)
    else:
        logger.info('TASK : api_byUrl FAILED : url not in payload!')
    logger.info('TASK : api_byUrl FINISH')
    logger.info('----------------------------------------------------------------TASK END')