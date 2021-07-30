from typing import Dict, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os 
import requests
import re
import time 
from .produtos import Product, Megasena, Lotofacil
import unidecode


class Loader():

    """
    Library to load all results of federal lottery of Brazil
    
    Found the chromedrive here:
    https://chromedriver.chromium.org/downloads 

    returns the return dataset containing all results
    """
    
    produtos: List = [Megasena, Lotofacil]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    implicitly_wait: int = 5
    sleep_wait: int = 10

    @staticmethod
    def sanitize_page_source(page_source: str) -> str:
        """
        sanitize the page source removing all unecessary data
        """
        page_source = re.sub(r"[\t\n]+"," ", unidecode.unidecode(page_source))
        page_source = re.sub(r"\s\s+","", page_source)
        page_source = page_source.replace('<tr bgcolor="#b5ffbd"><tr>','<tr>')
        page_source = page_source.replace('<tr bgcolor="#b5ffbd"></tr><tr>','<tr>')
        page_source = page_source.replace('<tr bgcolor="#FFFFFF"><tr>','<tr>')
        page_source = page_source.replace('<tr bgcolor="#FFFFFF"></tr>','')
        page_source = page_source.replace('<tbody>','')
        page_source = page_source.replace('</tbody>','')
        page_source = page_source.replace('nmeros','numeros')
        page_source = page_source.replace('<th ','<td ')
        page_source = page_source.replace('</th>','</td>')
        page_source = page_source.replace('ú','</td>')
        page_source = page_source.replace('<td>CANAL ELETRONICO </td> <td>--</td> </tr><tr> ','')
        page_source = re.sub(r'<table><!-- LINHA DA CIDADE-->([^!]+)!-- FIM LINHA CIDADE--></table>',"</td>", page_source)

        return page_source

    @staticmethod
    def load_data() -> List:

        chrome_options = Options()
        #chrome_options.add_argument("--headless") 

        browser = webdriver.Chrome(executable_path=Loader.dir_path+'/../config/chromedriver', options=chrome_options)
        browser.implicitly_wait(Loader.implicitly_wait)

        url_arquivos: Dict[str, str] = {}
        response_server: bytes = b''
        
        dataset = {}

        for produto in Loader.produtos:

            browser.get(Product.get_url(produto))
            browser.implicitly_wait(Loader.implicitly_wait)
            wait = WebDriverWait(browser, 20)
            
            link_download: WebElement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.title.zeta')))
            link_download.click()
            browser.close()

            time.sleep(Loader.sleep_wait)

            browser.switch_to.window(browser.window_handles[-1])
            wait.until(EC.title_contains('Resultado'))
            
            page_source = Loader.sanitize_page_source(browser.page_source)

            soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')

            datalist: List[Dict] = [] 
            counter: int = 0
            fields: List = []
            table = soup.find('table')
            
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if counter == 0:
                    for column_name in columns:
                        column_name = re.sub(r'\s+','_',column_name.text.strip().lower())
                        fields.append(column_name)
                else:
                    idx = 0
                    row_data: Dict = {}
                    for value in columns:
                        row_data[fields[idx]] = value.text.strip()
                        idx += 1
                    datalist.append(row_data)
                counter += 1

            dataset[produto.slug] = datalist
            wait = WebDriverWait(browser, 20)
        
        browser.quit()
        return dataset