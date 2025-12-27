import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mangum import Mangum # 引入适配器

app = FastAPI(title="Quantum Dual-Persona")

# --- 关键修改 1: 获取绝对路径 ---
# 在服务器上，相对路径可能会出错，所以我们用 os 获取当前文件的绝对位置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 挂载静态文件
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 设置模板目录
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- 路由部分 (保持不变) ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mode/academic", response_class=HTMLResponse)
async def get_academic_mode(request: Request):
    data = {
        "name": "Li Ming",
        "title": "Data Scientist",
        "gpa": "3.9 / 4.0 (Magna Cum Laude)",
        "university": "Tsinghua University",
        "skills": ["Python (Pandas, NumPy)", "Bayesian Inference", "TensorFlow", "PostgreSQL"]
    }
    return templates.TemplateResponse("academic.html", {"request": request, **data})

@app.get("/mode/cyberpunk", response_class=HTMLResponse)
async def get_cyberpunk_mode(request: Request):
    data = {
        "alias": "Ghost_0x1",
        "role": "Full Stack Netrunner",
        "power": "OVER 9000",
        "guild": "Society of The Glitch",
        "loot": ["FastAPI Exploits", "Linux Kernel Hacking", "Reverse Engineering", "Coffee.exe"]
    }
    return templates.TemplateResponse("cyberpunk.html", {"request": request, **data})

@app.post("/action/contact-academic", response_class=HTMLResponse)
async def contact_academic():
    import asyncio
    await asyncio.sleep(0.5)
    return """
    <span class="ml-4 text-gray-700 font-serif italic fade-in-up">
        📧 email: <a href="#" class="underline hover:text-blue-600">li.ming@tsinghua.edu.cn</a>
    </span>
    """

@app.post("/action/contact-cyberpunk", response_class=HTMLResponse)
async def contact_cyberpunk():
    return """
    <span class="ml-4 text-green-400 font-mono text-sm">
        <span class="animate-pulse">📟 ENC_ID: 994-231-X [SECURE]</span>
    </span>
    """

# --- 关键修改 2: Mangum 适配器 ---
# Netlify 会寻找这个 handler 变量来运行程序
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
