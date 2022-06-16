from asyncio import exceptions
from asyncio.log import logger
import time
import asyncio
import aiohttp
import logging
import exceptions
import scraper
import export



async def main():
    print(f"started at {time.strftime('%X')}")
    urls = ["https://okandalan.github.io/15", "https://www.hepsiburada.com/dreame-v10-pro-dikey-kablosuz-sarjli-supurge-genpa-garantili-p-HBV0000188N7U",
            "https://www.hepsiburada.com/fantom-p-1200-pratic-kirmizi-kuru-supurge-p-evfanprap1200"]

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Referer":"https://www.google.com.tr",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "country-code": "Turkey"
    }
    tasks = []
    
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        for url in urls:
            if "hepsiburada" in url:
                retailer = "hepsiburada"
            elif "gittigidiyor" in url:
                retailer = "gittigidiyor"
            task = scraper.fetchData(session, url, retailer)
            tasks.append(task)
        
        # return_exceptions=True append raised Exceptions to data so they can be catched
        data = await asyncio.gather(*tasks, return_exceptions=True)
        

    for i in data:
        try:
            # Catched Exceptions in the data
            if (isinstance(i, Exception)):
                raise i
        except Exception as e:
            logger.exception(f"Error: {str(e)}")

    print(data)
    export.exportToCsv(data)
    export.exportToExcel(data)

    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())
