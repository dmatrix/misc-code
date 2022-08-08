import random
from numpy import NaN
import pandas as pd

NUM_ROWS = 8001
STATES = ["CA", "AZ", "OR", "WA", "TX", "UT", "NV", "NM", None]
M_STATUS = ["married", "single", "domestic", "divorced", "undeclared"]
GENDER = ["F", "M", "U"]
HOME_OWNER = ["condo", "house", "rental", "cottage"]

def get_anonomized_name(num_letters=6):
    import string

    return ("anonomized-" + "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=num_letters)))

def get_anonomized_ssn():
    return ("anonomized-" + "".join(["{}".format(random.randint(0, 9)) for num in range(1, 10)]))

def generate_data(rows=101):
    items = items = [{"id": i,
          "ssn": None,
          "name": None,
          "amount": i * 1.5 * 1000, 
          "interest": random.randint(1,3) * 1.0,
          "state": random.choice(STATES),
          "marital_status": random.choice(M_STATUS),
          "property": random.choice(HOME_OWNER),
          "dependents": random.randint(1,5) if i % 2 == 0 else NaN,
          "defaulted": random.randint(0,1),
          "gender": random.choice(GENDER) } for i in range(1,rows)]
    return items

def gen_pandas_data(rows=101):
    items = generate_data(rows)
    return pd.DataFrame.from_dict(items)
