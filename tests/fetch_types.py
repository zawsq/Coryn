import aiohttp
import asyncio
import re
from pprint import pprint as print

async def fetch(session, url, pattern):
    async with session.get(url) as response:
        content = await response.text()
        match = re.search(pattern, content)
        return url, match.group(1) if match else None

async def main():
    url = 'https://coryn.club/item.php?type={}'
    pattern = r'class="content-subtitle">\s+\[ ([:0-9a-zA-Z\s]+)'
    type_names = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(29):
            url_type = url.format(i)
            tasks.append(fetch(session, url_type, pattern))
        results = await asyncio.gather(*tasks)
        for url, result in results:
            type_names[url] = result.strip() if result else result
    
    print((sorted(type_names.items(), key=lambda x: int(x[0].split('=')[-1]))))

if __name__ == '__main__':
    asyncio.run(main())