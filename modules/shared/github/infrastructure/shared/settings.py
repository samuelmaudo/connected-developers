import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
