## About

The Open Source Routing Machine is a high performance routing engine written in C++11 designed to run on OpenStreetMap data.

## Current build status

| build config | status |
|:-------------|:-------|
| Linux        | [![Build Status](https://travis-ci.org/Project-OSRM/osrm-backend.png?branch=master)](https://travis-ci.org/Project-OSRM/osrm-backend) |
| Windows      | [![Build status](https://ci.appveyor.com/api/projects/status/4iuo3s9gxprmcjjh)](https://ci.appveyor.com/project/DennisOSRM/osrm-backend) |
| Coverage     | [![codecov](https://codecov.io/gh/Project-OSRM/osrm-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/Project-OSRM/osrm-backend) |

## Building

For instructions on how to [build](https://github.com/Project-OSRM/osrm-backend/wiki/Building-OSRM) and [run OSRM](https://github.com/Project-OSRM/osrm-backend/wiki/Running-OSRM), please consult [the Wiki](https://github.com/Project-OSRM/osrm-backend/wiki).

To quickly try OSRM use our [free and daily updated online service](http://map.project-osrm.org)

## Documentation

### Full documentation

- [osrm-routed HTTP API documentation](docs/http.md)
- [libosrm API documentation](docs/libosrm.md)

### Quick start

Building OSRM assuming all dependencies are installed:

```
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
sudo cmake --build . --target install
```

Loading preparing a dataset and starting the server:

```
osrm-extract data.osm.pbf -p profiles/car.lua
osrm-contract data.osrm
osrm-routed data.osrm
```

Running a query on your local server:

```
curl http://127.0.0.1:5000/13.388860,52.517037;13.385983,52.496891?steps=true&alternatives=true
```

### Running a request against the Demo Server

First read the [API usage policy](https://github.com/Project-OSRM/osrm-backend/wiki/Api-usage-policy).

Then run simple query with instructions and alternatives on Berlin:

```
curl https://router.project-osrm.org/13.388860,52.517037;13.385983,52.496891?steps=true&alternatives=true
```

## References in publications

When using the code in a (scientific) publication, please cite

```
@inproceedings{luxen-vetter-2011,
 author = {Luxen, Dennis and Vetter, Christian},
 title = {Real-time routing with OpenStreetMap data},
 booktitle = {Proceedings of the 19th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems},
 series = {GIS '11},
 year = {2011},
 isbn = {978-1-4503-1031-4},
 location = {Chicago, Illinois},
 pages = {513--516},
 numpages = {4},
 url = {http://doi.acm.org/10.1145/2093973.2094062},
 doi = {10.1145/2093973.2094062},
 acmid = {2094062},
 publisher = {ACM},
 address = {New York, NY, USA},
}
```

## Transport en commun

Ce projet est basé sur le projet Open Source Routing Machine (OSRM) en C++ et réalisé principalement avec les données de Open Street Map (OSM) de la région Alsace et les données de la Compagnie des Transport Strasbourgeois (CTS).

### Implémentation :

Le projet OSRM est très efficace en terme de performance. Après les sites de comparaison, le temps moyen pour trouver le chemin le plus court avec OSRM est bien plus rapide que d'autres moteurs d'itinéraires comme Google, Cloudmade, MapQuest, etc...([lien](http://geotribu.net/node/520#footnote2_wm1g6rz)) Notamment grace à un nouveau mécanique d'optimisation : la Contracttion Hierarchies. Puisque l'OSRM donne autant d'avantages, mon objectif pour cette implémentation est d'apportter le moins de modifications possibles afin de conserver ces performances.

#### Extraction des données de la CTS
La récuperation des données utiles à partir des données fournies par la CTS. Ces données sont en format GTFS. Bien évidement, plusieur parser de ce type de donnée sont disponible mais malheureusement aucun n'est en C++. J'ai décidé de prendre le parser Transitfeed en Python, écrit par Google qui gère actuellement de diffuser les données du format GTFS.

Les informations récupérés à partir de ces données corrigent un gros défaut des données d'OSM. En effet, les données d'OSM nous fournissent les trajet de Bus/Tram ainsi que les arrets mais les informations fournis ne nous permettent pas de calculer la distance exactes entre 2 arrets, sans cet information, il nous est impossible de calculer le temps de parcours entre 2 arrets. Et donc avec les données de la CTS, on peut extraire cet information. 

Les informations utiles sont: les arrets de bus et tram(id, longitude, latitude), les arcs qui representent e lien entre 2 arrets successives (id source, id destination, durée entre 2 arrets).
Tout cette phase est réalisé en Python dans le script testForOsrm.py dans le dossier python.

#### Intégration des nouvelles données dans OSRM
L'intégration de ces nouvelles données sont effectuée après l'extraction des données de l'OSM pour plusieurs raisons. L'ajout d'un nouveau noeud ou d'un nouveau arc est très délicat, car OSRM demande id d'un noeud qui existe dans les données de l'OSM. On ne peut pas ajouter un noeud ou un arc de façon hasard parce que OSRM fait appel ensuite aux coordonnées (longitude, latitude) de ce noeud pour calculer la distance d'un arc.

Heuresment, comme j'ai précisé précédement, l'OSM nous fournit les arrets de Bus/Tram avec les coordonnées. J'ai donc sauvegardé les noeuds de l'OSM qui représentent les arret de Bus/Tram et ensuite comparer ces coordonnées avec les données récupérées depuis le script python. Après ce traitement, j'obtient l'id de l' OSM correspondant à chaque arret des données de la CTS.
J'ai aussi utilisé la même mécanique pour trouver le noeud le plus proche des arrets de Bus/Tram afin de relier le réseau de transport au réseau de routier.

Cette phase est réalisé dans le fichier source de OSRM extractor.cpp.

L'ajout des arcs devient plus facile, néanmoins, j'ai dû ajouter une nouvelle fonction pour ajouter des arcs qui me semble plus adapté.


### Source des données :
Données OSM : [data OSM](http://download.geofabrik.de/europe/france/alsace.html) (format osm.pbf).
Données CTS : [data CTS](http://www.gtfs-data-exchange.com/meta/9798402).

### Running :
Installer OSRM et tous les dépendants de OSRM.

Installer le parser du format GTFS : [transitfeed](https://github.com/google/transitfeed)

Les données de la CTS doivent être dans le fichier python et nommé ctsdata.zip

Nous avons utilisé du python dans le fichier extractor.ccp, vous devez donc linker avec la bibliotheque python. Dans 
```
build/CMakeFiles/EXTRACTOR.dir/build.make 
```
cherchez extractor.cpp.o et ajoutez à la fin de la commande 
```
-I votre_bibli_python 
```

Dans 
```
build/CMakeFiles/osrm-extract.dir/link.txt 
```
ajoutez à la fin
```
-framework Python 
```