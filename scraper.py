import re
from bs4 import BeautifulSoup
import logging
import cchardet
import exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

fileHandler = logging.FileHandler("scraper.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
streamHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler) 

async def fetchData(session, url, retailer):
    async with session.get(url) as response:    
        if (response.status == 200):
            logger.info(f"Successful request, url: {url} status code: {response.status}")

            html = await response.text()
            if (retailer == "hepsiburada"):
                return await extractDataHepsi(html)
            if (retailer == "gittigidiyor"):
                return await extractDataGG(html)            

        elif (response.status == 204):
            logger.info(f"There is no content, url: {url} status code: {response.status}")
            raise exceptions.NoContent(f"There is no content, url: {url} status code: {response.status}")
        elif (response.status >= 400):
            raise exceptions.FailedRequest(f"Request failed, url: {url} status code: {response.status}")


async def extractDataHepsi(html):
    soup = BeautifulSoup(html, "lxml")

    productDetail = soup.find("div", class_="productDetailContent")

    productData = productDetail.find("div", class_="product-information col lg-5 sm-1")

    productTitle = productData.find("h1", itemprop="name").text.strip()

    productPriceAndRatings = productData.find("div", class_="product-price-and-ratings")

    # Get value with correct floating point format
    productOriginalPrice = re.search(r"([0-9]*[.])?[0-9]+", productPriceAndRatings.find(id="originalPrice")\
    .text.replace(".", "").replace(",", ".")).group()   
    productOfferedPrice = productPriceAndRatings.find(id="offering-price")["content"]

    # Check discount. If it is not exist, assign price without discount to '-'
    if (productOriginalPrice == productOfferedPrice):
        productOriginalPrice = "-"

    productRatingsContainer = productPriceAndRatings.find("span", class_="ratings evaluate")
    productRating = productRatingsContainer.find("span", itemprop="ratingValue")["content"].replace(",", ".")
    productReviewCount = productRatingsContainer.find("span", itemprop="reviewCount")["content"]
    
    productImageContainer = productDetail.find(id="productDetailsCarousel")

    productMainImg = productImageContainer.find("a")
    productMainUrl = productMainImg.find("img")["src"]

    productImgs = productMainImg.find_next_siblings("a")
    productImgUrls = []
    if productImgs is not None:
        for img in productImgs:
            productImgUrls.append(img.find("img")["data-src"])

    return {"Title": productTitle, "Price": productOfferedPrice, 
            "Price Without Discount": productOriginalPrice,
            "Main Image": productMainUrl, "Images": productImgUrls, 
            "Rating Score": productRating, "Review Count": productReviewCount}


async def extractDataGG(html):
    soup = BeautifulSoup(html, "lxml")

    productDetail = soup.find(id="gallery-title-price-sellerInformation")

    productData = productDetail.find("div", class_="gg-w-13 gg-d-13 gg-t-24 gg-m-24 pr0 padding-none-m")

    productTitleRatingContainer = productData.find(id="badgeTitleReviewBrand")
    productTitle = productTitleRatingContainer.find(id="sp-title").text
    productRating = productTitleRatingContainer.find(id="sp-reviewAverage").text
    productReviewCount = productTitleRatingContainer.find(id="sp-reviewCommentCount").text

    productPriceContainer = productDetail.find(id="sp-price-container")
    # Get value with correct floating point format
    productOriginalPrice = re.search(r"([0-9]*[.])?[0-9]+", productPriceContainer.find(id="sp-price-highPrice")\
    .text.replace(".", "").replace(",", ".")).group() 
    productOfferedPrice = productPriceContainer.find(id="sp-price-lowPrice").text 

    # If there is no discount lower price div holds '\n', so check for it
    # Check discount. If it is not exist, assign price without discount to '-'
    if (productOfferedPrice == "\n"):
        productOfferedPrice = productOriginalPrice
        productOriginalPrice = "-"
    else:
        # Get value with correct floating point format
        productOfferedPrice = re.search(r"([0-9]*[.])?[0-9]+", productOfferedPrice\
        .replace(".", "").replace(",", ".")).group()

    productImageContainer = productDetail.find(id="gallery")
    
    productMainImg = productImageContainer.find(id="big-photo")
    productMainUrl = productMainImg["src"]

    productImgsUl = productImageContainer.find("ul", class_="product-photos-ul") 
    productImgs = productImgsUl.find_all("img")
    productImgUrls = []
    for img in productImgs:
        productImgUrls.append(img["swapimg"])    

    return {"Title": productTitle, "Price": productOfferedPrice, 
            "Price Without Discount": productOriginalPrice,
            "Main Image": productMainUrl, "Images": productImgUrls, 
            "Rating Score": productRating, "Review Count": productReviewCount}
    
