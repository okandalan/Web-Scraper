import imp
import time
import random
from collections import OrderedDict
import asyncio
import aiohttp
import logging
import exceptions
import scraper
import export
import user_agents

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

fileHandler = logging.FileHandler("scraper.log")
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.INFO)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler) 


async def main():
    print(f"started at {time.strftime('%X')}")
    urls = ["https://www.hepsiburada.com/dreame-v10-pro-dikey-kablosuz-sarjli-supurge-genpa-garantili-p-HBV0000188N7U",
            "https://hepsiburada.github.io/",   
            "https://www.hepsiburada.com/fantom-p-1200-pratic-kirmizi-kuru-supurge-p-evfanprap1200"]

    # Order HTTP headers to prevent getting blocked
    ordHeaders = OrderedDict([ 
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"),
        ("Accept-Encoding", "gzip, deflate, br"),
        ("Accept-Language", "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"),
        ("Referer", "https://www.google.com.tr"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0")
    ])

    with open('scraper.log', 'w'):
        pass

    tasks = []
    
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(headers=ordHeaders, timeout=timeout) as session:
        for url in urls:
            # Rotate user agent to prevent getting blocked
            session.headers["User-Agent"] = random.choice(user_agents.userAgents)
            
            if "hepsiburada" in url:
                retailer = "hepsiburada"
            elif "gittigidiyor" in url:
                retailer = "gittigidiyor"
            else:
                continue
            task = scraper.fetchData(session, url, retailer)
            tasks.append(task)
        
        # return_exceptions=True append raised Exceptions to data so they can be catched
        data = await asyncio.gather(*tasks, return_exceptions=True)
        
    # Catched Exceptions in the data
    for exception in data:
        try:
            if (isinstance(exception, Exception)):
                raise exception
        except exceptions.NoContent as e:
            logger.error(str(e), exc_info=True)
        except exceptions.FailedRequest as e:
            logger.error(str(e), exc_info=True)
        except aiohttp.ServerTimeoutError as e:
            logger.error(f"Timeout error: {str(e)}", exc_info=True)
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error: {str(e)}", exc_info=True)
        except aiohttp.ClientError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)

    export.exportToCsv(data)
    export.exportToExcel(data)

    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())
