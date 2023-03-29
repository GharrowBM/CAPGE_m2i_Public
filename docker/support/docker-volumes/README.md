# Les volumes de Docker

### A quoi ça sert ?

Dans le cadre de l'utilisation des conteneurs, il est important de savoir que les données stockées dans nos conteneurs ne sont pas persistantes. Par défault, les informations stockées seront perdues en cas d'erreur ou de recréation d'un conteneur. Pour y remédier, nous allons devoir utiliser des volumes, qui permettent de stocker de façon plus sûre les données de nos applications.

Il existe plusieurs variantes de volumes:
- Les **volumes anonymes** qui servent à stocker des données temporaires
- Les **volumes nommés** qui servent à stocker les données permanentes
- Les **Bind Mounts** permettant de relier à notre système de fichier des chemins de notre conteneur

L'objectif des conteneur docker est ainsi de base de permettre une isolation totale des informations, et le faire que les données temporaires / persistentes de notre application se voient être perdues en cas de suppression puis de recréation de notre conteneur suit cette logique de non persistence. Ceci est en partie dû au fait que les conteneurs sont basés sur des images et que ces dernières sont `read-only`. Les données du conteneur disparaissent lors de sa suppression, et lors de se recréation, le conteneur se base uniquement sur l'image dont il a besoin, et non sur un état particulier de son cycle de vie.

---

### Nos premiers volumes

Les volumes sont des dossiers sur notre machine qui seront reliés à nos conteneurs. Les volumes sont des emplacements dans lesquels nos conteneurs peuvent écrire et qui peuvent par la suite être lus par ce dernier. De la sorte, il nous est possible d'avoir une persistence de nos données.

Dans notre Dockerfile, il est possible d'ajouter l'instruction **VOLUME** pour permettre la création d'un volume:

```dockerfile
VOLUME [ "/path/to/files" ]
```

Via cette instruction, Docker va gérer de lui-même la création d'un dossier pour y stocker les fichiers générés par notre conteneur. Ce volume sera ainsi utilisé par notre conteneur pour y stocker des fichiers, et il lui sera possible d'y retourner en cas de relance du conteneur. Cependannt, dans le cas où l'on voudrait brancher plusieurs conteneurs d'une même application à la même structure de données, cela ne sera pas possible. En effet, notre volume est actuellement un volume **anonyme**. 

Un volume anonyme est ainsi un emplacement dans notre machine qui va servir à notre conteneur pour y stocker des fichiers, mais ce dernier est spécifique à notre conteneur (de part le fait que l'association a lieu lors de la création du conteneur et est gérée par Docker via un ID généré aléatoirement). Nos volumes se trouveront dans des dossier gérés par Docker, et non par nous. Il est de par le fait impossible de savoir où ces dossiers se trouvent. Pour créer un un volume ciblable par plusieurs conteneurs et pouvoir atteindre la même structure de dossier gérés par Docker, il nous faut utilisé un **volume nommé** afin de représenter ce chemin nous étant inconnu par un mot, le **nom du volume**.

Pour pouvoir créer des volumes nommés lors du lancement de nos conteneurs, la méthode la plus simple est d'utiliser l'option `-v`. Via cette option, on peut spécifier le nom du volume avant de spécifier le chemin que l'on veut relier à un volume:

```bash
docker run -v nom-volume:/path/to/files image-name
```

---

### Les Bind Mounts

Lorsque l'on est un développeur, nous pouvons avoir besoin de pouvoir modifier nos fichiers de code et voir notre conteneur suivre nos changements sans avoir à nous rajouter comme étape la re-création de notre image. Pour y parvenir, il est possible d'utiliser ce que l'on appelle un `bind mount`. Le principe est de relier des fichiers de notre structure personnelle avec la structure de fichiers du conteneur. De sorte, nous avons la possibilité de modifier nous même en temps réel le contenu d'un conteneur via la manipulation de nos fichiers. 

La création d'un bind mount se trouve être la meme méthodologie que la création d'un volume nommé, à ceci près que l'on ne donnera pas un nom de volume en première partie de l'argument de l'option `-v` mais le chemin dans notre hierarchie de fichiers:

```bash
docker run -v /host/file/path:/container/file/path image-name
```

Dans le cadre de notre application Node.js, il nous faut cependant faire attention à bien comprendre le fonctionnement du bind mount pour en apprécier l'utilité. Un bind mount va chercher à relier nos fichiers et dossier **par dessus** ce que docker aurait accompli via l'utilisation des volumes. Dans le cas où nous n'aurions jamais utilisé la commande `npm install` pour générer nos modules, alors le dossier ne sera pas présent sur notre machine, et c'est son absence (docker ne se permet pas d'écrire sur notre machine les fichiers du conteneur dans le cas d'un bind-mount) qui sera copiée sur notre conteneur.

En effet, dans notre cas, il nous faudra utiliser plusieurs types de volumes pour notre application: 

- Un volume nommé pour stocker nos feedbacks `-v feedback:/app/feedback`
- Un volume anonyme pour stocker les modules de node `-v /app/node_modules`
- Un bind mount pour y relier nos fichiers durant le développement `-v "$(pwd):/app"`

Dans le cas où plusieurs éléments de volumes cherchent à relier nos dossiers et fichiers du conteneur à une ressource, alors c'est le chemin le plus long qui sera privilégié par Docker en cas de conflit. Ainsi, notre bind mount, dont le chemin ciblé au sein du conteneur est plus court que notre volume anonyme ou notre volume nommé, n'entrera pas en conflit avec la création et la liaison de nos deux autres volumes.

Concernant Node.js, il peut être utile, dans le cas d'un développement basé sur Docker et de l'utilisation de Bind mounts, d'avoir recours au package `nodemon` que l'on peut ajouter en dépendance de développement. De la sorte, et en ajoutant comme script l'exécution de notre application via `nodemon -L script.js`, il nous est possible d'observer les modifications à la fois si les fichiers HTML sont changés, mais également si notre Javascript évolue.

L'utilisation d'un Bind mount n'est souvent requise que durant le développement, et il est du coup utile d'avoir également l'utilisation de la commande **COPY** dans le cadre d'un **Dockerfile**. En effet, lorsqu'une personne exterieure à notre cercle de développement souhaite utiliser notre image, il lui faut avoir accès à tout le code nécessaire au lancement de l'application, et donc, il faut que tout ce code ait été copié au sein de l'image via la commande **COPY**.

---

### Les volumes Read-Only

Dans le cas où nous voudrions ne pas permettre à Docker de pouvoir écrire dans nos volumes mais simplement de pouvoir y lire des fichiers, alors il est possible de rendre ces liens **Read-only**. Ainsi, dans le cas d'un bind mount, il est possible d'empêcher Docker de créer des structures de dossiers vides ou de pouvoir y injecter des fichiers. Le bind mount n'aura alors plus que pour utilité d'être lu par Docker et de faire s'opérer les changement dans le conteneur, et non le sens inverse. Il ne nous reste plus qu'à créer des volumes anonymes pour tous les emplacements de notre application dans lesquelle cett dernière pourrait avoir besoin d'écrire.

---

### Gérer nos volumes

Pour pouvoir voir nos volumes, il est possible d'avoir recourt à la commande `docker volume ls`. Dans le cas où l'on souhaitera ajouter manuellement un volume, nous pouvons utiliser `docker volume create volume-name`. Dans le cas où l'on voudrait cette fois-ci supprimer un volume, nous pouvons user de `docker volume rm volume-name` pour le faire un par un, ou de `docker volume prune` pour supprimer tous les volumes non utilisés d'un coup. Si l'on veut observer un volume en particulier, il est également possible de le faire via `docker volume inspect volume-name`.

### .dockerignore

A la façon du fichier `.gitignore` dans l'univers du versioning de code, il existe la possibilité d'utiliser un fichier `.dockerignore` pour éviter la copie de certains fichiers lorsque l'on utilise la commande **COPY** dans un Dockerfile. Toutes les structures hierarchiques de chemins de fichiers seront ignorés lors de l'utilisation de telles instructions.

### Les arguments et variables d'environnement

Dans le monde du développement, il est utile de pouvoir créer des scripts qui sont plus génériques. Bien souvent, la création de tels éléments passe par l'utilisation d'arguments, alors que la sécurisation des données entrantes est gérée par le passage de variables d'environnement, lesquelles sont lues au moment de la compilation et évitent par exemple l'affichage d'un mot de passe en clair. Dans l'univers Docker, il est possible d'avoir recourt à ces deux concepts. 

* Les **arguments** sont disponibles dans le cadre d'un Dockerfile, mais ne sont plus disponibles par la suite dans le cadre de l'exécution du conteneur et donc dans le contexte de notre application. Pour en ajouter, il faut utiliser l'option `--build-arg` durant un `docker build`
* Les **variables d'environnement**, à contrario, sont disponibles à la fois dans le Dockerfile mais aussi dans le conteneur. Pour ajouter une variable d'environnement, on peut user de l'option `--env` (ou `-e`) dans un `docker run`

```dockerfile
# On créé la variable d'envrionnement 'LISTENING_PORT' et on lui donne comme valeur 80 par défaut (modifiable via --env LISTENING_PORT=1234)
ENV LISTENING_PORT=80

# On se sert de notre variable dans le cadre de l'exposition d'un port du conteneur
EXPOSE ${LISTENING_PORT}
```

Il est possible de stocker nos variables d'environnement dans un fichier `.env` et utiliser ensuite l'option `--env-file chemin/du/fichier` pour conserver les variables et si possible les exclures via l'utilisation de `.gitignore` et `.dockerignore` (l'utilisation d'un fichier empêchera la lecture des variables d'environnement par l'utilisation d'une commande `docker history image-name` par des individus mal intentionnés).

Pour utiliser les arguments, on va avoir recourt à une syntaxe de cet ordre: 

```dockerfile
ARG NAME=VALUE
```

Via l'utilisation d'arguments, il est possible, non pas de créer des conteneurs différents basés sur la même image comme c'est le cas avec des variables d'environnement, mais bien des images différentes basées sur le même fichier **Dockerfile**.

Les lignes d'arguments ou de variables d'environnement ajoutant, comme les autres instructions dans un Dockerfile, des couches à notre image, il est important de bien les ordonner dans le but d'éviter de casser l'utilisation du cache de part leur modification fréquente et du placement de ces instruction en début du Dockerfile.

---

[Retour](../../README.md)