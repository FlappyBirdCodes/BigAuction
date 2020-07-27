import pandas as pd
import random

urlFile = pd.read_csv(r"C:\Users\oscar\Documents\BigAuction\urlsCsv\test.csv")
urls = urlFile["url"]
urls = [url for url in urls if url != "None"]

