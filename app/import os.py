import os
import pandas as pd


df = pd.read_csv("/Users/ligiavergara/docker/app/titanic.csv")
html_table = df.head().to_html()
print(html_table)