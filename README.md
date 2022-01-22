# telebot
## first
Download chrome-driver: https://chromedriver.chromium.org/home  
Download: tesseract-ocr: https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows or (google)  
IF MISSING FILE BUG... -> COPY BUG TO GOOGLE

### install chrome-driver and change path in crawl.py
## RUN
```
python -m venv venv
source venv/bin/active
pip install -r requirements.txt
```
```
copy .env.template .env -> change .env file
export PYTHONPATH=$PWD

python src/main.py  -> run bot
python src/utils/database.py -> change code and run to check database
python src/utils/crawl.py -> check run selenium crawl
```