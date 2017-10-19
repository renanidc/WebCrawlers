# WebCrawlers
Este repositório contém Web Crawlers para extração de notícias dos principais portais brasileiros. Os Web Crawlers foram contruídos em python com o auxílio das bibliotecas: 

-[Requests](http://docs.python-requests.org/en/master/).

-[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

Os Web Crawlers construídos navegam automaticamente pelos sites selecionados e extraem as notícias. O Web Crawler separa as notícias por categoria e salva cada notícia em um arquivo .txt separado, sendo que cada categoria de notícia é separada em uma pasta diferente. O Web Crawler também salva as notícias em um arquivo .csv, sendo que esse arquivo contém:

+titulo da notícia

+texto da notícia

+categoria da noticia

+data de publicação da notícia
