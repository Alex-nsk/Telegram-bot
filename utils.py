import requests
import json
from config import keys



class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(base: str, sym: str, amount:str):
        if base == sym:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            sym_ticker = keys[sym]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {sym}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')



        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={sym_ticker}')
        total_sym = json.loads(r.content)[keys[sym]]

        return total_sym


