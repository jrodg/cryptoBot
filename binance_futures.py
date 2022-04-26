import logging
import requests
import pprint
logger = logging.getLogger()


def get_contrats():
  res_obj = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
  print(res_obj.status_code, res_obj.json())

  contracts = []

  for contract in res_obj.json()['symbols']:
      print(contract['pair'])
      contracts.append(contract['pair'])
  return contracts

print(get_contrats())
