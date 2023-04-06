# Introduction à Kubernetes

Kubernetes existe dans le but de pallier à certain problèmes que l'on pourrait rencontrer dans le cadre de l'utilisation de Docker. Par exemple, il est souvent délicat de devoir déployer manuellement des conteneurs, en particulier si ces derniers finissent par avoir un soucis et se stopper suite à une erreur. A l'heure actuelle, le deploiement Docker demandera la majorité du temps une personne présente en temps réelle pour gérer les conteneurs un par un, ce qui risque d'augmenter rapidement les coups de déploiement d'une application, en particulier si ce déploiement a lieu dans le cloud comme sur des services tels qu'**Azure**, **GCP** ou **AWS**.

Dans un contexte de déploiement professionnel, l'autre cas de figure qui pourrait se présenter est la nécessité de devoir démultiplier ou réduire le nombre de conteneurs de notre application en cas de forte demande ou en cas de pause temporaire de la demande. Pour ce faire, Kubernetes est un service optimal nous assurant un scaling de notre application en temps réel, en plus de permettre de redistribuer les demande des clients vers les différents conteneurs de sorte à éviter une trop forte demande de performance d'un conteneur en particulier. Le tout mis dans le cadre d'une multitudes de conteneurs pouvant tourner non par sur une seule machine hôte mais bien sur plusieurs machines rend les capacités de Kubernetes nécessaire dans le monde actuel, en particulier si l'on veut se mesurer aux géants de ce monde. La plupart des fournisseurs de services Cloud offrent d'ailleurs la possibilité de déploier une application en se servant des services tels que l'**Auto-Scaling** ou le **Load Balancing**.

---

### Le Jargon Kubernetes

Dans l'univers de Kubernetes, il existe plusieurs mot-clés essentiels qu'il est bon de connaitre afin de pouvoir éviter les soucis de compréhension future. 

Un déploiement Kubernetes donne lieu à la création d'un `cluster`, qui consiste en une multitude de `nodes` pouvant être de deux types:

* Les `master nodes` dont l'objectif est la manipulation des autres nodes. Celles-ci disposent dans leur fonctionnement de plusieurs composants essentiels tels qu'une API, des outils de plannification, etc... L'élément important à retenir est la capacité des master nodes à se servir d'un `control plane`.
* Les `worker nodes` qui sont de leur côté les réels éléments de travail dans un cluster Kubernetes. Ces worker nodes sont en général plus nombreuses et peuvent être de plusieurs types. La plupart du temps, chaque nodes de travail se voit être une machine virtuelle différente, permettant ainsi la spécialisation des conteneurs travaillant dans leur infrastructure interne. Pour fonctionner, ces nodes utilisent des `configurations`, des `proxys` ainsi que des `pods`. Un groupement de pods se verra la plupart du temps rassembler derrière un `service`, qui a pour rôle d'assurer la communication entre les éléments et de d'exposer une IP unique pour chaque pod.

---

### Les Worker Nodes

Une worker node est ainsi capable de gérer plusieurs conteneurs. Ces conteneurs seront la plupart du temps situés dans des `Pods`, qui sont des sous-ensemble regroupant le ou les conteneurs, ainsi qu'au besoin des volumes. Il est facile de se représenter une node de travail comme étant notre ordinateur dans le cadre de la réalisation d'un Docker Compose, mais il ne faut pas oublier que ces dernières peuvent être à la fois des machines physiques mais aussi des virtualisation d'ordinateurs. 

Chaque node de ttravail dispose pour sont fonctionnement d'un `kubelet`, qui a pour rôle d'assurer la communication entre les nodes, en particulier avec la node maîtresse, d'un daemon Docker dans le but de faire tourner les conteneurs et d'un proxy qui est utilisé dans le cadre d'une communication inter-nodes. 

Une node de travail ne peut exister en solitaire, et il lui faut pour assurer son fonctionnement la supervision d'une node maîtresse dont l'objectif est le management des multitudes de nodes de travail, un peu comme un développeur assurerait le lancement ou le déploiement de X conteneurs sur X machines, mais de façon automatisée et configurable.

---

### Les Master Nodes

Les nodes maîtresses ont une architecture plus spécialisée dans la gestion que les nodes de travail. En effet, chaque node maîtresse possède dans son infrastructure une `API` dont les kubelets se servent pour discuter avec elle. L'autre élément important d'une node maîtresse est la présence d'un `Scheduler`, dont l'objectif est ici la sélection de la node de travail la plus optimale pour le stockage et le lancement d'un ou de plusieurs conteneurs lors de la création d'un nouveau déploiement. Les déploiements sont ensuite gérés par des `manager de contrôleurs`, l'application de gestion se trouvant aussi dans l'infrastructure de notre node maîtresse. Enfin, il est possible de trouver également un `manager cloud spécifique` en fonction du service en ligne dans lequel nous sonmmes en train de réaliser notre cluster, comme c'est bien souvent le cas des grands du Cloud comme **AWS**. Il est ainsi possible, via une node maîtresse, d'assurer le fonctionnement de nodes de travail à la fois dans le même serveur / ordinateur mais également dans des emplacements Web complètements différents, ce grâce à la présence de l'API et des autres sous-services possédés par la node.

---

### Minikube

Pour travailler facilement avec Kubernetes et pour notre apprentissage, deux options s'offrent à nous si l'on a pas envie de se ruiner en création de cluster chez les cloud providers. LA solution la plus aisée est l'utilisation de **Minikube**, qui est un service permettant le lancement d'une machine virtuelle (qui peut d'ailleurs être dans un Docker), dont l'objectif sera la création d'un ensemble master-worker node unique nous permettant de gérer des pods de façon aisée. Pour installer minkube, le plus simple est de passer par l'utilisation d'un gestionnaire de packages tels que **Chocolatey** et d'entrer la ligne de commande ci-dessous dans un terminal ouvert avec les privilèges administrateur: 

```bash
choco install minikube kubernetes-cli
```

Gra^ce à cette ligne de commande, l'installation de minikube ainsi que de `kubectl`, l'outil d'administration de Kubernetes, se réalisera généralement sans encombre. Une fois l'installation effectuée, il ne restera plus qu'à créer notre cluster dans lequel on va pouvoir déploier nos applicatifs via la ligne de commande ci-dessous: 

```bash
# Pour démarrer notre cluster
minikube start 

# Pour connaitre l'état de fonctionnement du service minikube
minikube status

# Pour arrêter notre cluster
minikube stop
```

---

### Kind

L'autre possibilité est l'utilisation de **Kind**, qui, contrairement à minikube, permet la création de cluster plus complexes. Via l'utilisation de Kind, il est ainsi possible sur un même ordinateur de virtualiser plusieurs fausses machines virtuelles via des configurations sur la forme d'un ou de plusieurs fichiers `.yml`. L'utilisation de Kind est cependant plus complexe, et il vaut mieux avoir déjà un peu de pratique dans l'environnement Kubernetes pour comprendre réellement comment s'en servir. 

Son installation n'est cependant pas plus compliquée que celle de minikube, en particulier si l'on a, encore une fois, recourt à un gestionnaire de paquets tels que **Chocolatey**:

```bash
choco install kind kubernetes-cli
```

Pour démarrer un environnement dans lequel on peut déploier nos applicatifs avec Kind, les lignes de commandes suivantes sont nécessaires: 

```bash
# Pour démarrer un cluster ne possédant d'une node maîtresse
kind create cluster

# Pour stopper le cluster
kind delete cluster
```

Pour aller plus loin, en particulier pour créer des structures plus complexes avec X nodes maîtresses et / ou X nodes de travail, il va falloir utiliser l'option `--config chemin/vers/fichier.yml`. De plus, pour changer le nom de notre cluster, on peut utiliser l'option `--name nom-cluster`.

---

[Retour](../../README.md)