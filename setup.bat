#!/bin/bash

# Create and activate the virtual environment
python -m venv my_venv
source my_venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Notify the user that setup is complete
echo "Setup complete. Virtual environment activated."
