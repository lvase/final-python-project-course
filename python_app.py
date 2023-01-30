import requests
from flask import json
from cleanco import basename

print("GET METHOD TESt")
id = input("Enter the id of the company that you want to get:")
url = "http://127.0.0.1:5000/get_comp?id=" + id
response = requests.get(url)
obj = json.loads(response.content)
comp_name = obj['name']
cleaned_name = basename(comp_name)
print(obj)
print("Uncleaned company name: " + comp_name)
print("Cleaned company name with basename from cleanco: " + cleaned_name)

print("POST METHOD TEST")
id = input("Enter the id of the company that you want to add:")
name = input("Enter the name of the company that you want to add:")
country_iso = input("Enter the country_iso of the company that you want to add:")
city = input("Enter the city of the company that you want to add:")
nace = input("Enter the nace of the company that you want to add:")
website = input("Enter the website of the company that you want to add:")

payload = {"id": id, "name":name, "country_iso":country_iso, "city":city, "nace":nace, "website":website}
url = "http://127.0.0.1:5000/add_comp"
response = requests.post(url,json=payload)
print(response.text)