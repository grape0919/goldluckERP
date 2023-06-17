import json
import os

DEFAULT_CONF_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.json")
with open(DEFAULT_CONF_PATH, 'r') as config_file:
    sft_configuration = json.load(config_file)
    database_credential = sft_configuration['database_credential']