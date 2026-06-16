setup:
	pip install -r requirements.txt

format:
	black .

lint:
	ruff check .

test:
	pytest

run:
	streamlit run app.py

freeze:
	pip freeze > requirements.txt
