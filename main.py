import asyncio
import aiohttp
import scraper
import time

async def main():
    print(f"started at {time.strftime('%X')}")
    urls = ["https://www.gittigidiyor.com/sac-bakim/sac-bakim-ve-sampuan/sampuan/davines-energizing-dokulme-onleyici-sampuan-250-ml_spp_835744"]

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Referer":"https://www.google.com.tr",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "country-code": "Turkey"
    }
    tasks = []
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in urls:
            tasks.append(scraper.fetchData(session, url, "gg"))

        data = await asyncio.gather(*tasks)
        print(data)
    print(f"finished at {time.strftime('%X')}")
if __name__ == "__main__":
    asyncio.run(main())
