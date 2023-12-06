import asyncio
import concurrent.futures
import io

import aiohttp
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response
from PIL import Image, ImageFile

client_session = aiohttp.ClientSession()
pool = concurrent.futures.ProcessPoolExecutor()
app = FastAPI(title="dynasty-scans-proxy")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
ImageFile.LOAD_TRUNCATED_IMAGES = True


@app.get("/", include_in_schema=False)
async def route_index():
    return RedirectResponse("/docs")


def process_image(data):
    image = io.BytesIO()
    raw = Image.open(io.BytesIO(data))
    raw.save(image, format="webp", quality=90)
    return image.getvalue()


@app.get("/dynasty-scans-image/{path:path}")
async def route_dynasty_scans_image(request: Request, path: str):
    url = f"https://dynasty-scans.com/system/{path}?{request.query_params}"
    async with client_session.get(url) as response:
        data = await response.read()

    loop = asyncio.get_running_loop()
    image = await loop.run_in_executor(pool, process_image, data)

    return Response(
        content=image,
        media_type="image/webp",
        headers={"Cache-Control": f"max-age={24 * 60 * 60}"}
    )
