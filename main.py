import scraper
import asyncio
import aiohttp
import time

async def main():
    print(f"started at {time.strftime('%X')}")
    urls = ["https://www.hepsiburada.com/dreame-v10-pro-dikey-kablosuz-sarjli-supurge-genpa-garantili-p-HBV0000188N7U",
            "https://www.hepsiburada.com/arnica-merlin-pro-2-si-1-arada-850-watt-dikey-elektrikli-supurge-p-evarnmerlinpro", 
            "https://www.hepsiburada.com/arnica-et13311-tria-pro-dik-elektrikli-supurge-p-hbv00000pjbwd"]

    headers = {
        'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        'Referer':"https://www.google.com.tr",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language': "en-US,en;q=0.5",
        'country-code': "Turkey"
    }
    tasks = []
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in urls:
            tasks.append(scraper.fetchData(session, url))

        data = await asyncio.gather(*tasks) 
    print(f"finished at {time.strftime('%X')}")
if __name__ == "__main__":
    asyncio.run(main())
