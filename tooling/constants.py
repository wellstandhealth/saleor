import os
from dotenv import load_dotenv
load_dotenv()

EXPORT_SALEOR_MODELS = tuple(os.getenv('EXPORT_SALEOR_MODELS').split(','))
