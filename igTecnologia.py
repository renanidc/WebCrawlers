# -*- coding: utf-8 -*-

from multiprocessing import Lock, Process, Queue, current_process
import requests
from bs4 import BeautifulSoup
import datetime
import json
import csv
import os

#Metodo para extrair dados da noticia e salvar em CSV
def salvarNoticias(url):

	#Atributos da notícia
	noticia_html=""	
	titulo = ""
	texto = ""
	categoria = ""
	data_publicacao = ""		

	#Define objeto writer para gravar no arquivo CSV
	arquivo = csv.writer (open("CSV/igTecnologia.csv", "a"), delimiter="|")

	#Tenta acessar link da noticia
	try:
		#Acessa link da noticia (requisição)
		r = requests.get(url, timeout = 5.000)

		#Recebe conteúdo HTML da noticia
		noticia_html = BeautifulSoup (r.content)
	except:
		print 'ERRO DE CONEXÃO!'

	#Extrai dados do HTML
	try:
		titulo = noticia_html.find('h1', attrs={'id':'noticia-titulo-h1'}).text
		
		#Imprime titulo da noticia no terminal
		print titulo.encode('utf-8')
		
		texto = noticia_html.find('div', attrs={'id':'noticia'})
		data_publicacao = noticia_html.find('time', attrs={'itemprop':'datePublished'}).text
		categoria = 'Tecnologia'				
		data_captura_noticia = datetime.datetime.now()	

		#Remover tags script do HTML
		for script in texto(["script"]):
			script.extract()

		texto = texto.text #Recebe texto puro, sem tags HTML						

	except:
		print "Noticia fora do formato padrão!"

	try:
		#Escreve linha no arquivo CSV com os dados extraídos da notícia
		arquivo.writerow([titulo.encode('utf-8'), texto.encode('utf-8'), categoria, 
			data_publicacao, data_captura_noticia, url])
	except:
		print 'ERRO DE UNICODE!'

	try:
		#Escreve noticia separada por categoria em arquivo .txt

		path = 'Categorias/'+categoria+'/' #Define caminho do arquivo .txt
		
		#Verifica se o diretório existe, se não existir cria o diretório
		if not os.path.exists(path):
			os.makedirs(path)

		#Extrai data ordenada da noticia	
		dia, mes, ano = data_publicacao.split('/') #Separa dia, mês, ano da data de publicação
		ano, hora = ano.split(' ') #Separa ano e hora de publicação

		arquivo_txt = open(path+ano+'_'+mes+'_'+dia+'_'+titulo+'_ig_Tecnologia.txt', 'w')
		arquivo_txt.write (texto.encode('utf-8'))
	except:
		print 'ERRO DE UNICODE!'

#Metodo para capturar os links das noticias (JSON)
def capturarLinks(self):
	
	i = 0 #Contador de paginação

	#Faz requisição (GET)
	r = requests.get('http://tecnologia.ig.com.br/_indice/noticias/select?start='+str(i)+'&size=10&site=tecnologia&wt=json')

	while i<9274:

		try:	   		
	   		#recebe reponse em JSON
	   		request_json = json.loads(r.content)
	   		response = request_json['response']
	   		docs = response ['docs']

	   		#Abre aquivo em modo append (adiciona informações ao final do arquivo)
	   		arquivo_links = open ('links/links_IG_tecnologia.txt', 'a')
	   		
	   		#Extrair URLS (10 noticias por página)
	   		for x in range(0, 9): 
	   			url = docs [x]
	   			url = url ['url']
	   			print url

	   			#Escreve links no arquivo
	   			arquivo_links.write(str(url) + '\n')			
		except:
			print "ERRO DE CONEXÃO"

		#Incrementa contador de paginação (Número máximo 9273)
		if (i >= 9270):
			i = i+ 1
		else:
			i = i + 10

		#Faz requisição (GET)
		r = requests.get('http://tecnologia.ig.com.br/_indice/noticias/select?start='+str(i)+'&size=10&site=tecnologia&wt=json')


def worker(work_queue, done_queue):
    try:
        for url in iter(work_queue.get, 'STOP'):
        	status_code = salvarNoticias(url)
        	done_queue.put("%s - %s got %s." % (current_process().name, url, status_code))
    except Exception, e:
        done_queue.put("%s failed on %s with: %s" % (current_process().name, url, e.message))
    return True

def main():
    #Abre arquivo de links
	arquivoLinks = open ('links/links_IG_tecnologia.txt', 'r')
	links = arquivoLinks.readlines()

	workers = 15
	work_queue = Queue()
	done_queue = Queue()
	processes = []

	#Coloca url na fila
	for url in links:
		work_queue.put(url)

	for w in xrange(workers):
		p = Process(target=worker, args=(work_queue, done_queue))
		p.start()
		processes.append(p)
		work_queue.put('STOP')

	for p in processes:
		p.join()
		done_queue.put('STOP')

main()