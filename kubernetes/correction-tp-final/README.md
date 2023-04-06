# Comment utiliser l'Application ? 

### Dans un Docker Compose

Pour utiliser l'application dans le cadre de Docker compose, il suffit d'entrer la commande ci-dessous: 

```bash
docker compose up -d --build
```

Il est ensuite possible de tester l'application via l'utilisation d'un client REST de type **Postman** ou **Thunder Client**: 

* Pour les tâches (il faut un Bearer Token ayant pour valeur `abc`):
  * **POST /tasks**: Il est possible de poster un JSON possédant les attributs **test** et **title**, tous les deux de type **string**.
  * **GET /tasks**: On récupère ensuite les tâches
* Pour les utilisateurs:
  * **POST /signup**: Il est possible de poster un JSON ayant pour attributs **email** et **password**, tous les deux de type **string**
  * **POST /login**: Il est ensuite possible de poster le même JSON dans le but de se voir répondre un token d'authentification à condition que l'utilisateur ait été créé via l'endpoint précédent.

---

### Dans un cluster Kubernetes

A partir d'un cluster généré via minkube, dont la création provient de la ligne de commande ci-dessous: 

```bash
minikube start --driver docker
```

Il est possible d'appliquer les fichiers de ressources joint au projet dans le cluster. Tout d'abord, il nous faut appliquer l'environnement via la commande ci-dessous: 

```bash
kubectl apply -f .\ressources-files\environment.yml
```

Puis on peut appliquer le reste des fichiers de ressources via la commande ci-dessous: 

```bash
kubectl apply -f .\ressources-files\
```

