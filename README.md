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
res = req.post('http://<IP>:5000/repos', json={'org': 'microsoft'})
result = res.json()
print(result)
```

## Load test
Load test using `Apahe Bench(ab)`.


```python
# Install Apache Bench
$ sudo apt install apache2-utils
# Start load-test
$ ab -p post_loc.txt -T application/json -c 4 -n 20 http://<IP>:5000/repos

# post_loc.txt contains the json you want to post
# -p means to POST it
# -T sets the Content-Type
# -c is concurrent clients
# -n is the number of requests to run in the test
```

#### Test result(local):
- _Apache Bench_ based load-test result has given in file `ab_test_result.txt` with `n=20, c=4`.
- `time_metrict_results.txt` is the response time for a set of organizations called sequentially. Columns respectively as `organization name`, `response time in seconds`, `status code`.

## Bottleneck
- Access restriction `403 error` during multiple calls to `github` during testing/evaluation(api call limit from gitHub side). Couldn't increase value of _`n`_ during load test.
- No option to pass `excluding-fields` as parameter to restrict unwanted fields coming within result-json from `github`.
