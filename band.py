# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class band:

	#Metodo para extrair dados da noticia e salvar em CSV
	def salvarNoticias(self):

		#Define objeto writer para gravar no arquivo CSV
		arquivo = csv.writer (open("Band.csv", "a"), delimiter="|")

		#Abre arquivo de links
		links = open ('links/linksBand.txt', 'r')

		#Laço para percorrer linhas do arquivo de links
		for linha in links:		
			
			#Cada linha do arquivo contém um link
			link = linha

			#Acessa link da noticia (requisição)
			r = requests.get(link)

			#Recebe conteúdo HTML da noticia
			noticia_html = BeautifulSoup (r.content)	

			#Extrai dados do HTML
			titulo = noticia_html.find('h1', attrs={'class':'titulo_noticia '}).text
			texto = noticia_html.find('span', attrs={'itemprop':'articleBody'}).text		 
			categoria = 'economia'
			data_publicacao = noticia_html.find ('span', attrs={'itemprop':'datePublished'}).text
			data_captura_noticia = datetime.now()

			#Imprime titulo da noticia no terminal
			print titulo.encode('utf-8')

			#Escreve linha no arquivo CSV com os dados extraídos da notícia
			try:
				arquivo.writerow([titulo.encode('utf-8'),texto.encode('utf-8'),categoria,
								data_publicacao.encode('utf-8'), data_captura_noticia, link])
			except:
				print 'ERRO DE UNICODE!'

	#Metodo para capturar os links das noticias
	def capturarLinks(self):

		print 'Crawleando: http://noticias.band.uol.com.br/economia/ ...' 

		i = 1 #Contador para percorrer paginação do site
		r = requests.get('http://noticias.band.uol.com.br/economia/?page=' + str(i))
		soup = BeautifulSoup (r.content) #recebe conteúdo HTML da requisição		

		#Laço para navegar na paginação do site
		while i <= 10:
			#Laço para encontrar noticias pelo atributo class do HTML 
			for noticia in soup.findAll('ul', attrs={'class':'lista-noticias-nova-home'}):
				#Captura link da noticia
				link = noticia.find ('a')['href']
				print link

				#Grava link no arquivo
				arquivo = open("links/linksBand.txt", "a")
				try:
					arquivo.write (link + '\n')
				except:
					print 'ERRO DE UNICODE'				

			#Incrementa contador de paginação
			i=i+1 
			#Gera requisição para próxima página
			r = requests.get('http://noticias.band.uol.com.br/economia/?page=' + str(i))
			soup = BeautifulSoup (r.content) #recebe conteúdo HTML da nova requisição