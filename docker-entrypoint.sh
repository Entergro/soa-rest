#!/bin/bash -e

uvicorn main:app --host 0.0.0.0 --port 80 | python3 worker.py

