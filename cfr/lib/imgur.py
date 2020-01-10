import requests
import configparser
from os import path
from pathlib import Path

config_file = str(Path(path.dirname(path.abspath(__file__))).parent) + '/imgur.ini'

config = configparser.ConfigParser()
config.read(config_file)

client_id = config['IMGUR']['client_id']
client_secret = config['IMGUR']['client_secret']

def upload_image(data):
  headers = {'Authorization' : 'Client-ID {}'.format(client_id)}
  form = {'image' : data}

  return requests.post('https://api.imgur.com/3/upload', data=form, headers=headers)
