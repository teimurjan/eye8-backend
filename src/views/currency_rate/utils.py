import requests
import math
from xml.etree import ElementTree as ET


def get_float_from_node(key, node):
    return float(node.find(key).text.replace(",", "."))


DELTA = 1.5
ROUND_RATES = False


def get_rounded_rate(rate):
    _, integer = math.modf(rate)
    for delta in [0, -1, 1]:
        if (integer + delta) % 3 == 0:
            return integer + delta


def get_currency_rates(date=None):
    rates = {}

    date_query = "fdate=" + date if date else ""
    response = requests.get(f"https://nationalbank.kz/rss/get_rates.cfm?{date_query}")
    if response.status_code == 200:
        currencies = ET.fromstring(response.text).iter("item")
        for currency in currencies:
            if currency.find("title").text == "KGS":
                value = get_float_from_node("description", currency)
                nominal = get_float_from_node("quant", currency)
                rates["kzt_to_kgs"] = value / nominal
            elif currency.find("title").text == "USD":
                value = get_float_from_node("description", currency)
                nominal = get_float_from_node("quant", currency)
                rates["kzt_to_usd"] = value / nominal

        if rates.get("kzt_to_kgs") and rates.get("kzt_to_usd"):
            rates["kgs_to_usd"] = rates["kzt_to_usd"] / rates["kzt_to_kgs"] + DELTA
            if ROUND_RATES:
                rates["kgs_to_usd"] = get_rounded_rate(rates["kgs_to_usd"])

        return rates if len(rates) > 0 else None

    return None
