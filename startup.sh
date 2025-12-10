#!/bin/bash
gunicorn --bind 0.0.0.0:${PORT:-8000} app:app

