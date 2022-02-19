# telebot
Project chatbot EPU-D13CNPM4 to see timetable and test timetable

## Download tesseract ocr
Download: tesseract-ocr: https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows or (google)
IF MISSING FILE BUG... -> COPY BUG TO GOOGLE


### Setup environment
```bash
cp .env.template .env -> then add bot token
python3.9 -m venv venv
source venv/bin/active
pip install -r requirements.txt
```
### RUN LOCAL
#### Export python path to pass error no module name
```bash
export PYTHONPATH=$PWD
```
#### Train model
```bash
python3.9 src/model/train_modelv3.py -> uncomment train_model() and run to train_model
```
#### Run bot
```bash
python3.9 src/main.py  -> run bot
```

### RUN WITH DOCKER
#### Build app
```bash
docker-compose build
```
#### Create .env file
```bash
cp .env.template .env -> change DB_URL=mongodb://mongo:MONGO@mongodb:27017
```
#### Start mongodb server
```bash
docker-compose up -d mongodb
```
#### Add user to mongodb
```bash
docker-compose exec mongodb mongo -u mongo -p MONGO
```
In mongo shell run command
```bash
use telebot;
db.createUser({user: "mongo", pwd: "MONGO", roles: [{role: "readWrite", db: "telebot"}]});
```
#### Start bot
```bash
docker-compose up -d bot
```