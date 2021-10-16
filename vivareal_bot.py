# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:18:56 2021

@author: mateuscarvalho
"""

# Importações
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
from tqdm import tqdm
from datetime import datetime

# Inicializando o Webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Dicionário de urls
urls_dict = {"Brooklin": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/brooklin/apartamento_residencial/",
             "Butanta": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/butanta/apartamento_residencial/",
             "Republica": "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/republica/apartamento_residencial/",
             "Bras": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/bras/apartamento_residencial/",
             "Freguesia do O": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/freguesia-do-o/apartamento_residencial/",
             "Higienopolis": "https://www.vivareal.com.br/venda/sp/sao-paulo/centro/higienopolis/apartamento_residencial/",
             "Jardins": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/jardins/apartamento_residencial/",
             "Lapa": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/lapa/apartamento_residencial/",
             "Moema": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/moema/apartamento_residencial/", 
             "Mooca": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/mooca/apartamento_residencial/",
             "Morumbi": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/morumbi/apartamento_residencial/",
             "Pinheiros": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/pinheiros/apartamento_residencial/",
             "Santana": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/santana/apartamento_residencial/",
             "Saude": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/saude/apartamento_residencial/",
             "Vila Mariana": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/vila-mariana/apartamento_residencial/",
             "Vila Matilde": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-leste/vila-matilde/apartamento_residencial/",
             "Campo limpo": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-sul/campo-limpo/apartamento_residencial/",
             "Tucuruvi": "https://www.vivareal.com.br/venda/sp/sao-paulo/zona-norte/tucuruvi/apartamento_residencial/",
             "Fortaleza": "https://www.vivareal.com.br/venda/ceara/fortaleza/"
             }

#Criando a lista que irá armazenar todos os resultados
results = []

# Iniciando o for para iterar no dicionário de urls
for bairro, url in urls_dict.items():
    driver.get(url)
    sleep(2)
    
    try:
        driver.find_element_by_class_name("cookie-notifier__cta").click()
    except:
        print("No cookies!")
    
    for i in tqdm(range(30), desc=bairro):
        sleep(10)
        #Capturando somente o bloco com os apartamentos
        main_div = driver.find_element_by_class_name("results-main__panel")
        properties = main_div.find_elements_by_class_name("js-property-card")
        # Realizando a paginação 
        paginator = driver.find_element_by_class_name("js-results-pagination")
        next_page = paginator.find_element_by_xpath("//a[@title='Próxima página']")
        
        #For para capturar as informações de cada apartamento (Id, endereço, n°quartos, tamanho, garagens etc)
        for i, apartment in enumerate(properties):
            #Capturando o link do apartamento
            url = apartment.find_element_by_class_name("js-card-title").get_attribute("href")
            #Capturando o id do link
            apto_id = url.split("id-")[-1][:-1]
            #Capturando o título do anúncio
            header = apartment.find_element_by_class_name("property-card__title").text
            
            #Capturando o endereço do imóvel
            try:
                address = apartment.find_element_by_class_name("property-card__address").text
            except:
                adress = None
            #Capturando a área do imóvel
            try:
                area = apartment.find_element_by_class_name("js-property-card-detail-area").text
            except:
                area = None
            #capturando a quantidade de quarto
            try:
                rooms = apartment.find_element_by_class_name("js-property-detail-rooms").text
            except:
                rooms = None
            #Capturando a quantidade de banheiros
            try:
                bathrooms = apartment.find_element_by_class_name("js-property-detail-bathroom").text
            except:
                bathrooms = None
            #Capturando a quantidade de garagens
            try:
                garages = apartment.find_element_by_class_name("js-property-detail-garages").text
            except:
                garages = None
            #Capturando os amenities(informações adicionais sobre o imóvel)
            try:
                amenites = apartment.find_element_by_class_name("property-card__amenities").text
            except:
                amenites = None
            #Capturando o preço do apartamento
            try:
                price = apartment.find_element_by_class_name("js-property-card-prices").text
            except:
                price = None
            #Capturando o preço do condomínio
            try:
                condo = apartment.find_element_by_class_name("js-condo-price").text
            except:
                condo = None
            #Criando um campo com a data de execução do Crawler    
            crawled_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            #Criando um dicionário de resultados
            results.append({"id":apto_id,
                            "url": url,
                            "header": header,
                            "address": address,
                            "area": area,
                            "bathrooms": bathrooms,
                            "garages": garages,
                            "amenites": str(amenites).replace("\n", " "), #Deixando as informações adicionais na mesma linha
                            "price": str(price).split("\n")[-1], #Alguns imóveis possui o valor de aluguel e o valor de venda, estou pegando o de venda
                            "condo":condo,
                            "bairro":bairro,
                            "crawled_at": crawled_at})
        #Clicando na próxima página    
        try:
            next_page.click()
        except:
            print("Next page not clickable")
            break

#Exportando em um arquivo Excel
pd.DataFrame(results).to_csv("Crawler_vivaReal.csv", index=False, encoding='utf-8-sig')
#Fechando o google Chrome
driver.close()
            
            
            
        

