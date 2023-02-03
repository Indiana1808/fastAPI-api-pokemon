# fastAPI-api-pokemon

Logiciel installer et outils : 

•	MySQL Workbench : pour la création de la base de données et la manipulation de données dans un premier temps.
•	MySQL Community Server : pour avoir un serveur de base de données.
•	Insomnia : pour tester les requêtes de l’API, FastAPI.
•	Python : langage de programmation pour utiliser FastAPI et aussi pour envoyer des requêtes à notre base de données.

Librairies installer : 

Ci-dessous les différentes librairies qu’il faut installer pour pouvoir coder l’API. Dans une invite de commande typer les lignes ci-dessous :
•	pip3 install fastapi   --user
•	pip3 install uvicorn --user 
•	pip3 install pydantic –user
•	pip3 install mysql-connector-python


	pip installe par défaut les packages Python dans un répertoire système (tel que /usr/local/lib/python3.4). Cela nécessite un accès root.
	C’est pour cela on utilise --user pour créer des packages d'installation pip dans le répertoire personnel à la place, ce qui ne nécessite aucun privilège spécial.
	FastAPI est une librairie avec laquelle on créer notre propre API.
	Uvicorn est un serveur Web compatible ASGI (async server gateway interface). Ça simplifie l'élément de liaison qui gère les connexions Web à partir du navigateur ou du client API, puis permet à FastAPI de répondre à la demande réelle. 
	mysql-connector-python comme le nom l’indique, on va utiliser cette librairie pour nous connecter à notre base de données.
	Pydantic est une bibliothèque utile pour l'analyse et la validation des données. Il contraint les types d'entrée au type déclaré. On va utiliser cette librairie pour créer des modèles avec pour manipuler les informations depuis les requêtes de type POST ou PUT.
Lancement de l’application : 

•	Tout d’abord on lance MySQL Workbench avec privilège administratif pour se connecter à notre base de données.
•	Dans le répertoire de notre projet, avec une invite de commande on lance uvicorn avec cette ligne, uvicorn main:app --reload. Le main c’est le nom de notre fichier python, app c’est le nom qu’on a donné à notre API et le –reload est utilisé pour relancer notre server uvicorn à chaque fois qu’il y a un changement dans notre code de python.
•	Puis on lance Insomnia pour tester les requêtes de notre API.



