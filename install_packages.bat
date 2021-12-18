@echo off

echo Installing required packages...

call python -m venv venv

call ./venv/Scripts/activate

call pip install -r requirements.txt

call npm install

call npm install -g mapshaper