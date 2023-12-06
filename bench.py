import asyncio
import time
import aiohttp

# Source: https://dynasty-scans.com/chapters/myself
data = [
    {"image": "/system/releases/000/039/756/001.png", "name": "001"},
    {"image": "/system/releases/000/039/756/002.png", "name": "002"},
    {"image": "/system/releases/000/039/756/003.png", "name": "003"},
    {"image": "/system/releases/000/039/756/004.png", "name": "004"},
    {"image": "/system/releases/000/039/756/005.png", "name": "005"},
    {"image": "/system/releases/000/039/756/006.png", "name": "006"},
    {"image": "/system/releases/000/039/756/007.png", "name": "007"},
    {"image": "/system/releases/000/039/756/008.png", "name": "008"},
    {"image": "/system/releases/000/039/756/009.png", "name": "009"},
    {"image": "/system/releases/000/039/756/010.png", "name": "010"},
    {"image": "/system/releases/000/039/756/011.png", "name": "011"},
    {"image": "/system/releases/000/039/756/012.png", "name": "012"},
    {"image": "/system/releases/000/039/756/013.png", "name": "013"},
    {"image": "/system/releases/000/039/756/014.png", "name": "014"},
    {"image": "/system/releases/000/039/756/015.png", "name": "015"},
    {"image": "/system/releases/000/039/756/016.png", "name": "016"},
    {"image": "/system/releases/000/039/756/017.png", "name": "017"},
    {"image": "/system/releases/000/039/756/018.png", "name": "018"},
    {"image": "/system/releases/000/039/756/019.png", "name": "019"},
    {"image": "/system/releases/000/039/756/020.png", "name": "020"},
    {"image": "/system/releases/000/039/756/021.png", "name": "021"},
    {"image": "/system/releases/000/039/756/022.png", "name": "022"},
    {"image": "/system/releases/000/039/756/credits.png", "name": "credits"}
]


async def run_test():
    buster = f"?t={time.time_ns()}"
    async with aiohttp.ClientSession() as session:
        total_difference = 0
        for entry in data:
            print(f"{entry['name']}\t... ", end='', flush=True)

            # Request from proxy first to avoid
            # possible warm start advantage.
            start = time.time()
            base = "https://dynasty-scans-proxy.nsk.sh/dynasty-scans-image"
            proxied_url = f"{base}/{'/'.join(entry['image'].split('/')[2:])}"
            async with session.get(proxied_url + buster) as response:
                proxied_body = await response.read()
            proxied_time = time.time() - start

            start = time.time()
            original_url = "https://dynasty-scans.com" + entry['image']
            async with session.get(original_url + buster) as response:
                original_body = await response.read()
            original_time = time.time() - start

            difference = proxied_time - original_time
            total_difference += difference
            size_proportion = len(proxied_body) / len(original_body)
            print(f"{difference:+.02f}s ({size_proportion:.0%} in size)")

        print("---")
        print(f"Total difference: {total_difference:+.02f}s")
        print(f"Average: {total_difference / len(data):+.02f}s")


asyncio.run(run_test())
