# Comment utiliser l'application ?

### Dockerizer l'application

Pour Dockerizer l'application, il faut, dans un terminal ouvert à la racine du projet, exécuter les commandes ci-dessous: 

```bash
docker build -t nom-repo/nom-image:latest .
```

Pour la tester en local, on peut lancer un conteneur de l'application avec cette commande: 

```bash
docker run -d -p 3000:3000 -e STORY_FOLDER=story -v /app/story nom-repo/nom-image
```

Enfin, pour la mettre sur DockerHub, il faut, après s'être logué avec `docker login`, exécuter la commande ci-dessous: 

```bash
docker push nom-repo/nom-image
```

---

### Créer et paramétrer le cluster Kubernetes

Pour pouvoir faire tourner notre application dans le cluster, il faut déjà en avoir un. Pour créer un cluster avec minikube, on va utiliser la commande:

```bash
minikube start --driver docker
```

Puis il nous faudra appliquer nos fichiers de ressources via la commande ci-dessous: 

```bash
kubectl apply -f .\ressources-files\deployment.yml,.\ressources-files\service.yml,.\ressources-files\environment.yml
```

Enfin, pour accéder, depuis l'extérieur, au cluster local, il faut utiliser le mécanisme du tunneling de minikube, que l'on déclenche via cette commande:

```bash
minikube service exo-05-service
```

On obtient ainsi une adresse IP, que l'on peut requêter en ajoutant l'endpoint **/story** auquel on peut envoyer, via une requête **POST**, un JSON de ce type:

```json
{
  "text": "Test de requête POST"
}
```

Puis, via une requête GET au même endpoint, on va obtenir, normalement, un résultat de ce type: 

```json
{
  "story": "Test de requête POST\n"
}
```

Si c'est le cas, alors tout est bon, notre application fonctionne ! 

> Pour faire crasher notre application et tester le LoadBalancer, il est aussi possible d'envoyer une requête GET à l'endpoint **/error**.

