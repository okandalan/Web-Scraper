# Web-Scraper
Web Scraper scrapes e-commerce websites' products data such as price, price without discount, main image URL, other image URLs, title, rating and review count. Then export them in supported file formats.

## Supported websites:
Hepsiburada <br />
Gittigidiyo

## Supported formats:
csv <br /> 
Xlsx(Excel)

## How to install requirements:
`pip install -r requirements.txt`

## Usage:
Scraper takes format and urls of products pages as input. You should put your input urls in file. There should be one url for each line and put your input file in same folder as other *.py files. <br />
Input file example:
```
url1
url2
url3
```
Now you can run scraper with this format.`python (or python3) main.py format1 format2 (if you want you can give only one format) input_file` <br />
Examples: <br />
`python3 main.py excel csv products_urls.txt` <br />
`python3 main.py csv products_urls.txt` <br />
`python3 main.py excel  products_urls.txt` <br />
After program finished, you can see your exported files in exported_files directory and loggings in scraper.log




    
    




