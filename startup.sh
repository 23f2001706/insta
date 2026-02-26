#!/bin/bash

# Exit on error
set -e

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the Flask app with gunicorn
gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:8000 app:app
