# Real-Estate-ENSAE
Projet de Machine Learning sur la prédiction de biens immobiliers
Lien vers le challenge : https://challengedata.ens.fr/participants/challenges/68/

Ancien Repertoire Github : https://github.com/Stevenworick/ML_ENSAE (Problèmes de versions entre nos différents ordinateur et le serveur en ligne -Novices sur GitHub)

 **1. Sources données additionnelles :** 

RATP : https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/export/

SNCF : https://ressources.data.sncf.com/explore/dataset/referentiel-gares-voyageurs/table/?disjunctive.gare_ug_libelle&sort=gare_alias_libelle_noncontraint&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJ0cmVlbWFwIiwiZnVuYyI6IkNPVU5UIiwieUF4aXMiOiJuaXZlYXVzZXJ2aWNlX2xpYmVsbGUiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1jdXN0b20ifV0sInhBeGlzIjoiZ2FyZV9yZWdpb25zbmNmX2xpYmVsbGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwic2VyaWVzQnJlYWtkb3duIjoiIiwic2VyaWVzQnJlYWtkb3duVGltZXNjYWxlIjoiIiwiY29uZmlnIjp7ImRhdGFzZXQiOiJyZWZlcmVudGllbC1nYXJlcy12b3lhZ2V1cnMiLCJvcHRpb25zIjp7ImRpc2p1bmN0aXZlLmdhcmVfdWdfbGliZWxsZSI6dHJ1ZSwic29ydCI6ImdhcmVfYWxpYXNfbGliZWxsZV9ub25jb250cmFpbnQifX19XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZSwidGltZXNjYWxlIjoiIn0%3D&fbclid=IwAR1JsF5cZvYJ5Y4j9ngMGF9I8eQqK4doy4aHgCc4ri9Jmadc_OtwKAWCQPA&location=5,46.8977,1.85189&basemap=jawg.transports

Ecole Primaire et Secondaire (de la maternelle au lycée) : https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/table/?disjunctive.nature_uai&disjunctive.nature_uai_libe&disjunctive.code_departement&disjunctive.code_region&disjunctive.code_academie&disjunctive.secteur_prive_code_type_contrat&disjunctive.secteur_prive_libelle_type_contrat&disjunctive.code_ministere&disjunctive.libelle_ministere&fbclid=IwAR3LzC7ouWixjvfeUIOFKQgPIrkj87wgWFBT3yMN1_bnpb5nwds6VxiXf7A

Entreprises Francaises : https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/

API coordonnées : https://adresse.data.gouv.fr/api-doc/adresse

**2. Bibliographie - Documentation  :** 



**3. Cartographie des différents codes :**

- Real Estate - MLENSAE + ML : Code principale
- Coord.py : Code permettant la récupération des coordonnées des entreprises françaises à partir des adresses de la base SIRENE
- Test Para : Code permettant le calcul des distances entre les annonces et les infrastructures. Utilisation de la parallélisation 
              afin de gagner en temps de calcul
- Only ML : Notebook avec les tests ML à lancer sur l'ordinateur à distance
- Images Features : Notebook permettant l'ajout de features à partir des photos de l'annonce.

