#!/bin/bash

poetry run alembic upgrade head
poetry run fastapi run curso_fast/app.py --host 0.0.0.0 --port 8000