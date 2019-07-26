# Abstract
A REST API service to get top 3 repositories of an organisation in Github by starts. Implemented using `falcon` which is a Python web framework.
## Pre-requirements
- Running environment `Python >= 3.6.*, Ubuntu 18.04`
- Install python libraries, `sudo pip3 install -r requirements.txt`, (included in `run.sh` also).

## Start server
To install dependencies: `./run.sh install &`

To start: `sudo python3 service.py &`
OR `./run.sh start &`

To stop: `./run.sh stop &`

## API ```POST``` query sample
```python
# Please refer test.py for more
import requests as req
# As per config.ini
res = req.post('http://0.0.0.0:5000/repos', json={'org': 'microsoft'})
result = res.json()
print(result)
```

## Load test
Load test using `Apahe Bench(ab)`.


```bash
# Install Apache Bench
$ sudo apt install apache2-utils
# Start load-test
$ ab -p post_loc.txt -T application/json -c 4 -n 20 http://0.0.0.0:5000/repos

# post_loc.txt contains the json you want to post
# -p means to POST it
# -T sets the Content-Type
# -c is concurrent clients
# -n is the number of requests to run in the test
```
