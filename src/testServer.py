import requests


for i in range(50):
	headers = {"Content-Type": "application/json"}
	r = requests.put(url='http://127.0.0.1:8080', data=i, headers=headers)
	print "Body:   " + r.request.body
	print "Status: " + str(r.status_code)
	print "_--_"
	r2 = requests.get(url='http://127.0.0.1:8080')
	print "Data from GET: " + r2.text