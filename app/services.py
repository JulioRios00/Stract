import os
from dotenv import load_dotenv
import requests
import logging

logger = logging.getLogger(__name__)

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("AUTH_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def get_platform():
    url = f"{BASE_URL}/platforms"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_accounts(platform):
    url = f"{BASE_URL}/accounts?platform={platform}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_fields(platform):
    url = f"{BASE_URL}/fields?platform={platform}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_insights(platform, account):
    fields = (
        "ad_name,clicks,spend,impressions"
        if platform == "meta_ads"
        else "ad_name,clicks,cost,impressions"
    )

    url = (
        f"{BASE_URL}/insights"
        f"?platform={platform}"
        f"&account={account['id']}"
        f"&token={account['token']}"
        f"&fields={fields}"
    )

    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)

    return response.json()
