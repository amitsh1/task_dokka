# task_dokka

## install packages (python 3.7)
* pip install -r requirements.txt

## or use the Dockerfile
* docker build -t task_dokka .
* docker run -d -v ${PWD}:/app -p 5000:5000 task_dokka python /app/server.py

## run flask server
* python server.py

## example use
* curl -i -X POST -F filedata=@sample.csv "http://localhost:5000/api/getAddresses" 