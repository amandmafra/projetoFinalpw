from fastapi import FastAPI, Form, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import User, OrderForm
from starlette.exceptions import HTTPException 

app = FastAPI()
router = APIRouter()

SQLALCHEMY_DATABASE_URL = "sqlite:///./cafe.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/js", StaticFiles(directory="js"), name="js")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Rotas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...),email: str = Form(...) ,cpf: str = Form(...), db: Session = Depends(get_db)):
    new_user = User(username=username, password=password, cpf=cpf,email=email)
    db.add(new_user)
    db.commit()

    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/cafe1", response_class=HTMLResponse)
async def cafe1(request: Request):
    return templates.TemplateResponse("cafe1.html", {"request": request})

@app.get("/cafe2", response_class=HTMLResponse)
async def cafe2(request: Request):
    return templates.TemplateResponse("cafe2.html", {"request": request})

@app.get("/cafe3", response_class=HTMLResponse)
async def cafe3(request: Request):
    return templates.TemplateResponse("cafe3.html", {"request": request})

@app.get("/cafe4", response_class=HTMLResponse)
async def cafe4(request: Request):
    return templates.TemplateResponse("cafe4.html", {"request": request})

@app.post("/cafe1", response_class=HTMLResponse)
async def post_cafe1(request: Request, form: OrderForm):
    return templates.TemplateResponse("cafe1.html", {"request": request, "form": form})

@app.post("/cafe2", response_class=HTMLResponse)
async def post_cafe2(request: Request, form: OrderForm):
    return templates.TemplateResponse("cafe2.html", {"request": request, "form": form})

@app.post("/cafe3", response_class=HTMLResponse)
async def post_cafe3(request: Request, form: OrderForm):
    return templates.TemplateResponse("cafe3.html", {"request": request, "form": form})

@app.post("/cafe4", response_class=HTMLResponse)
async def post_cafe4(request: Request, form: OrderForm):
    return templates.TemplateResponse("cafe4.html", {"request": request, "form": form})

@router.get("/search")
async def get_search(request: Request):
    return JSONResponse(content={"message": "GET request to search endpoint"})

@router.post("/search")
async def post_search(request: Request):
    data = await request.json()
    search_term = data.get("search_term")
    if search_term == 'cafe' or search_term == 'café':
        return JSONResponse(content={"redirect_url": "/cafe2"})
    elif search_term == 'bebida gourmet':
        return JSONResponse(content={"redirect_url": "/cafe1"})
    elif search_term == 'cafeteiras':
        return JSONResponse(content={"redirect_url": "/cafe3"})
    elif search_term == 'capsulas' or search_term == 'cápsulas':
        return JSONResponse(content={"redirect_url": "/cafe4"})
    else:
        return JSONResponse(content={"message": "Nenhuma correspondência encontrada."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
