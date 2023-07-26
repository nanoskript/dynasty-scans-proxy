import asyncio
import concurrent.futures
import io

import aiohttp
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response
from PIL import Image

client_session = aiohttp.ClientSession()
pool = concurrent.futures.ProcessPoolExecutor()
app = FastAPI(title="dynasty-scans-proxy")
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/", include_in_schema=False)
async def route_index():
    return RedirectResponse("/docs")


def process_image(data):
    image = io.BytesIO()
    raw = Image.open(io.BytesIO(data))
    raw.save(image, format="webp", quality=90)
    return image.getvalue()


@app.get("/dynasty-scans-image/{p1}/{p2}/{p3}/{p4}")
async def route_dynasty_scans_image(p1: str, p2: str, p3: str, p4: str):
    url = f"https://dynasty-scans.com/system/releases/{p1}/{p2}/{p3}/{p4}"
    async with client_session.get(url) as response:
        data = await response.read()

    loop = asyncio.get_running_loop()
    image = await loop.run_in_executor(pool, process_image, data)

    return Response(
        content=image,
        media_type="image/webp",
        headers={"Cache-Control": f"max-age={24 * 60 * 60}"}
    )
