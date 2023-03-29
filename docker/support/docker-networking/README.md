# Le networking en Docker

### Qu'est-ce que c'est ?

L'utilisation des networks dans Docker est due à un besoin métier particulier. En effet, lorsque l'on veut que nos conteneurs puissent discuter entre eux dans le but de s'échanger des informations ou des données, il nous faut généralement leur faire partager le même réseau. Ces conteneurs évoluant dans une machine virtuelle ou sur une machine distante et quand bien même cela est possible, il est bien souvent périlleux de leur faire utiliser le réseau de l'hôte pour récupérer des ressources de ce dernier. Docker nous offre ainsi la possibilité de créer différents réseaux dans lesquels nous pouvons brancher un ou plusieurs conteneurs. Un conteneur peut également appartenir à plusieurs réseaux en même temps.

Nous pouvons ainsi différencier plusieurs types de mise en relation de nos conteneurs: 
- Notre **conteneur** et le **Web**
- Notre **conteneur** et l'**hôte**
- Notre **conteneur** et un autre **conteneur**

---

### Communication Conteneur-Web / Conteneur-Hôte

Par défaut, les conteneurs Docker sont capable d'accéder au Web, il n'y a donc pas besoin d'ajouter de configuration particulière pour leur offrir la possibilité d'appeler une API par exemple. Cependant, les requêtes de connexion ou d'obtention de ressource vers notre hôte (localhost) ne fonctionnent pas.

Pour permettre à notre conteneur d'accéder à notre hôte, il va falloir utiliser une autre adresse dans notre code -> `host.docker.internal`. Via cette adresse, qui remplacera `localhost`, Docker va automatiquement remplacer le nom de domaine par l'adresse IP de notre hôte.

---

### Communication Conteneur-Conteneur

Si nous souhaitons permettre à plusieurs conteneurs Docker de communiquer entre eux, il va suffir d'utiliser les features spécifiques à Docker (créer / lister / supprimer des réseaux Docker). Pour le moment, il est possible d'utiliser l'inspection d'un conteneur `docker inspect nom-conteneur` pour obtenir l'adresse IP d'un conteneur et ainsi modifier notre code dans le but d'atteindre le conteneur. Cependant, cette solution n'est pas optimale, car l'adresse IP assignée à un conteneur est dynamique, elle changera à chaque fois que notre conteneur sera relancé.

Pour créer un reseau, il est possible d'utiliser la commande `docker network create nom-reseau`. Si l'on veut par la suite manipuler les réseaux, les commandes habituelles sont disponibles: `docker network ls` pour le listing, `docker network rm nom-reseau` pour la suppression sélective et `docker network prune` dans le but de supprimer tous les réseaux n'étant pas utilisés par un ou plusieurs conteneurs.

Il est possible de brancher un conteneur dans un réseau lors de l'utilisation de `docker run` via l'option `--network nom-reseau`. Dans le cadre d'une utilisation d'un réseau par des conteneur, Docker nous permet d'utiliser un système de nom de domaine particulier qui sera automatiquement reliée à l'IP d'un conteneur. Pour s'en servir, il n'y a rien de plus simple, il suffit de placer à la place d'une IP le nom du conteneur et Docker se chargera de le remplacer par son IP au sein du réseau.

```javascript
mongoose.connect({
  "mongodb://container-name:27017/database-name'
})
```

---

### Un peu de théorie

Docker se sert d'un DNS personnalisé pour permettre la liaison des conteneurs, il n'a pas la possibilité de modifier notre code. Lorsqu'une requête sort d'un conteneur et cherche à atteindre un nom de conteneur, Docker va automatiquement rediriger la requête vers le conteneur cible. 

De plus, il existe plusieurs drivers pour la liaison réseau des conteneurs, par défaut celui utilisé étant le driver `bridge`:

- `host`: Permet aux conteneurs de partager le réseau de l'hôte, et ainsi de partager `localhost`.
- `overlay`: Déprécié, il permet à plusieurs conteneurs tournant sur plusieurs daemons de communiquer entre eux.
- `macvlan`: Permet l'ajout d'une adresse mac sur un conteneur, qui peut ensuite être utilisée dans notre code pour atteindre le conteneur souhaité.
- `none`: Désactive purement et simplement les fonctionnalités réseau du conteneur.

---

[Retour](../../README.md)