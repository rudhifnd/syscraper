import requests
import json
import pandas as pd

url = "https://www.glassdoor.co.uk/api/employer/11891-rating.htm?dataType=trend&category=overallRating&locationStr=&jobTitleStr=&filterCurrentEmployee=false"

with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en",
    }
    response = se.get(url)

data = json.loads(response.text)

results = pd.DataFrame()
results["date"], results["rating"] = data["dates"], data["employerRatings"]
