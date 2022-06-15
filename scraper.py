from itertools import product
from bs4 import BeautifulSoup
import logging
import cchardet


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("scraper.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def fetchData(session, url):
    try:
        async with session.get(url) as response:
            html = await response.text()
    except Exception as e:
        logging.warning("Exception occured", exc_info=True)
    else:
        return await extractDataGG(html)


async def extractDataHepsi(html):
    soup = BeautifulSoup(html, "lxml")

    productDetail = soup.find("div", class_ = "productDetailContent")

    productData = productDetail.find("div", class_ = "product-information col lg-5 sm-1")

    productTitle = productData.find("h1", itemprop = "name").text.strip()

    productPriceAndRatings = productData.find("div", class_ = "product-price-and-ratings")
    productOriginalPrice = productPriceAndRatings.find(id="originalPrice").text    # change , with . and strip whitespaces + TL
    productOfferedPrice = productPriceAndRatings.find(id="offering-price")["content"]

    productRatingsContainer = productPriceAndRatings.find("span", class_="ratings evaluate")
    productRating = productRatingsContainer.find("span", itemprop="ratingValue")["content"] # change , with .
    productReviewCount = productRatingsContainer.find("span", itemprop="reviewCount")["content"]

    productImageContainer = productDetail.find(id="productDetailsCarousel")

    productMainImg = productImageContainer.find("a")
    productMainUrl = productMainImg.find("img")["src"]

    productImgs = productMainImg.find_next_siblings("a")
    productImgUrls = []
    for img in productImgs:
        productImgUrls.append(img.find("img")["data-src"])

    return {"Title": productTitle, "Price": productOfferedPrice, 
            "Price Without Discount": productOriginalPrice,
            "Main Image": productMainUrl, "Images": productImgUrls, "Rating Score": productRating,
            "Review Count": productReviewCount}


async def extractDataGG(html):
    soup = BeautifulSoup(html, "lxml")

    productDetail = soup.find(id="gallery-title-price-sellerInformation")

    productData = productDetail.find("div", class_="gg-w-13 gg-d-13 gg-t-24 gg-m-24 pr0 padding-none-m")

    productTitleRatingContainer = productData.find(id="badgeTitleReviewBrand")
    productTitle = productTitleRatingContainer.find(id="sp-title").text
    productRating = productTitleRatingContainer.find(id="sp-reviewAverage").text
    productReviewCount = productTitleRatingContainer.find(id="sp-reviewCommentCount").text

    productPriceContainer = productDetail.find(id="sp-price-container")
    productOriginalPrice = productPriceContainer.find(id="sp-price-highPrice").text.strip()
    productOfferedPrice = productPriceContainer.find(id="sp-price-lowPrice") # olmama durumuna bakılacak

    productImageContainer = productDetail.find(id="gallery")
    
    productMainImg = productImageContainer.find(id="big-photo")
    productMainUrl = productMainImg["src"]

    productImgsUl = productImageContainer.find("ul", class_="product-photos-ul") # normalde ul den sonra boşluk var ama çalışmıyor öyle
    productImgs = productImgsUl.find_all("img")
    productImgUrls = []
    for img in productImgs:
        productImgUrls.append(img["data-zoom-image"])    

    return {"Title": productTitle, "Price": productOfferedPrice, 
            "Price Without Discount": productOriginalPrice,
            "Main Image": productMainUrl, "Images": productImgUrls, "Rating Score": productRating,
            "Review Count": productReviewCount}
    
