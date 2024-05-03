from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
import os
from routes.general import general_router
from routes.proceso import proceso_router
from routes.user import user_router
from routes.causa import causas_router

# Directorio base donde se encuentra el script de servidor
base_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="Test Tus datos",
    description="this is a simple REST API using fastapi and mongodb",
    version="0.0.1"
)

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(general_router)
app.include_router(proceso_router, prefix="/proceso")
app.include_router(user_router, prefix="/auth")
app.include_router(causas_router, prefix="/causas")

# Configurar la ruta de los archivos estáticos de React de manera relativa
static_dir = os.path.join(base_dir, "frontend/dashboard/build/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configurar la ruta principal para servir la aplicación React
templates_dir = os.path.join(base_dir, "frontend/dashboard/build")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
