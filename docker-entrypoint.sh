#!/bin/sh

port=${PORT-8000}

cd collections_core && alembic upgrade head
cd ../ && uvicorn collections_core.main:app --host 0.0.0.0 --port "$port"
