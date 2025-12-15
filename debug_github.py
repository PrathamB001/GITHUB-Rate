import requests
import os

headers = {"Accept": "application/vnd.gh_utils+json"}

token = os.getenv("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

q = "(calorie OR exercise) language:python stars:>10 fork:false archived:false"

r = requests.get(
    "https://api.github.com/search/repositories",
    headers=headers,
    params={"q": q, "per_page": 5},
    timeout=10
)

print("STATUS:", r.status_code)
items = r.json().get("items", [])
print("COUNT:", len(items))

for it in items[:3]:
    print(it["full_name"], "->", it["html_url"])
