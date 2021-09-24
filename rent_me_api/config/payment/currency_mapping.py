currency_dict = {
    "British Pound Sterling": "GBP",
    "Canadian Dollar": "CAD",
    "Cape Verdean Escudo": "CVE",
    "Chilean Peso": "CLP",
    "Colombian Peso": "COP",
    "Congolese France": "CDF",
    "Egyptian Pound": "EGP",
    "SEPA": "EUR",
    "Gambian Dalasi": "GMD",
    "Ghanaian Cedi": "GHS",
    "Guinean Franc": "GNF",
    "Kenyan Shilling": "KES",
    "Liberian Dollar": "LRD",
    "Malawian Kwacha": "MWK",
    "Moroccan Dirham": "MAD",
    "Mozambican Metical": "MZN",
    "Nigerian Naira": "NGN",
    "Peruvian Sol": "SOL",
    "Rwandan Franc": "RWF",
    "Sierra Leonean Leone": "SLL",
    "São Tomé and Príncipe dobra": "STD",
    "South African Rand": "ZAR",
    "Tanzanian Shilling": "TZS",
    "Ugandan Shilling": "UGX",
    "United States Dollar": "USD",
    "Central African CFA Franc BEAC": "XAF",
    "West African CFA Franc BCEAO": "XOF",
    "Zambian Kwacha (pre-2013)": "ZMK",
    "Zambian Kwacha": "ZMW",
    "Brazilian Real": "BRL",
    "Mexican Peso": "MXN",
    "Argentine Peso": "ARS"
}

def get_currency_list(a_dict):
    currency_list = []
    
    for key in a_dict:
        currency_list.append(key)
        
    return currency_list
    