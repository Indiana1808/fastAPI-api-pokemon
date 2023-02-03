from fastapi import FastAPI
from mysql.connector import Error
import mysql.connector
import json
import re  # c'est une librairie
from pydantic import BaseModel

# Ici, la variable app sera une instance de la classe FastAPI. Ce sera le principal point d'interaction pour créer notre API.
app = FastAPI()


#  Le @app.get("/") indique à FastAPI que la fonction juste en dessous est chargée de gérer les requêtes qui vont au chemin(ici pokemons)/en utilisant une opération get.
#  Il s'agit d'un décorateur lié à une opération de chemin ou d'un décorateur d'opération de chemin.
@app.get("/pokemons")
def recupererToutPokemon():
    # Nous utilisons un try catch pour empêcher l'API de planter s'il y a des erreurs de connexion à la base de données
    try:
        # la fonction mysql.connector.connect établit une connexion, établissant une session avec le serveur MySQL.On passe en argument dans la fonction,
        # l'hôte qui est l'adresse IP du serveur de base de données, le nom de la base de données, l'utilisateur et le mot de passe de l'utilisateur
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():  # la fonction is_connected() vérifie si le code a une connexion établie avec le serveur, si oui, elle renvoie true sinon false

            # la fonction curseur() renvoie la valeur sous forme d'objets.
            cursor = connection.cursor(dictionary=True)
            # On passe le dictionary=True pour qu'il renvoie des lignes sous forme de dictionnaires.
            # Les dictionnaires sont utilisés pour stocker des valeurs de données dans des paires clé:valeur. Example "nom_pokemon" : "Pikachu"
            # La variable query stocke la requête MySQL que nous utiliserons pour manipuler les données de la base de données
            query = ("SELECT id_pokemon, nom_pokemon FROM pokemon")
            # la fonction execute() est utilisée pour exécuter la requête stocker dans la variable query
            cursor.execute(query)
            # la fonction fetchall() récupère toutes les lignes (ou toutes les lignes restantes) d'un ensemble de résultats de requête
            result = cursor.fetchall()
            # et renvoie une liste. Si plus aucune ligne n'est disponible, elle renvoie une liste vide.
            cursor.close()  # la fonction close() désactive le cursor qu'on utilise sur la base de données pour exécuter votre requête
            connection.close()  # ici la fonction close() coup la connexion avec la base de données
            # on utilise la fonction json.dumps() pour convertir les données reçues de la base de données en chaîne de caractères
            result = json.dumps(result)
    except Error as e:  # nous utilisons la classe Error de la librairie mysql.connector pour intercepter toutes les exceptions reçues de la connexion avec la base de donnéees
        # MySQL et pour afficher l'erreur dans un try catch
        print("Error while connecting to MySQL", e)
    finally:  # Le but de l'instruction finally dans la gestion des erreurs est de s'assurer qu'un morceau de code de nettoyage est exécuté, dans notre cas,
        # nous nous assurons que toutes les connexions à la base de données sont fermées
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    # json.loads() prend une chaîne de caractères et renvoie un objet json.
    return json.loads(result)


# ici le {id} est un paramètre pour stocker une information
@app.get("/pokemons/id/{id}")
def recupererPokemonParId(id: str):

    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # La requête ci-dessous récupère les informations demandées dans les 3 tables pour un pokémon spécifié par son identifiant
            query = ("SELECT pokemon.id_pokemon, pokemon.num_pokedex, pokemon.nom_pokemon, pokemon.taille, pokemon.poids, pokemon.stat_base, pokemon.image, type.type_pokemon, type.types_fort_contre, type.types_faibles_contre, competence.competence,competence.description, competence.puissance, competence.precisions, competence.pp_max, competence.type FROM pokemon INNER JOIN type ON pokemon.type_id_type=type.id_type AND pokemon.id_pokemon=" +
                     id + " INNER JOIN competence ON pokemon.competence_Id_competence=competence.Id_competence AND pokemon.id_pokemon=" + id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/pokemons/name/{nom}")
def recupererPokemonParNom(nom: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # La requête ci-dessous récupère les informations demandées dans les 3 tables pour un pokémon spécifié par son nom
            query = ("SELECT pokemon.id_pokemon, pokemon.num_pokedex, pokemon.nom_pokemon, pokemon.taille, pokemon.poids, pokemon.stat_base, pokemon.image, type.type_pokemon, type.types_fort_contre, type.types_faibles_contre, competence.competence,competence.description, competence.puissance, competence.precisions, competence.pp_max, competence.type FROM pokemon INNER JOIN type ON pokemon.type_id_type=type.id_type AND pokemon.nom_pokemon='" +
                     nom + "' INNER JOIN competence ON pokemon.competence_Id_competence=competence.Id_competence AND pokemon.nom_pokemon='" + nom + "'")
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/types/id/{id}")
def recupererDetailDetypeParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête récupère les détails du type précisé par un identifiant
            query = ("select * from type where id_type =" + id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/abilities")
def recupererLesCompetences():
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            query = (
                "select distinct (competence), description, puissance, precisions, pp_max, type from competence")  # Cette requête récupère la liste de toutes les compétences.
            # Nous utilisons distinct pour supprimer les données en double de la requête.
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/abilities/{id}")
def recupererLesCompetenceParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête récupère les détails de la compétence précisée par un identifiant
            query = (
                "select Id_competence, competence, description, puissance, precisions, pp_max, type from competence where Id_competence = " + id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/pokemons/id/types/{id}")
def recupererLesCompetenceParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # dans cette fonction on veut récuperer le ou les types du pokémon précisé par un identifiant. Mais comme nous stockons des données sur plusieurs tables,
            # nous devons d'abord récupérer les données de clé étrangère de la table pokemon pour récupérer les informations souhaitées dans l'autre tables.
            query = (
                "select type_id_type from pokemon where id_pokemon =" + id)
            cursor.execute(query)
            result = cursor.fetchall()
            result = json.dumps(result)
            # Étant donné que les données que nous avons reçues de la base de données sont sous la forme de dictionnaires
            id = re.findall(r'\d+', result)
            # (clé : valeur, exemple "pokemon" : "Ronflex"), nous utilisons cette petite fonction avec une regex pour trouver uniquement les identifiants de la table et
            # les stocker dans un tableau

            query = (
                "select type_pokemon from type where id_type = '" + id[0] + "'")  # Cette requête récupère finalement récupère le ou les types du pokémon précisé par un identifiant
            cursor.execute(query)
            result = cursor.fetchall()
            result = json.dumps(result)
            cursor.close()
            connection.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.get("/pokemons/id/abilities/{id}")
def recupererCompetenceApprenablesParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête récupère les compétences apprenables du pokémon précisé par un identifiant
            query = (
                "select competence from competence where Id_competence in (select competence_Id_competence from pokemon where id_pokemon = " + id + ")")
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            result = json.dumps(result)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)

# Pour une requête de type POST, nous devons créer un modèle où nous stockerons les données récupérées de la requête post. Le modèle ci-dessous est utilisé pour stocker
# toutes les informations récupérées,le type de pokemon, les type de pokemon qu'il est fort contre et les type de pokemon qu'il est faible contre


class typeModel(BaseModel):
    type_pokemon: str
    type_fort_contre: str
    type_faibres_contre: str


@app.post("/type/")
# Pour la requête POST, nous utilisons la fonction asynchrone, car à un moment donné de la requête, l'API devra attendre une réponse
async def ajouterType(type: typeModel):
    # qui est principalement une manipulation de données dans la base de données, puis attend une réponse de la base de données pour savoir si la requête a réussi ou non.
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            query = (
                "select id_type from type order by id_type desc limit 1")  # Ici on récupère le dernier id stocké dans la base de données afin que le prochain typem n'ait pas d'id existant
            cursor.execute(query)
            result = cursor.fetchall()
            result = json.dumps(result)
            id = re.findall(r'\d+', result)
            # Ici, nous en ajoutons un au dernier identifiant stocké dans la base de données
            id = eval(id[0]) + 1
            # Les %s sont appelés espaces réservés et peuvent être compris comme des modèles de « recherche et remplacement » prédéfinis.
            #  C'est-à-dire que lorsque la requête s'exécutera, les %s seront remplacés par des données réelles
            query = ("insert into type values (%s, %s, %s, %s)")
            # La variable args stocke les données qui remplaceront chaque %s dans l'ordre
            args = (id, type.type_pokemon, type.type_fort_contre,
                    type.type_faibres_contre)  # Cette requête ajoute un nouveau type
            result = cursor.execute(query, args)
            connection.commit()  # La fonction commit() signifie que les modifications apportées à la transaction en cours sont rendues permanentes et que toutes les nouvelles
            # requêtes verront les nouvelles informations stockées, supprimées ou modifiées
            result = json.dumps(result)
            if(result == 'null'):  # Lors de mes tests, j'ai découvert que lorsque la requête s'est exécutée avec succès, elle renvoie une valeur nulle. Ainsi,
                # au lieu d'afficher null, je l'ai remplacé par Commande réussie
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


class competenceModel(BaseModel):
    competence: str
    description: str
    puissance: str
    precision: str
    pp_max: str
    type: str


@app.post("/abilities/")
async def ajouterCompetence(competence: competenceModel):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # La table compétence est liée au table type par la clé étrangère type_id_type. Nous récupérons à la fois les derniers type_id_type et Id_competence utilisés
            # pour les incrémenter de un afin d'éviter la duplication des clés pour que la dernière ligne de compétence soit liée à la dernière ligne de type
            query = (
                "select Id_competence, type_id_type from competence order by Id_competence desc limit 1")
            cursor.execute(query)
            result = cursor.fetchall()
            result = json.dumps(result)
            id = re.findall(r'\d+', result)
            # id[0] c'est la valeur de Id_competence
            id_competence = eval(id[0]) + 1
            id_type = eval(id[1]) + 1  # id[1] c'est la valeur de type_id_type

            query = (
                "insert into competence values (%s, %s, %s, %s, %s, %s, %s, %s)")  # Cette requête ajoute un nouveau compétences
            args = (id_competence, competence.competence, competence.description,
                    competence.precision, competence.puissance, competence.pp_max, competence.type, id_type)
            result = cursor.execute(query, args)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


class pokemonModel(BaseModel):
    num_pokedex: int
    nom_pokemon: str
    taille: float
    poids: float
    state_base: int
    image: str


@app.post("/pokemons/")
async def ajouterPokemon(pokemon: pokemonModel):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Le pokémon de table est lié aux deux autres compétences et types de table. On récupère donc tous les identifiants pour les incrémenter de un. Ce faisant,
            # la dernière ligne de pokemon est liée à la dernière ligne de compétence et de type. Plus tard, nous pouvons récupérer toutes les informations du pokemon
            # nouvellement stocké et son type et ses capacités.
            query = (
                "select id_pokemon, competence_Id_competence, type_id_type from pokemon order by id_pokemon desc limit 1")
            cursor.execute(query)
            result = cursor.fetchall()
            result = json.dumps(result)
            id = re.findall(r'\d+', result)
            id_pokemon = eval(id[0]) + 1  # id[0] c'est la valeur de id_pokemon
            # id[1] c'est la valeur de competence_Id_competence
            id_competence = eval(id[1]) + 1
            id_type = eval(id[2]) + 1  # id[2] c'est la valeur de type_id_type

            query = (
                "insert into pokemon values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")  # Cette requête ajoute un nouveau pokémon
            args = (id_pokemon, pokemon.num_pokedex, pokemon.nom_pokemon, pokemon.taille,
                    pokemon.poids, pokemon.state_base, pokemon.image, id_competence, id_type)
            print(args)
            result = cursor.execute(query, args)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.delete("/pokemons/{id}")
def effacerPokemonParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête supprime un pokémon précisé par un identifiant
            query = ("delete from pokemon where id_pokemon = " + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.delete("/abilities/{id}")
def effacerCompetenceParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête supprime une competence précisé par un identifiant
            query = ("delete from competence where id_competence = " + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.delete("/type/{id}")
def effacerTypeParId(id: str):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête supprime un type précisé par un identifiant
            query = ("delete from type where id_type = " + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.put("/pokemons/{id}")
# Comme la requête POST, la requête PUT a également besoin d'un modèle pour stocker les informations reçues de la requête.
def miseAJourPokemon(id: str, pokemon: pokemonModel):
    # Nous avons donc utilisé le modèle déjà déclaré pour stocker de nouvelles informations qui doivent être mises à jour dans la base de données
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête met à jour les informations d'un pokémon stockées dans la base de données à l'aide d'un identifiant. La fonction str() convertit les données entre
            # parenthèses en chaîne de caractères
            query = ("update pokemon set num_pokedex = " + str(pokemon.num_pokedex) + ", nom_pokemon ='" + pokemon.nom_pokemon + "', taille=" +
                     str(pokemon.taille) + ",poids=" + str(pokemon.poids) + ",stat_base=" + str(pokemon.state_base) + ", image='" + pokemon.image + "' where id_pokemon=" + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.put("/abilities/{id}")
def miseAJourCompetence(id: str, competence: competenceModel):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête modifie la compétence précisée par un identifiant
            query = ("update competence set competence ='" + competence.competence + "', description='" + competence.description + "', puissance='" + competence.puissance +
                     "', precisions='" + competence.precision + "', pp_max='" + competence.pp_max + "', type='" + competence.type + "' where Id_competence= " + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)


@app.put("/type/{id}")
def miseAJourType(id: str, type: typeModel):
    try:
        connection = mysql.connector.connect(
            host='localhost', database='pokemon', user='root', password='root')
        if connection.is_connected():

            cursor = connection.cursor(dictionary=True)
            # Cette requête modifie le type précisée par un identifiant
            query = ("update type set type_pokemon ='" + type.type_pokemon + "', types_fort_contre='" +
                     type.type_fort_contre + "', types_faibles_contre='" + type.type_faibres_contre + "' where id_type=" + id)
            result = cursor.execute(query)
            connection.commit()
            result = json.dumps(result)
            if(result == 'null'):
                result = "Commande réussie"
                result = json.dumps(result)
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return json.loads(result)
