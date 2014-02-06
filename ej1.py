#!/usr/bin/python
# -*-coding: utf-8 -*-

import web
from web import form
from web.contrib.template import render_mako
import dbm
from mako.template import Template
import sys

#Importando librería pymongo, específicamente el objeto de conexión
import pymongo

import feedparser

import tweepy

import csv

# para sesiones
web.config.debug = False

# Mis bibliotecas de datos

biblioheader=[]

bibliocuerpo=[]  

bibliopie=[]

bibliox=[]

pagina=[]

pagina.insert(0,'No')
pagina.insert(1,'No')
pagina.insert(2,'No')
     
urls = (
    '/*', 'index',
    '/indexloge', 'indexloge',
    '/formulario', 'formulario',
    '/desconectar', 'desconectar',
    '/datos', 'datos',	
    '/datosmodifica', 'datosmodifica',
    '/datos2', 'datos2',
    '/datos3', 'datos3',
    '/xml', 'xml',
    '/mapa' , 'mapa',
    '/chartsdatos', 'chartsdatos',
    '/twitter', 'twitter',
)
app = web.application(urls, globals())
render = web.template.render('./plantillas/')

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':''})

###########mongodb#############

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 

db = conn.RegistroUsurarios

usuarios = db.usuarios

#Creando la conexión por defecto
#conexion = Connection()
 
#Definiendo la BD que vamos a usar. En caso de no existir, se crea automágicamente al insertar el primer registro
#db = conexion.bdRegistroUsuarios
 
#Se ingresa la información en estilo JSON (los mismos datos de arriba) y se guarda en una variable
#alumno1 = {"Alumno": "Mario Andrés Cares Cabezas", "Dirección": "El Canelo 2652, Iquique, Chile", "Fecha Nacimiento": "1990-05-16", "Carrera": "Ing. Informática", "Semestre Actual": 8, "Ramos": ["Adm. Recursos Humanos", "Economía", "Proyecto Final", "Aud. Computacional"]}
 
#Guardamos el alumno
#db.alumnos.save(alumno1)
 
#Leemos los alumnos ingresados
#cursor = db.alumnos.find()
#for alumno in cursor:
#print alumno


######################

formulariodatos = form.Form( 

    form.Textbox("nombre", form.notnull, form.Validator('No vacio', lambda x:x!=""),description = "Nombre:"),
    form.Textbox("apellidos", form.notnull,form.Validator('No vacio', lambda x:x!=""), description = "Apellidos:"),
    form.Textbox("correo", form.notnull,form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', "Formato incorrecto"),description = "Correo Electrónico:"),
    form.Textbox("visa", form.notnull, form.regexp('^([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})$', "Formato de tarjeta VISA no valido"),description = "Número de Visa:"),
    form.Dropdown("dia", ['1', '2', '3','4','5','6','7','8','9','10','11','12','13','14', '15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30', '31']),
    form.Dropdown("mes", ['1', '2', '3','4','5','6','7','8','9','10','11','12']),
    form.Dropdown("anho",[1980 ,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014], description="Año de nacimiento"),
    form.Textarea("direccion", form.notnull,description = "Dirección:"),
    form.Password("contra",form.notnull, form.Validator('7 caracteres', lambda x: len(x)>=7),description = "Contraseña:"),
    form.Password("verifi", form.notnull, form.Validator('No vacio', lambda x:x!=None),description = "Verificación:"),
    form.Radio("pago", ['Tarjeta de crédito', 'Contra reembolso']),
    form.Checkbox("clausulas", description = "Aceptación de Cláusulas:"),
    form.Button("boton"),
    validators = [form.Validator("No coinciden las contraseñas", lambda x: x.contra == x.verifi), form.Validator("Error fecha.", lambda x: (((int(x.mes) == 2) and ((int(x.dia) <= 28) and ((int(x.anho) % 4) != 0) or (int(x.dia) <= 29) and ((int(x.anho) % 4) == 0))) or ((int(x.dia) <= 30) and ((int(x.mes) == 4) or (int(x.mes) == 6) or (int(x.mes) == 9) or (int(x.mes) == 11)))) or (int(x.mes) == 1) or (int(x.mes) == 3) or (int(x.mes) == 5) or (int(x.mes) == 7) or (int(x.mes) == 8) or (int(x.mes) == 10) or (int(x.mes) == 12))] 
) 

	

formudatos2 = form.Form( 

    form.Textbox("nombre", form.notnull, description = "Nombre:"),
    form.Textbox("visa", form.notnull, form.regexp('^([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})$', "Formato de tarjeta VISA no valido"),description = "Número de Visa:"),
    form.Button("buscar"),
) 
		 
#####################


formcharts = form.Form( 
	form.Textbox("asig1",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "DAI:"),
	form.Textbox("asig2",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "SPSI:"),
	form.Textbox("asig3",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "IV:"),
	form.Textbox("asig4",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "TID:"),
	form.Textbox("asig5",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "SO:"),
	form.Button("boton"),
		)



######################

def modificapaginas(pagina, npagina):

	pagina[2] = pagina[1]
	pagina[1] = pagina[0]
	pagina[0] = npagina


	 # Comprueba si es un numero de tarjeta visa
def tarjetaCredito(string):
	a = re.compile(r'([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})')
	return a.match(string)

	# Comprueba si es un email
def email(string):
  	a = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
  	return a.match(string)




#########################

def contra_correcta (usuario):
        return usuario


def comprueba_identificacion ():
        usuario = session.usuario
        return usuario


class desconectar:
        def GET(self):
                usuario = session.usuario
		session.kill()
		rellenaheader(biblioheader)
		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)
		#return render.index(biblioheader, bibliocuerpo, bibliopie)     
		return web.seeother('/')  




formacceso = form.Form( 
		    form.Textbox("usuario",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "Usuario:"),
		    form.Password("contra",form.notnull, form.Validator('No vacio', lambda x:x!=None),description = "Contraseña:"),
		    form.Button("Acceso"),
		)

###############################

def rellenaheader(biblioheader):


	f=open("./static/header/titulo.txt")
	titulo = f.read()
	f.close()

	f=open("./static/header/subtitulo.txt")
	subtitulo = f.read()
	f.close()


	biblioheader.insert(0, "/static/header/logo.gif")
	biblioheader.insert(1, titulo)
	biblioheader.insert(2, subtitulo)
	biblioheader.insert(3,formacceso)
	biblioheader.insert(4,pagina)

	return

def rellenaheader2 (biblioheader):

	f=open("./static/header/titulo.txt")
	titulo = f.read()
	f.close()

	f=open("./static/header/subtitulo.txt")
	subtitulo = f.read()
	f.close()

	biblioheader.insert(0, "/static/header/logo.gif")
	biblioheader.insert(1, titulo)
	biblioheader.insert(2, subtitulo)
	
	return


def rellenacuerpo(bibliocuerpo):

	f = open("./static/cuerpo/textoinicio.txt")
	textoinicio = f.read()
	f.close()

	bibliocuerpo.insert(0, textoinicio)

	return

def rellenapie(bibliopie):

	f = open("./static/pie/pie.txt")
	textopie = f.read()
	f.close()

	bibliopie.insert(0, textopie)

	return

##### XML ####

def noticias():
	noticia1 = ""
	noticia2 = ""
	noticia3 = ""
	noticia4 = ""
	noticia5 = ""

	conte1 = ""
	conte2 = ""
	conte3 = ""
	conte4 = ""
	conte5 = ""		

	d = feedparser.parse(r'http://encultura2.com/?feed=rss2', request_headers={'Cache-control': 'max-age=600'})
	
	# Titulos
	noticia1 = d.entries[0].title
	noticia2 = d.entries[1].title
	noticia3 = d.entries[2].title
	noticia4 = d.entries[3].title
	noticia5 = d.entries[4].title

	# Contenido
	conte1= d.entries[0].summary
	conte2= d.entries[1].summary
	conte3= d.entries[2].summary
	conte4= d.entries[3].summary
	conte5= d.entries[4].summary


	#noticias[i][2] = d.entries[i].id
	
	noticias1 = [noticia1, conte1, noticia2, conte2, noticia3, conte3, noticia4, conte4, noticia5, conte5]

	return noticias1


##############




##### GOOGLE MAPS ##########

mapas = '''
<script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDVdHdp8sjYC8R5385XA1Fo5-P18vNtd2M&sensor=true">
    </script>
    <script type="text/javascript">
      function initialize() {
        var mapOptions = {
          center: new google.maps.LatLng(37.197125, -3.624440),
          zoom: 8,
	  
	mapTypeControl: true,
    mapTypeControlOptions: {
	      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
	    },
	    zoomControl: true,
	    zoomControlOptions: {
	      style: google.maps.ZoomControlStyle.SMALL
	    }
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"),
            mapOptions);
	


	    var marker = new google.maps.Marker({
	    position: map.getCenter(),
	    map: map,
	    title: 'Click to zoom'
	  });

	  google.maps.event.addListener(map, 'center_changed', function() {
	    // 3 seconds after the center of the map has changed, pan back to the
	    // marker.
	    window.setTimeout(function() {
	      map.panTo(marker.getPosition());
	    }, 3000);
	  });

	  google.maps.event.addListener(marker, 'click', function() {
	    map.setZoom(18);
	    map.setCenter(marker.getPosition());
		
	  });

	 
      }
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>'''




##############################



######TWITTER#########

def twitterfuncion():
	tt = []
	ttla = []
	ttlo = []
	# Consumer keys and access tokens, used for OAuth
	consumer_key = 'tj9PrXfT8RZJi88Jnl2GlQ'
	consumer_secret = 'i0xTR6RJbn4gT2gyIyHj4pD8Vyl1v3kKTw9kJtqXM'
	access_token = '2247760207-TBGP0aaW2tCio0ziOg7WvnIte5LOtC4ThJtLTg6'
	access_token_secret = 'mvRssKbKbO3zR16ihMUHZ2Sp6Swu2ZdLFZMDEZxbprTcw'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)
	# https://dev.twitter.com/docs/api/1.1/get/search/tweets
	#tweets = api.search(q='Granada', count=1)
	count = 0
	conta = 0
	c = 0
	#keyword = 'McDonalds '
	#result = tweepy.api.search(q=keyword,rpp=1000,page=2, geocode= "34.085422,-117.900879,100mi" )

	
    	#for tweet in result:
	#	lat, lon = tweet.geo if tweet.geo else ('', '')
	#print lat
       # w.writerow((keyword, tweet.text, lat, lon))
	#results = tweepy.api.search(q = "Linux",geocode="38.376,-0.5,8km", rpp=1000)

	#for result in results:
	#    print result.text
	#    print result.location #if hasattr(result, 'location') else "Undefined location"
	
	for tweet in tweepy.Cursor(api.search,
                           q="Granada",
                           rpp=2,
			   count=0,
                           result_type="recent",
                           include_entities=True,
                           lang="es").items():
   	 #print tweet.created_at, tweet.text
	 
	 #tt.insert(0,tweet.text)
	 #tt.insert(0,tweet.coordinates)
	 #conta = conta+1
	 #c = c + 2
	 if tweet.geo:
		conta = conta +1
		lan, lon = tweet.geo['coordinates']
		t= [lan,lon, tweet.text]
	 	print lon
		print tweet.geo
		return t
		#tt.insert(conta,tweet.text)
	 #print tweet.geo
	 if conta >= 1 :
			return t
	return 
	 



#### MAPAS PARA TWITTER ######


def creamapa(d1, d2): 
	
	return

#####################


class index:

	def GET(self):
		
		modificapaginas(pagina,"index")
		usuario = comprueba_identificacion ()
		
		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)
                salir = "si"
                if usuario:
			rellenaheader2(biblioheader)
			return render.indexloge(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
                else:
			rellenaheader(biblioheader)
			return render.index(biblioheader, bibliocuerpo, bibliopie, pagina,  usuario=usuario)       


	def POST(self): 
		modificapaginas(pagina,"index")
		usuario = comprueba_identificacion ()
		rellenaheader(biblioheader)
		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)

		form = biblioheader[3]
                if not form.validates ():
                        return render.index(biblioheader, bibliocuerpo, bibliopie, pagina) 
		i = web.input()
                usuario = i.usuario
                contra = i.contra

		#return render.index(biblioheader, bibliocuerpo, bibliopie)
                if contra == contra_correcta(usuario):
                        session.usuario = usuario
                        return render.indexloge(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
		else:

			return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)


class formulario:
	def GET(self):
		modificapaginas(pagina,"formulario")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)		


		f = open("./static/header/titulo.txt")
		titulo = f.read()
		f.close()

		f = open("./static/header/subtitulo.txt")
		subtitulo = f.read()
		f.close()

		formdatos = form.Form( 
		    form.Textbox("titulo",form.notnull, form.Validator('No vacio', lambda x:x!=None), description = "Titulo:"),
		    form.Textbox("subtitulo",form.notnull, form.Validator('No vacio', lambda x:x!=None),description = "Subtitulo:"),
		    form.Button("Cambiar"),
		) 

		formul = formdatos
		bibliocuerpo[0] = formul
		if usuario:
			return render.formulariologe(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
		else:
			return render.formulario(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)

	def POST(self): 

		modificapaginas(pagina,"formulario")
		formula = bibliocuerpo[0]
 		titulo1 = formula.d.titulo
		subtitulo1 = formula.d.subtitulo

		i = web.input()
		
		if i.usuario!= "":

			return web.seeother('/')  

		titulo1 = i.titulo
		subtitulo1 = i.subtitulo

		f=open("./static/header/titulo.txt","w")
		f.write(titulo1)
		f.close()
		f=open("./static/header/subtitulo.txt","w")
		f.write(subtitulo1)
		f.close()
	
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)
		
	
		rellenapie(bibliopie)

		bibliocuerpo[0] = formula

		if contra == contra_correcta(usuario):
                        session.usuario = usuario
                        return render.indexloge(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
		else:

			return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)


class datos:
	def GET(self):
		modificapaginas(pagina,"datos")
		usuario = comprueba_identificacion ()

		if usuario:
		        rellenaheader2(biblioheader) 
		else:
			rellenaheader(biblioheader)

		rellenapie(bibliopie)
	
		formdatos = formulariodatos()

		bibliocuerpo.insert(0,formdatos)

		return render.datos(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)

	def POST(self):

		modificapaginas(pagina,"datos")
		usuario = comprueba_identificacion ()

		if usuario:
		        rellenaheader2(biblioheader) 
		else:
			rellenaheader(biblioheader)

		rellenapie(bibliopie)
		
		form = bibliocuerpo[0]
		fallo = "no"


		
		if not form.validates():
			fallo = "si"
	
		if (fallo == "si"):
		
			bibliocuerpo.insert(0,form)
			return render.datos(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)			

		elif(fallo != "si"):

			usuario1 = {'Nombre': form.d.nombre, "Apellidos": form.d.apellidos, "Correo": form.d.correo, "Visa": form.d.visa, "Dia": form.d.dia, "Mes": form.d.mes, "Anho": form.d.anho, "Direccion": form.d.direccion, "Contra": form.d.contra, "Pago": form.d.pago}
 
			#Guardamos el usuario
			usuarios.insert(usuario1)
			
		        bibliocuerpo.insert(0,"Usuario insertado")
		 	return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)


class datosmodifica:
	def GET(self):
		modificapaginas(pagina,"datosmodifica")
		usuario = comprueba_identificacion ()

		if usuario:
			rellenaheader2(biblioheader) 
		else:
			rellenaheader(biblioheader)

		formdatos2 = formudatos2()
		#bibliocuerpo.pop()
		bibliocuerpo.insert(0,formdatos2)

		return render.datosmodifica(biblioheader, bibliocuerpo, bibliopie, bibliox, pagina, usuario=usuario)

	def POST(self):
		modificapaginas(pagina,"datosmodifica")
		usuario = comprueba_identificacion ()
		fallo = "no"
		if usuario:
		        rellenaheader2(biblioheader) 
		else:
			rellenaheader(biblioheader)

		rellenapie(bibliopie)
		
		form1 = bibliocuerpo[0]
		
		if not form1.validates():
			fallo = "si"
	
		if (fallo == "si"):
		
			bibliocuerpo.insert(0,form1)
			return render.datosmodifica(biblioheader, bibliocuerpo, bibliopie, bibliox, pagina, usuario=usuario)			

		elif(fallo != "si"):

			
			
			x = "no"
			try:
				x = bibliox.pop()
			except:
				print "Salta error"
			
			print x
			if (x == "no"): 

				print "entro"
				form = formulariodatos()

				try:
					 p_usu = usuarios.find_one({'Visa':form1.d.visa})
					 #print p_usu
					 guardar = "si"
					 form.nombre.value = p_usu['Nombre']
					 form.apellidos.value = p_usu['Apellidos']
					 form.correo.value = p_usu['Correo']
					 form.visa.value = p_usu['Visa']
					 form.dia.value = p_usu['Dia']
					 form.mes.value = p_usu['Mes']
					 form.anho.value = int(p_usu['Anho'])	 
					 form.direccion.value = p_usu['Direccion']
					 
					 bibliox.append("si")

					 bibliocuerpo.insert(0,form)
					 return render.datos2(biblioheader, bibliocuerpo, bibliopie, bibliox, pagina, usuario=usuario)

				except:
					
					#print 'valor ' + x
					bibliocuerpo.insert(0,"No existe el usuario")
					return render.indexloge(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)

			else:
				###
				usuario = comprueba_identificacion ()
				print "entra en else"
				if usuario:
					rellenaheader2(biblioheader) 
				else:
					rellenaheader(biblioheader)

				rellenapie(bibliopie)
		
				form = bibliocuerpo[0]
				fallo = "no"
		
				if not form.validates():
					fallo = "si"
	
				if (fallo == "si"):
					bibliox.append("si")
					bibliocuerpo.insert(0,form)
					return render.datosmodifica(biblioheader, bibliocuerpo, bibliopie, bibliox, pagina, usuario=usuario)		

				elif(fallo != "si"):

		 			usuarios.update({"Nombre" : form1.d.nombre},{"Nombre": form.d.nombre, "Apellidos": form.d.apellidos, "Correo": form.d.correo, "Visa": form.d.visa, "Dia": form.d.dia, "Mes": form.d.mes, "Anho": form.d.anho, "Direccion": form.d.direccion, "Contra": form.d.contra, "Pago": form.d.pago});
					

					bibliocuerpo.insert(0,"Usuario insertado")
				 	return render.indexloge(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
				###


## XML ##


class xml:
	

	def GET(self):

		modificapaginas(pagina,"noticias")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)		


	
			
		noticias1 = noticias()
		return render.xml(biblioheader, bibliocuerpo, bibliopie, pagina, noticias1, usuario=usuario)

	def POST(self): 

		

		return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
####

class mapa:
	

	def GET(self):

		modificapaginas(pagina,"noticias")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)		


	
		return render.mapa(biblioheader, bibliocuerpo, bibliopie, pagina, mapas, usuario=usuario)

	def POST(self): 

		

		return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
####


class chartsdatos:
	def GET(self):
		
		modificapaginas(pagina,"noticias")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)	
		
		#form9 = formudatos2()
		try:
			form9 = formcharts()
			bibliocuerpo.pop()
			bibliocuerpo.insert(0,form9)
			return render.chartsdatos(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
		
		except:
			print "fallo"
		
		print "entra get"
		
		
	

	def POST(self):
		
		print "entra post"
		modificapaginas(pagina,"noticias")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)	

		
		form9 = formcharts()
		datos=[]

		if not form9.validates():
			form9 = formcharts()
			bibliocuerpo.pop()
			bibliocuerpo.insert(0,form9)		
			return render.chartsdatos(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)	
		else:	
			
	
			datos.insert(0,form9.d.asig1)
			datos.insert(1,form9.d.asig2)
			datos.insert(2,form9.d.asig3)
			datos.insert(3,form9.d.asig4)
			datos.insert(4,form9.d.asig5)
			
			
			print datos[0]
			print "pasa"
						
			return render.charts(biblioheader, bibliocuerpo, bibliopie, pagina,datos, usuario=usuario)

####

class twitter:
	

	def GET(self):

		modificapaginas(pagina,"noticias")
		usuario = comprueba_identificacion ()

		if usuario:
                        rellenaheader2(biblioheader) 
                else:
			rellenaheader(biblioheader)


		rellenacuerpo(bibliocuerpo)
		rellenapie(bibliopie)		

		print "COORDENADASSSSSS"
		t = twitterfuncion()
		la = t[0]
		lo = t[1]
		tw = t[2]
		#print t[0]
		#print t[1]
	
		return render.twitter(biblioheader, bibliocuerpo, bibliopie, pagina, la, lo,tw, usuario=usuario)

	def POST(self): 

		

		return render.index(biblioheader, bibliocuerpo, bibliopie, pagina, usuario=usuario)
####

if __name__ == "__main__":
    app.run()
