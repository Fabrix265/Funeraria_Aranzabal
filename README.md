# Funeraria_Aranzabal

Activa el entorno virtual con:
venv\Scripts\Activate.ps1

Para correrlo:
uvicorn main:app

O para especificar un puerto(tiene que estar desactivado):
uvicorn main:app --port 8000

Para correrlo escuchando(no para produccion):
uvicorn main:app --port 8000 --reload

Para ver la documentacion:
http://localhost:8000/docs
http://localhost:8000/redoc