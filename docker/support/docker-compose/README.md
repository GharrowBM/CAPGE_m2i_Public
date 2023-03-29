# Docker Compose

### Définition

Si l'on se retrouve à devoir créer une application multi-conteneurs possédant potentiellement des réseaux, des volumes et des binds mounts, alors les lignes de commandes à connaitre et à utiliser deviennent rapidement un calvaire pour les dveloppeurs. Pour accélérer et facilité cette partie du travail, il est possible d'utiliser à la place **Docker Compose**. Docker compose est une feature de docker permettant la lecture d'un fichier au format `.yml` possédant toute la configuration de nos conteneurs. Via ce fichier, il est possible d'utiliser simplement une commande, `docker compose up`, pour lancer l'ensemble des conteneurs ou une autre, `docker compose down`, pour tout retirer d'un coup.

---

### Notre premier fichier de composition

Pour créer un fichier compatible avec Docker compose, il suffit de créer un fichier `docker-compose` au format `YAML` (**docker-compose.yml** ou **docker-compose.yaml** donc). Ce fichier va contenir l'ensemble de nos services, qui seront au final des conteneurs. Chaque conteneur va pouvoir par la suite être paramétré, comme par exemple le nom du conteneur, les réseaux dont il aura besoin, ses volumes, etc...

```yaml
version: '3'
services:
  first-service:
    image: image-name
    volumes: 
      - volume-name:/path/to/folder
    environment:
      FIRST_VARIABLE: value
      - OTHER_SYNTAX=value
    env_files:
      - path/to/file

volumes: 
  volume-name:
```

* `version`: Permet de définir quelle version de la syntaxe nous utiliserons dans notre fichier, celle-ci évoluant avec les version de **docker** et de **docker compose**.
* `services`: Sert à définir quels sous-ensembles devront être managés par Docker Compose.
* `volumes`: Sert à définir quels volumes créer / utiliser dans le cadre de notre déploiement (ces ressources seront créées dans le cas d'un volume nommé en cas d'absence de ce dernier).

Il n'y a pas besoin de spécifier le réseau que vont utiliser les conteneurs dans le cadre de l'utilisation de Docker Compose, ce dernier créé en effet automatiquement un réseau dont tous les conteneurs feront partie. 

Au niveau des services, plusieurs attributs sont possible d'être défini dans notre fichier de configuration:
* `image`: Le nom de l'image dont le conteneur va se servir lors de sa construction
* `build`: Les instructions de build permettant au conteneur de créer une image via un Dockerfile. L'attribut peut alors soit être directement le chemin reliant au fichier, soit posséder les attributs `context` dans le but de définir le dossier parent servant de référence au Dockerfile ainsi que `dockerfile` dans le dac où le fichier porterai un nom différent de **Dockerfile**.
* `ports`: L'ensemble des ports utilisés par notre conteneur dans le cas où l'on souhaiterai les exposer à l'hôte
* `volumes`: Les définition des volumes anonymes, nommés et bind mounts usés par le conteneur.
* `container_name`: Si l'on veut spécifier le nom qu'aura le conteneur à sa création 
* `environment`: Permet de spécifier des variables d'environnement
* `env_file`: Relie les variables d'environnement à un ou plusieurs fichiers dans le but de protéger les données sensibles.
* `depends_on`: Permet de décrire les autres services dont ce service aura besoin pour fdonctionner (Docker Compose fera en sorte de ne pas créer les conteneur dans le désordre et de stopper les conteneurs possédant une dépendance dans le cas où la dépendance viendrait à se stopper).
* `stdin_open`: Pour obtenir l'équivalent de `-i` et ainsi conserver un mode interactif.
* `tty`: Pour obtenir l'équivalent de `-t` et ainsi avoir un terminal disponible.

---

### D'autres commandes et options

Lors du lancement d'un service avec docker, il est possible d'ajouter l'option `--build` à notre `docker compose up` dans le but de forcer la création nouvelle d'image de sorte à surpasser l'utilisation du cache ou d'images déjà présentes dans notre base d'images.

De plus, si l'on souhaite uniquement créer les images et non exécuter notre composition, il est possible d'user de la commande `docker compose build`.

---

### Les conteneurs utilitaires

Dans le cas où l'on souhaiterai créer des conteneurs ayant pour objectif de nous aider dans nos tâches de développement, alors nous pouvons nous servir de conteneurs pour créer une structure de fichiers, comme par exemple l'initialisation d'un projet node, ou le branchement de dépendances, etc...

Il est d'ailleurs possible d'exécuter des commandes au sein d'un conteneur, et ainsi si l'on le souhaite de pouvoir utiliser un conteneur Docker dans le but de tester des scripts Bash sans avoir à installer de machine virtuelle Linux. Pour exécuter des applications dans un conteneur Docker, il faut utiliser la commande `docker exec nom-conteneur nom-bin`. 

Il est d'ailleurs intéressant de voir la différence, au sein d'un Dockerfile, entre l'instruction **CMD** et l'instruction **ENTRYPOINT**. Si l'on ajoute d'ailleurs, suite au nom de l'image, dans le cadre d'un `docker run`, une série de commandes, alors ces commandes seront celles qui seront lancées à la place de la commande par défaut:

- `CMD`: Va offrir une commande par défaut lors de l'exécution de notre conteneur 
- `ENTRYPOINT`: Va permettre de restreindre à l'utilisateur de notre conteneur l'utilisation d'une certaine commande

```dockerfile
# Dans ce cas, l'utilisateur pourra choisir par la suite d'utiliser uniquement des commandes en lien avec le début de la commande: 'node ...'
ENTRYPOINT [ "node" ]

# Dans ce cas, l'utilisateur pourra choisir par la suite d'utiliser n'importe quelle commande à la place de celle choisie ici par défaut
CMD [ "node", "script.js ]
```

Combiner ces informations avec un **Docker Compose** va nous permettre de simplifier la création de bind mounts dans le cas d'utilisation de conteneurs utilitaires. Pour pouvoir ajouter des commandes à la suite d'un `docker compose`, il va cependant falloir utiliser `docker compose run` pour lancer un service unique depuis notre fichier de configuration **docker-compose.yml**. Pour ce cas de figure, il n'y aura pas suppression automatique du conteneur, il est alors possible de le faire via `--rm`.

---

[Retour](../../README.md)