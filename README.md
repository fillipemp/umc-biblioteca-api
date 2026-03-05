# umc-biblioteca-api

# Rodar comando no terminal para inicio do sistema:

python -m venv .venv

# Windows: .venv\Scripts\activate

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload

# Abrir sistema na Web:
# http://127.0.0.1:8000/docs 