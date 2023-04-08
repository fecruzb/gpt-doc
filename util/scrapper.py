from llama_index import download_loader
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin
from llama_index.node_parser import SimpleNodeParser

def url_to_urls(url):
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, features="html.parser")
    urls = []
    for link in soup.findAll('a'):
        href = link.get("href")
        if href and not urlparse(href).netloc:
            urls.append(urljoin(url, href))

    print(urls)
        
    return urls

def url_to_nodes(url):
    urls = url_to_urls(url)
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    documents = loader.load_data(urls)
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    return nodes