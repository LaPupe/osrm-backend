#!/usr/bin/python2.5

import transitfeed
import sys



def stop_list():

	feed_name = "../../../gtfs_parser/google_transit/data.zip"
	feed_name = feed_name.strip()

	loader = transitfeed.Loader(feed_name)
	data = loader.Load()

	#indice pour la liste des stops
	nbStops = 0
	pre_stop = 0

	#La liste retournee qui contient  2 listes : stops et edges
	list_gtfs = []
	edge_list = []
	#list stops contient des listes de stops de chaque route
	#note : une route = un trajet de bus/tram
	stop_list = []

	#list intermediaire
	stop_list_id = []

	#parcourir chaque route = trajet de bus/tram
	for route in data.GetRouteList():
		#contient les stops de chaque route
		stop_each_route = []

		#first trip
		trip = route._trips[0]

		i = 0
		for stop_time in trip.GetStopTimes():
			#print stop_time.stop_id + " : " + str(stop_time.departure_secs)

			#liste intermediaire permet de savoir si le stop a deja ete ajoute
			if any(stop_time.stop_id in id for id in stop_list_id) == False:
				#Recuperer les informations dun arret (longitude, latitude)
				stop = data.GetStop(stop_time.stop_id)
				#ajouter les informations du stop dans la liste
				stop_each_route.append([stop.stop_id, stop.stop_lat, stop.stop_lon])
				
			#Si il y a plus que 2 arrets dans la liste
			if i > 0:
				#calculer le temps entre 2 stops
				# TODO : le temps entre 2 stops peut parfois etre nul(0), peut-on accepte ce comportement ??
				duration = (stop_time.departure_secs - pre_stop)
				#print duration

				#Construire un nom pour l'arc
				nameArc = "TRANSPUB " + route.route_id + " " + stop_list_id[nbStops+i-1] + " <---> " + stop_time.stop_id

				#ajouter 1 arc
				edge_list.append([stop_list_id[nbStops+i-1], stop_time.stop_id, duration, nameArc])

			#ajouter le stop dans la liste intermediaire
			stop_list_id.append(stop_time.stop_id)

			#stocker l'horaires du stop precedent
			pre_stop = stop_time.departure_secs

			#incremente i pour la taille de la liste stop_each_route, on peut aussi utiliser len(stop_each_route) 
			i += 1
		#ajouter i au nombre total de stops
		nbStops += i
		
		
		stop_list.append(stop_each_route)

		# for edge in edge_list:
		# 	print edge[0] + "  ---->  " + edge[1] 

	list_gtfs.append(stop_list)
	list_gtfs.append(edge_list)

	return list_gtfs


if __name__ == '__main__':
    stop_list()