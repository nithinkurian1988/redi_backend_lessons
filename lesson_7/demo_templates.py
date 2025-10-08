from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/chatgpt")
def chatgpt(name: str):
    return templates.TemplateResponse("chat.html", {"request": {}, "user": name})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)