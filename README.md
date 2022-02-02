# telebot
Project chatbot EPU-D13CNPM4 to see timetable and test timetable
## FIRST
Download chrome-driver: https://chromedriver.chromium.org/home  
Download: tesseract-ocr: https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows or (google)  
IF MISSING FILE BUG... -> COPY BUG TO GOOGLE

### install chromedriver to `driver folder` and change path to the driver in crawl.py

### Setup environment
```
cp .env.template .env THEN Setup uri in .env file
python -m venv venv
source venv/bin/active
pip install -r requirements.txt
```
### RUN COMMANDS
```
export PYTHONPATH=$PWD
python src/main.py  -> run bot

python src/utils/database.py -> change code and run to check database
python src/utils/crawl.py -> check run selenium crawl
python src/model/train_modelv3.py -> uncomment train_model() and run to train_model
```