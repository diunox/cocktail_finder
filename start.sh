#!bin/sh
gunicorn app:app --config=config.py

