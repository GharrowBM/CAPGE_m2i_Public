# Bases de Kubernetes

### Les objets Kubernetes

Dans l'univers de Kubernetes, les éléments auprès desquels nous allons travailler et que nous manipulerons auront pour dénomination des objets. Ces objets peuvent être de plusieurs type:

* **Pods**: Un pod est une unité de fonctionnement. Il contient en général un (ou plusieurs) conteneur ainsi que ses volumes dans le cas où ce dernier demandent l'utilisation de volumes. Chaque conteneur au sein du même pod peuvent communiquer entre eux de par leur partage de `localhost`. Les pods sont des petites unités éphémères, et Kubernetes va se chercher de stopper / créer / relancer des pods en cas de besoin. La gestion des pods passe en général par l'utilisatio d'un déploiement. 
* **Deployment**: Un déploiement concerne la création de conteneurs sur un ou plusieurs pods, et permet le lancement des conteneurs dans une ou plusieurs nodes, qui seront assignées par le scheduler d'une node maîtresse. L'objet de déploiement cherche simplement à faire atteindre à notre cluster un état en particulier, et opérera les modifications nécessaire au passage de l'état actuel vers celui désiré. Les déploiements peuvent être mit en pause, supprimé, etc... et permettent la scalabilité de notre cluster. Via nos déploiement, nous gérons les pods. Il n'est donc pas nécessaire de gérer manuellement les pods des worker nodes.
* **Service**: Un service sert à regrouper et à gérer l'IP privée d'un ou de plusieurs pods dans le but d'idéalement y accéder en dehors du cluster. Par défaut, les pods auront une adresse IP qu'il est difficile de connaître, mais il est possible, via un service, de regrouper un ou plusieurs pods derrière une adresse IP, ce dans le but de les exposer à d'autres pods ou de les rendre accessible à l'extérieur du cluster. Sans service, la communication vers et depuis les pods est difficile à mettre en place. 
* **Volume**: Un volume est un espace dédié au stockage des données de nos applications
* ...

Dans l'utilisation de Kubernetes, il existe deux méthodes principale de lancement et de manipulation des objets. La première, dite **impérative**, correspond au lancement des différents objets et leur manipulation par des lignes de commande. De la sorte, nous avons à peu près le même fonctionnement que lorsque l'on utilisait les commandes Docker classique. L'autre méthode est dite la méthode **déclarative**, et concerne l'utilisation de fichiers de configuration contenant les différents objets, cette méthode s'apparente à l'utilisation de Docker Compose et permet d'appliquer, d'éditer ou de supprimer des éléments Kubernetes en une ligne de commande. 


---

### L'approche impérative

Lorsque l'on utilise l'approche impérative, il va nous falloir utiliser beaucoup de lignes de commandes. Ces lignes de commandes permettent de mettre en place nos objets, de les éditer et si l'on le veut de les détruire. Pour pouvoir entrer des commandes, il nous faut nous assurer que l'interface en lignes de commande de Kubernetes est installée sur notre machine (`kubectl version --client --output=yaml`).

Prennons l'exemple d'un déploiement d'une application simple. Notre application a, dans un premier temps, besoin d'être dockerizée pour être disponible dans Kubernetes (rappelons le, Kubernetes n'a pas pour objectif de remplacer Docker mais d'étendre ses capacités). Une fois notre application dockerizée, son placement et fonctionnement au sein d'un cluster passera par la création d'un pod qui se chargera de lancer le ou les conteneurs de notre application. Ce pod devra être situé dans une node de travail, et l'ensemble de ce processus sera rendu possible via la création d'un déploiement. 

Pour créer un déploiement, il n'y a rien de plus simple, il suffit d'utiliser la commande `kubectl create deployment nom-deploiement` en usant de l'option `--image` de sorte à indiquer quelle est l'image docker dont notre cluster a besoin:

```bash
kubectl create deployment dep-001 --image=mon-repo/mon-image
```

On observe ici également qu'il nous faut avoir recourt à l'utilisation d'un lien d'image sous la forme d'un repository distant. En effet, le cluster n'a pas pour objectif d'être sur notre machine, et il est naturel que ce dernier ne s'amuse donc pas à tranférer nos images automatiquement depuis notre stockage local vers le cluster. Pour ce faire, il va `docker pull`, et il lui faut donc le nom d'une image disponible, par exemple sur Dockerhub. La syntaxe est donc celle observée plus haut.

Dans le cas où l'on travaille avec `minikube`, il est possible de bénéficier d'une interface graphique (application web) dans le but d'observe l'état de notre cluster. Pour en bénéficier, il suffit d'entrer la ligne de commande ci-dessous dans notre terminal:

```bash
minikube dashboard
```

> Il est également possible d'avoir cette interface lorsque l'on utilise `kind`, mais pour ce faire, il nous faut dans un premier temps la configurer.

Une fois notre déploiement réaliser, il peut être intéressant de le rendre accessible à l'extérieur du cluster. Pour cela, il va nous falloir réaliser un service. Les services ont pour objectif d'aider à fixer et à atteindre les adresses IP de nos pods dans le but de permettre la communication intra-cluster mais également vers ou depuis l'extérieur.

Il existe plusieurs types principaux de services, chacun ayant ses avantages et ses inconvénients: 

* **ClusterIP**: Le déploiement va se voir affecté une (ou plusieurs si plusieurs pods) adresse IP qui ne sera accessible qu'au sein du Cluster. Via ce service, il est plus aisé de créer de la communication intra-cluster entre nos pods.
* **NodePort**: Le déploiement va s'adapter pour exposer à l'extérieur du cluster l'IP de la node de travail sur laquelle tourne le pod. Via ce service il est possible de communiquer en dehors du cluster, par exemple pour créer des sites webs.
* **LoadBalancer**: Le déploiement va s'adapter pour créer une IP extérieure au cluster qui sera ciblable par de potentiels clients, cette IP va de son côté automatiquement cibler un node / pod disponible, et va attaquer un autre node / pod concerné par le même déploiement en cas de surcharge. De la sorte, on peut créer des applications gérant de multiples requêtes sans surcharger une machine en particulier.

```bash
kubectl expose deployment-name --port number --type service-type
```

Dans le cas de l'utilisation de `LoadBalancer`, l'IP externe ne sera disponible de base que si l'on lance ce service dans un environnement cloud capable de gérer ce type de services. Dans le cas contraire, par exemple pour notre cluster local, il va nous falloir quelques étapes en plus pour donner une IP à notre service, qui restera `<pending>` en attendant. 

Pour minikube, ce n'est pas très compliqué, il va nous falloir utiliser `minikube service nom-service` pour exposer à l'extérieur du cluster notre **LoadBalancer**. Dans le cas de kind, il est possible de suivre un tutoriel (disponible [ici](https://kind.sigs.k8s.io/docs/user/loadbalancer/)) mais il est important de savoir que l'IP ne sera attaquable en dehors du cluster qu'en cas d'utilisation d'un environnement **Linux** et d'utilisation de **Docker Engine**.

Une fois notre service créé, il peut être intéressant, dans le cas d'un LoadBalancer, d'augmenter le nombre de conteneurs pour notre application, vu que l'IP rendue disponible par le load balancer sera dynamiquement transformée en l'IP d'un pod disponible. 

Pour augmenter le nombre de pods, on peut utiliser l'édition de notre déploiement, via la commande `kubectl scale nom-deploiement`. Dans le but d'augmenter le nombre de pods, il va falloir changer le nombre de `replicas`. Pour cela, l'option `--replicas number` va rendre cela assez aisé.

```bash
kubectl scale nom-dep --replicas 5
```

Si l'on souhaite modifier l'image Docker d'un déploiement, il est possible de modifier nos objets kubernetes via la commande `kubectl set`. Dans notre cas, on va avoir une syntaxe de la sorte:

```bash
kubectl set image deployment/deployment-name old-image-name=new-image-name:different-tag
```

Le pull d'une image Docker ne se fera cependant pas sans avoir un tag différent, il est donc important de faire attention à changer le tag de notre image dans le but de pouvoir changer notre déploiement.

Pour observer le status d'un déploiement, on peut utiliser la commande:

```bash
kubectl rollout status deployment/dep-name
```

En cas d'erreur ou si l'on souhaite revenir à l'ancienne version de notre déploiement, il est possible d'effectuer un rollback via la commande:

```bash
kubectl rollout undo deployment/dep-name

# Pour spécifier une version en particulier, on peut utiliser:
kubectl rollout undo deployment/dep-name --to-revision revision-number
```

On peut également consulter l'historique de nos changements via la commande:

```bash
kubectl rollout history deployment/dep-name
```

---

### L'approche déclarative

Jusqu'à maintenant, nous avions eu recourt à l'approche impérative pour travailler dans Kubernetes. Cette approche permet de réaliser l'essentiel des fonctionnalités de Kubernetes, mais elle possède un désavantage de taille: Il nous faut, tout comme c'est le cas de docker sans l'utilisation de Docker Compose, connaître par coeur toutes les commandes et toutes les options dont nous avons besoin, en plus de les utiliser dans le bon ordre. Si l'on le veut, il est possible, encore une fois, de créer un fichier texte contenant toutes nos commandes et de copier coller une à une chacune d'entre elle dans le but de les exécuter. 

Ce processus est cependant lent et fastidieux, et quitte à créer un fichier, il serait de bon ton de créer un fichier plus adapté à notre objectif. C'est pour cela que l'approche déclarative existe. Grâce à elle, il va être possible de stocker un ou plusieurs fichiers décrivant les objectifs (les objets et leurs propriétés que l'on veut voir présent) et via une commande, il sera possible d'appliquer ou de retirer telle ou telle configuration.

Pour exécuter un fichier de configuration, tout ce que nous avons à faire est d'utiliser la commande `kubectl apply -f chemin/vers/fichier.yml` pour appliquer l'état demandé et `kubectl delete -f chemin/vers/fichier.yml` pour retirer les objets Kubernetes spécifiés dans le **fichier de ressources**.

Un fichier de ressource va pouvoir prendre plusieurs formes et pourrait posséder les attributs suivants:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-name
spec:
  replicas: 5
  selector:
    matchLabels:
      app: app-name
  template:
    metadata:
      labels:
        app: app-name
    spec:
      containers:
      - name: container-name
        image: repository/image-name
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 80
```

La plupart du temps, il est également nécessaire d'ajouter des labels et des sélecteurs dans nos fichiers. Dans le cadre d'un déploiement, il va falloir que Kubernetes puisse connaître quels pods sont concernés par notre déploiement. Pour ce faire, il est possible d'observer les labels ou des expression. 

Pour faire simple, il est possible d'utiliser des labels qui ne sont au final que des ensemble de clés et de valeurs qui doivent correspondre entre le sélecteur et les labels possédés par les objets Kubernetes (pour un service, le sélecteur est automatiquement via l'utilisation de labels).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-name
spec:
  selector:
    app: app-name
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

Dans le cas d'un besoin de modification, il nous suffira de changer les informations dans le fichier de ressources et de l'appliquer à nouveau. Du moment que le nom de notre objet est le même, il s'agira d'une édition. De plus, il faut savoir qu'il est possible de fusionner plusieurs ressources en un seul fichier. Dans le YAML, il est possible de séparer des sections via `---`:

```yaml
# Fichier A

---

# Fichier B
```

---

### La sélection par expression

Suite à l'évolution de Kubernetes, il est arrivé la possibilité de sélectionner via des expressions, qui se retrouvent définies par des accolades dans lesquelles ont peut définir plus de détails, par exemple sélectionner plusieurs valeurs possibles pour une clé, voire même d'utiliser des opérateurs logiques: 

```yaml
selector:
  matchExpressions:
    - {key: key-name, operator: In, values: [value-1, value-2, value-3, ...]}
    - {key: key-name, operator: NotIn, values: [value-4, value-5, ...]}
```

Via l'utilisations des labels, il est aussi possible de sélectionner dans le cadre des commandes vues en premier partie de cette introduction (l'approche impérative). Pour ce faire, il est pas exemple possible de supprimer les éléments possédant un label particulier: 

```bash
kubectl delete object-type-1,object-type-2,... -l key=value
```

--- 

### Comment Kubernetes s'organise

Dans l'univers Kubernetes, il est intéressant de savoir comment Kubernetes se charge de savoir si un conteneur est en état de marche ou non. Pour se faire, Kubernetes utilise ce que l'on appelle une `liveness probe`, qui existe de base pour la plupart des application, mais qu'il nous est possible de modifier si notre application a un fonctionnement particulier. Pour paramétrer cette fonctionnalité, il est possible de le faire dans les fichiers de ressources, via l'attribut dédié:

```yaml
containers:
  - name: web-server
    image: nginx
    imagePullPolicy: IfNotPresent
    livenessProbe:
      httpGet:
        path: /
        port: 80
      periodSeconds: 15
      initialDelaySeconds: 5
```

De même, il est possible via l'utilisation de fichiers de ressources de définir de quelle façon Kubernetes va gérer le pull de nos images Docker. Par défaut, l'attribut a pour valeur `IfNotPresent` en cas d'asence de spécification du tag `latest` dans notre image, mais il est possible de le changer à `Always` pour forcer le pull d'une image en cas de changement sans avoir modifié le tag, ou sur `Never` pour que Kubernetes ne cherche pas de son côté à pull c'image Docker, quand bien même le tag serait différent ou l'image absente.



---

[Retour](../../README.md)