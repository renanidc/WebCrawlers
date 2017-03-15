# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

class g1: 

	#Metodo para extrair dados da noticia e salvar em CSV
	def salvarNoticias(self):

		#Atributos da notícia
		noticia_html=""	
		titulo = ""
		texto = ""
		categoria = ""
		data_publicacao = ""		

		#Define objeto writer para gravar no arquivo CSV
		arquivo = csv.writer (open("CSV/G1.csv", "a"), delimiter="|")

		#Abre arquivo de links
		links = open ('links/linksG1.txt', 'r')

		#Laço para percorrer linhas do arquivo de links
		for linha in links:		
			
			#Cada linha do arquivo contém um link
			link = linha

			#Tenta acessar link da noticia
			try:
				#Acessa link da noticia (requisição)
				r = requests.get(link)

				#Recebe conteúdo HTML da noticia
				noticia_html = BeautifulSoup (r.content)
			except:
				print 'ERRO DE CONEXÃO!'

			#Extrai dados do HTML
			try:
				titulo = noticia_html.find('h1', attrs={'class':'entry-title'}).text
				
				#Imprime titulo da noticia no terminal
				print titulo.encode('utf-8')
				
				texto = noticia_html.find('div', attrs={'id':'materia-letra'})

				#Remover tags script do HTML
				for script in texto(["script"]):
					script.extract()

				texto = texto.text #Recebe texto puro, sem tags HTML

				categoria = noticia_html.find('a', attrs={'class':'logo'}).text		
				data_publicacao = noticia_html.find ('abbr', attrs={'class':'updated'}).text
				data_captura_noticia = datetime.datetime.now()							

			except:
				print "Noticia fora do formato padrão!"

			try:
				#Escreve linha no arquivo CSV com os dados extraídos da notícia
				arquivo.writerow([titulo.encode('utf-8'), texto.encode('utf-8'), categoria.encode('utf-8'), 
					data_publicacao.encode('utf-8'), data_captura_noticia, link])
			except:
				print 'ERRO DE UNICODE'

			try:
				#Escreve noticia separada por categoria em arquivo .txt

				path = 'Categorias/'+categoria+'/' #Define caminho do arquivo .txt
				
				#Verifica se o diretório existe, se não existir cria o diretório
				if not os.path.exists(path):
					os.makedirs(path)

				#Separa data da noticia por ano, mês, dia
				dia, mes, ano = data_publicacao.split('/')
				ano, hora = ano.split(' ')

				arquivo_txt = open(path+ano+'_'+mes+'_'+dia+'_'+titulo+'_G1.txt', 'w')
				arquivo_txt.write (texto.encode('utf-8'))
			except:
				print 'ERRO DE UNICODE!'
			

	#Metodo para capturar os links das noticias
	def capturarLinks(self):

		print 'Crawleando: http://g1.globo.com/ ...'
		
		r = requests.get('http://g1.globo.com/')
		soup = BeautifulSoup (r.content) #recebe conteúdo HTML da requisição	

		paginacao = soup.find('div', attrs={'class':'load-more gui-color-primary-bg'})
		paginacao = paginacao.find('a')['href']

		#Laço para navegar na paginação do site
		while paginacao != None:

			#Laço para encontrar noticias pelo atributo class do HTML 
			for noticia in soup.findAll('div', attrs={'class':'feed-text-wrapper'}):			

				#Encontra link			
				link = noticia.find('a', attrs={'class':'feed-post-link'})['href']
				print link

				#Grava link no arquivo
				arquivo = open("links/linksG1.txt", "a")
				try:
					arquivo.write (link + '\n')
				except:
					print 'ERRO DE UNICODE'

			#Encontra link da próxima página (paginação)
			try:
				paginacao = soup.find('div', attrs={'class':'load-more gui-color-primary-bg'})
				paginacao = paginacao.find('a')['href']		
				r = requests.get('http://g1.globo.com/' + paginacao)
				soup = BeautifulSoup (r.content) #recebe conteúdo HTML da nova requisição
			except:
				print 'Captura de links concluída!'