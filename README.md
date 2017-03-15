# ip150_interfacer

ip150-interfacer est un petit script python qui se connecte à votre module IP 150 afin de récupérer les informations en temps réel.

Le script intègre également un mini serveur web accessible sur le port 12345 et retournant les dernières informations récupérées.

L'IP150 n'autorisant qu'une seule connexion, il ne sera plus possible d'accéder à l'interface web de votre alarme tant que le script sera en marche.


> Liste des requêtes HTTP

/status => Retourne un JSON informant de l'état des zones. Pour connaître le mapping des zones, appelez la page /description

/description => Affiche le nom des zones correspondants aux index du JSON de /status

/arm => Arme l'alarme

/desarm => Désarme l'alarme

/partiel => Place l'alarme en mode partiel

/stop => Déconnecte le script du module IP


> Configuration

La configuration s'effectue en modifiant le fichier const.py

Variables de connexion :
- USER_CODE : Code utilisateur
- PASSWORD : Mot de passe de l'IP150
- IP_ADDR : Adresse IP de votre alarme à saisir entre guillemets (ex: "192.168.1.253")
- TCP_PORT : Port TCP configuré (11000 par défaut)

Variables du script :
- STATUS_INTERVAL : Fréquence de récupération des informations (en secondes)
- LOGIN_MAX_RETRY : Nombre d'essais maximum à effectuer en cas d'echec de connexion
- LOGIN_WAIT_TIME_START, LOGIN_WAIT_TIME_MULT : Temps d'attente entre deux tentatives de connexion
- READY_WAIT_TIME : Temps d'attente après connexion (temps de chargement de l'alarme)
- *_CODES : Mapping des codes
