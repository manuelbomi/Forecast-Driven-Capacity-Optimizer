install:
	python -m pip install -r requirements.txt

test:
	pytest -q

api:
	uvicorn app.api:app --reload --port 8000

frontend:
	cd frontend && npm install && npm run dev

