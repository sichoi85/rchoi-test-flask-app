import requests

url = 'http://127.0.0.1:5000/upload-image'
my_img = {'image': open('/Users/sungilchoi/Projects/django-to-azure/azure-sql-db-python-rest-api/assets/receipt.jpg', 'rb')}
r = requests.post(url, files=my_img)

print(r.json())
