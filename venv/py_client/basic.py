import requests

endpoint = "http://localhost:8000/api/documents/"

get_res = requests.get(endpoint ,json={"product_id":123} )
# print(get_res.text)

print(get_res.text)

