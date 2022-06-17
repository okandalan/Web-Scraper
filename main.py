import time
import random
import sys
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

formatter = logging.Formatter("%(levelname)s :: %(name)s :: %(message)s")

fileHandler = logging.FileHandler("scraper.log")
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.INFO)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler) 


async def main(formats, fileName = None):
    print(f"started at {time.strftime('%X')}")

    urls = []
    # Reading url inputs into url
    if (fileName):
        with open(fileName) as file:
            for line in file:
                line = line.rstrip()
                if (line == ""):
                    continue
                urls.append(line)

    # Ordering HTTP headers to prevent getting blocked
    ordHeaders = OrderedDict([ 
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"),
        ("Accept-Encoding", "gzip, deflate, br"),
        ("Accept-Language", "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"),
        ("Referer", "https://www.google.com.tr"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0")
    ])

    # Clering log file
    with open('scraper.log', 'w'):
        pass

    tasks = []
    # Setting timeout value for get request
    timeout = aiohttp.ClientTimeout(total=10)
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
        
    # Catching Exceptions in the data
    for exception in data:
        try:
            if (isinstance(exception, Exception)):
                raise exception
        except asyncio.exceptions.TimeoutError:
            logger.error(f"Get request takes more than timeout value: {timeout.total} seconds", exc_info=True)
        except exceptions.NoContent as e:
            logger.error(str(e), exc_info=True)
        except exceptions.FailedRequest as e:
            logger.error(str(e), exc_info=True)
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error: {str(e)}", exc_info=True)
        except aiohttp.ClientError as e:
            logger.error(f"Error: {str(e)}", exc_info=True)

    # Exporting selected formats
    if ("excel" in formats):
        export.exportToExcel(data)
    if ("csv" in formats):
        export.exportToCsv(data)

    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    # Command line arguments error handling
    if (not (3 <= len(sys.argv) <= 4)):
        raise exceptions.WrongNumberOfArguments()

    formats = []
    if (len(sys.argv[:-1]) == 3):
        if ("excel" in sys.argv and "csv" in sys.argv):
            formats.append("excel")
            formats.append("csv")
        else:
            raise exceptions.InvalidArguments()
    if (len(sys.argv[:-1]) == 2):
        if ("excel" in sys.argv[:-1]):
            formats.append("excel")
        elif ("csv" in sys.argv[:-1]):
            formats.append("csv")
        else:
            raise exceptions.InvalidArguments()

    fileName = sys.argv[-1]

    asyncio.run(main(formats, fileName))