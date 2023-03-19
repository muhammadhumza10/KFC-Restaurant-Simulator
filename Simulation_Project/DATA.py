import math
from math import sqrt, pi

import numpy as np
import pandas as pd
import statistics

data = pd.read_csv("FinalKFCdata.csv")
InterArrival = data["InterArrival"]
Service = data["ServiceTime"]

IAlower = min(InterArrival)
IAupper = max(InterArrival)
STlower = min(Service)
STupper = max(Service)
lambda_ = 1/(sum(InterArrival)/len(InterArrival))
meu = 1/(sum(Service)/len(Service))
IASTD = statistics.stdev(InterArrival)
STSTD = statistics.stdev(Service)
IAmean = (sum(InterArrival)/len(InterArrival))
IAvar = IASTD**2
STmean = (sum(Service)/len(Service))
STvar = STSTD**2
IAalpha = (IAmean**2) / IAvar
IAbeta = IAmean/IAvar
STalpha = (STmean**2) / STvar
STbeta = STmean/STvar