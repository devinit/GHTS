from .models import Currency
import re

def safeInt(x):
    try:
        return int(x)
    except:
        return -1
    
def safeFloat(x):
    x = re.sub("[^0-9.]","", x)
    try:
        return float(x)
    except:
        return -1.00