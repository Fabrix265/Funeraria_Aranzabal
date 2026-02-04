from fastapi import FastAPI

app = FastAPI()

app.title = "Inventario Funeraria Aranzabal API"
app.version = "1.0"

@app.get("/", tags=["Home"])
def home():
    return "Funcionando"

