from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl="id-ID", tz=360)
pytrends.build_payload(
    kw_list=["kucing"],
    timeframe="today 12-m",
    geo="ID"
)

df = pytrends.interest_over_time().reset_index()
df.to_csv("trend_kucing.csv", index=False)

print("Selesai, file trend_kucing.csv dibuat")
