import logging
import requests

logger = logging.getLogger()


class BinanceFuturesClient:
    def __int__(self, testnet):
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com/"

        self.prices = dict()

        logger.info("Binance Futures Client initilized")

    def make_request(self, method, endpoint, data):
        if method == "GET":
            res = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError()
        if res.status_code == 200:
            return res.json()
        else:
            logger.error("Error while using a %s request to %s (error code %s)", method, endpoint, res.json(),
                         res.status_code)
            return None

    def get_contracts(self):
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None)

        contracts = dict()
        for data_contract in exchange_info['symbols']:
            contracts[data_contract['pair']] = data_contract
        return contracts

    def get_historical_candels(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000

        res_candels = self.make_request("GET", "fapi/v1/klines", data)

        candels = []

        if res_candels is not None:
            for cStick in res_candels:
                candels.append([cStick[0], float(cStick[1]), float(cStick[2]), float(cStick[3]), float(cStick[4]),
                                float(cStick[5])])
        return candels

    def get_bit_ask(self, symbol):

        data = dict()
        data['symbol'] = symbol
        ob_data = self.make_request("GET", "/fapi/v1/ticker/bookTicker", data)

        if ob_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(ob_data['bidPrice']), 'ask': float(ob_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[symbol]['ask'] = float(ob_data['askPrice'])
        return self.prices[symbol]
# def get_contrats():
#   res_obj = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
#   print(res_obj.status_code, res_obj.json())
#
#   contracts = []
#
#   for contract in res_obj.json()['symbols']:
#       print(contract['pair'])
#       contracts.append(contract['pair'])
#   return contracts
#
# print(get_contrats())
