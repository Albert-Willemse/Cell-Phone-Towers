@echo off

rem Create and activate the virtual environment
python -m venv my_venv
call my_venv\Scripts\activate

rem Install dependencies from requirements.txt
pip install -r requirements.txt

echo Setup complete. Virtual environment activated.
