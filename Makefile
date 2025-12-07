.PHONY: install run-be run-fe

install:
	uv pip install -e .
	uv pip install -e '.[dev]'

run-be:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-fe:
	streamlit run streamlit_app.py --server.runOnSave true
