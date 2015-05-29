# -*- coding:utf-8 -*- # Permet d'utiliser les caractères français.

#Import des modules nécessaires
from xml.dom.minidom import parse
import urllib, string, os, codecs


#Fonction pour ouvrir et lire le fichier XML.
def xmldescription(url):
    xmlfilename =urllib.urlopen(url) #Ouverture du fichier via le web.
    dom= parse(xmlfilename) #Lecture du fichier
    Description = dom.getElementsByTagName('summary') #Recherche l'élément 'summary'

    nbSummary = len(Description) #Nombre de summary
    condition = False
    NoSummary = 1
    while condition == False:
        if string.count(Description[NoSummary].firstChild.nodeValue ,u"Température:"):
            TxtNodeValue = Description[NoSummary].firstChild.nodeValue #Retourne le X ieme enfant du noeud soit le sommaire HTML
            condition = True
        NoSummary = NoSummary + 1
        if NoSummary == nbSummary:
            TxtNodeValue = "nil"
            condition = True

    # Traitement du noeud XML
    ListeB = string.split(TxtNodeValue, "<b>") # Division des informations du noeud à '<b>' retourne un liste de plusieurs éléments.

    if len(ListeB) > 1: # S'il y a de l'information dans la variable
            for elements in ListeB: # Pour chaque élément de la liste.
                if string.count(elements, "Temp") > 0: # S'il y a le texte 'TEMP' dans l'élément regardé.
                        TextTemp = string.split(elements, "</b>")[1] # Division pour extraire la température
                        NombreTemp = string.replace(TextTemp, "&deg;C <br/>", "") # Efface par remplacement les éléments indésirables
    else:
            NombreTemp = "-9999" # Si aucune température, mettre la valeur -9999.

    return string.strip(string.replace(NombreTemp, ",", ".")) # Retour de la valeur avec remplacement des , par des .

#Écriture dans un fichier
try:
	fichier = codecs.open(os.path.join(os.getcwd(), "Temperature.txt"),'w', encoding='utf-8')
	fichier.write( u"Température: " +  xmldescription("http://meteo.gc.ca/rss/city/qc-133_f.xml") + " Celcius")
	fichier.close()
except:
	fichier.close()



