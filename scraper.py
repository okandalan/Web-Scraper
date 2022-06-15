from bs4 import BeautifulSoup
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('scraper.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def fetchData(session, url):
    try:
        async with session.get(url) as response:
            html = await response.text()
    except Exception as e:
        logging.warning("Exception occured", exc_info=True)
    else:
        return await extractDataHepsi(html)

async def extractDataHepsi(html):
    soup = BeautifulSoup(html, "lxml")
    productDetail = soup.find('div', class_ = 'productDetailContent')

    productData = productDetail.find('div', class_ = "product-information col lg-5 sm-1")

    productTitle = productData.find('h1', itemprop = "name").text.strip()

    productPriceRatings = productData.find('div', class_ = "product-price-and-ratings")
    productOriginalPrice = productPriceRatings.find(id="originalPrice").text    # change , with . and strip whitespaces + TL
    productOfferedPrice = productPriceRatings.find(id="offering-price")["content"]
    productRatingsContainer = productPriceRatings.find('span', class_ = "ratings evaluate")
    productRating = productRatingsContainer.find('span', itemprop = "ratingValue")["content"] # change , with .
    productReviewCount = productRatingsContainer.find('span', itemprop = "reviewCount")["content"]

    productImageContainer = productDetail.find(id="productDetailsCarousel")

    productImages = productImageContainer.find_all('a')
    productMainImg = productImages[0].find('img')["src"]
    productImgUrls = []
    for i in productImages[1:]:
        productImgUrls.append(i.find('img')['data-src'])

    return {"Title": productTitle, "Price": productOfferedPrice, "Price Without Discount": productOriginalPrice, "Main Image": productMainImg, "Images": productImgUrls, "Rating Score": productRating, "Review Count": productReviewCount}    
