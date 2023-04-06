# Les données dans Kubernetes

Pour manipuler des données dans Kubernetes, il est important de comprendre ce que l'on entend lorsque l'on parle de l'**état** de notre cluster. Par rapport à nos données, il peut être intéressant de rapeller qu'il existe deux grands types de données: 
- Les données générées par l'utilisateur et dont l'objectif est souvent de se voir être stockées dans une base de données pour un usage futur.
- Les données générées par l'application et qui sont en général conservées en mémoire vive le temps de vie de l'application.

Dans le cadre de Kubernetes, ces deux types de données devraient idéalement persister à un certain degré. Les données de l'application devrait survivre à un reboot du conteneur par exemple afin de ne pas perturber l'utilisation de notre application, alors que les données d'utilisateur doivent être stockées évidemment dans le but de les rendre disponible en tout temps. Kubernetes ne va cependant pas ré-ecrire l'Histoire, et le stockage des données dans des volumes par Docker ne sera pas changé pour autant. La variante se fera dans le cadre de la méthodologie de remplissage des volumes, qui devront alors être gérés par Kubernetes pour potentiellement les rendre disponibles sur plusieurs pods voire même sur plusieurs nodes / machines.

Au vu de l'emplacement des volumes dans Kubernetes, qui sont rappellons le dans des pods, il est important de se rendre compte que le temps de vie d'un volume va dépendre du temps de vie d'un pod dans lequel il se trouve. Quand bien même Kubernetes est capable de gérer et de peupler les volumes au niveau des nodes ou au niveau des cloud-providers, le fonctionnement interne de la liaison pod-volume ne peut être changée et les volumes seront spécifiques à leur pod.

La différence fondamentale entre des volumes Docker et des volumes dans le cadre d'un fonctionnement via Kubernetes vient donc de la façon dont ces volumes vont être typés et de quels drivers vont être fixés dans leur configuration. De plus, dans le cadre de Kubernetes, les volumes ne vont par forcément résister à un reboot.

---

### emptyDir

Pour notre premier cas de volume Kubernetes, nous allons commencer par nous intéresser au driver `emptyDir`, qui a pour objectif, comme son nom l'indique, la création d'un dossier vide dans lequel Kubernetes va stocker les éléments en cas de crash du conteneur. Par analogie, on pourrait dire qu'il s'agit d'un volume ayant le même objectif qu'un volume anonyme. Le seul détail qui change est qu'il sera réellement vide, car quand bien même l'image est censé apporter un fichier à cet emplacement dans l'application, Kubernetes va placer à cet emplacement un dossier vide, et donc tous les fichiers que l'image y aurait mit seront effacés. 

Dans le cadre d'une application ayant pour but le stockage de valeurs temporaires n'étant pas accessible en amont, ce n'est cependant pas un soucis, et cela protègera notre application de pertes éventuelles dues à un crash. 

Pour créer un volume de ce type, il faut, au niveau de l'attribut `spec` de notre deployment, indique que l'on créé un volume:

```yaml
spec: 
  volumes:
    - name: volume-name
      emptyDir: {}
```

Au niveau de la définition du conteneur, il nous faudra ajouter l'emplacement qui sera reliée à ce volume, via l'attribut `volumeMounts`:

```yaml
volumeMounts:
  - mountPath: /path/to/bind
    name: volume-name
```

---

### hostPath

L'utilisation d'un volume de type emptyDir pose cependant un soucis en cas d'utilisation de multiples replicas de notre conteneur, car chaque clone de notre conteneur va posséder son propre dossier lié. Pour pallier à ce soucis, nous allons désormais explorer le driver `hostPath`.

Via l'utilisation de ce driver, le chemin lié ne le sera plus vers un dossier vide pour chaque pod mais tous les pods du déploiement partagerons le même chemin lié dans la node de travail. Via de système, il sera possible de gérer les multiples clones d'un conteneur se trouvant sur la même node. Pour nous en servir, il suffit de changer les attributs de notre fichier de ressource:


```yaml
volumes:
  - name: volume-name
    hostPath:
      path: /path/to/data/on/node
      type: DirectoryOrCreate # Permet la création en cas d'absence du dossier contrairement à 'Directory' où le conteneur va crash en cas d'absence du chemin
```

Le soucis que l'on peut encore avoir avec ce genre de driver est le fait que dans la majorité des cas, un cluster va travailler avec plusieurs nodes. Malgré tout, ce style de driver offre des avantages non néglibeables sur la méthode de **emptyDir**.

---

### csi

Contrairement aux autres drivers, le CSI (Container Storage Interface) est un driver plus flexible car il permet de gérer plusieurs systèmes de volumes. En réalité, en tant qu'interface, il fixe des règles de fonctionnement d'un système de liaison de données dans Kubernetes, et cette interface est utilisée comme base commune dans plusieurs autres drivers, en particulier chez les cloud-providers. 

De part ce mode de développement de l'environnement Kubernetes, on peut voir l'apparition de système de gestion de volumes dans plusieurs systèmes du cloud et ne pas perdre nos connaissances, mais simplement les appliquer à ce cloud-provider de part son respect de l'interface **CSI**.

---

### Les volumes persistants

Il est désormais temps de voir un tout autre type de volume, les **volumes persistants**. En effet, jusqu'à maintenant, nos volumes ne sont soit disponibles que durant la vie d'un pod, soit durant la vie d'une node. Il est cependant fréquent que l'on veuille gérer des données non dépendantes d'un pod ou d'une node, mais qui soit communes. Bien entendu, des scénarios oû ce mode de fonctionnement existent également, et il est alors utile de pouvoir manier à la fois les volumes classiques et les volumes persistants.

Pour créer des volumes persistants, il nous est déjà possible de le faire via le driver CSI et l'utilisation d'un cloud-provider, mais il peut être intéressant de voir les solutions "maisons" de Kubernetes. 


Dans le cadre des volumes persistants, la premier grosse différence est l'indépendance entre un pod et un volume. En tant que gérant d'un cluster, il sera même possible de brancher / débrancher des volumes aux pods de notre choix. Pour gérer ces liaisons, il est nécessaire d'utiliser des **claims** qui permettront à certains pods d'accéder à X volumes, qui seront désormais des ressources de cluster au même titre qu'une node.

Pour définir un volume persistant, il est nécessaire d'utiliser des fichiers de ressources supplémentaires. Il nous en faudra un pour le volume persistant, et un autre pour les claims nécessaire au branchement du volume persistant sur le ou les nodes.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-name
spec:
  capacity:
    storage: '1Gi'
  volumeMode: Filesystem 
  storageClassName: standard
  accessModes:
    - ReadWriteOnce 
  hostPath:
    path: /path/to/data
    type: DirectoryOrCreate
```

L'objectif de notre fichier de ressource pour le volume persistant est la création d'une ressource Kubernetes permettant le stockage d'une quantité finie de données. Généralement fixée par l'administrateur du cluster, cette ressource sera par la suite soit occupée entièrement, soit partagée entre plusieurs nodes / pods. Pour gérer l'association entre cette quantité de données et les pods, il est désormais nécassaire de réaliser des claims: 

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-name
spec:
  volumeName: pv-name
  resources:
    requests:
      storage: '100Mi'
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
```

Via l'utilisation de claims, il est possible de séparer au besoin la ressource préalablement configurée en fonction des besoin de tels ou tels pods. De la sorte, un espace de données de taille finie peut être 'partitionné' et alloué en fonction des besoin en espace des pods. 

Les modes d'accès ()`accessModes`) servent à définir de quelle façon les pods vont pouvoir accéder à la ressource. Dans le cadre d'un accès de type `ReadWriteOnce`, alors la lecture et l'écriture seront possible pour un seul pod. Si l'on veut rendre la chose possible pour X pods, alors il nous faut utiliser soit de la lecture seule pour de multiples pods via `ReadOnlyMany`, soit de l'écriture et lecture pour X pods via `ReadWriteMany`.

Dans le cadre d'utilisation de volumes persistants et de claims, il est nécessaire de spécifier l'utilisation d'une **storage class**. Dans notre cas, l'utilisation de la classe par défaut fournie par minikube et qui est de base configurée pour la réalisation d'**hostPath** est évidente, mais il se peut que dans le cadre d'un cluster plus complexe, il nous faille en user d'une autre.

La **storage class** a pour objectif la gestion par kubernetes de l'association entre les volumes persistants et les nodes / pods. Elle permet de définir les types de stockages, par exemple leurs performances, leur accessibilité, etc... Via l'utilisation de telles données Kubernetes va être capable d'allouer les ressources de façon dynamique en fonction des besoins des différentes configurations futures, en particulier si la storage class est omise dans le cadre d'une claim.

---

### Les variables d'environnement

Pour utiliser des variables d'environnement dans le cadre d'un cluster Kubernetes, il va nous falloir utiliser, par exemple, dans le fichier de ressources de notre déploiement, ajouter l'attribut `env` suivi de X variables d'environnement: 

```yaml
containers:
  - name: container-name
    env:
      - name: VAR_A
        value: 1
      - name: VAR_B
        value: 2
      - name: VAR_C
        value: 3
```

Il est aussi possible de ne pas les mettre dans le fichier de déploiement, mais dans une ressource dédiée. Par exemple, pour récupérer les variables dans X déploiements. Pour ce faire, il est possible de créer une ressource de type ConfigMap. Ce type de ressource a pour but de simplement stocker un ensemble de clé et de valeurs qu'il est possible de récupérer dans nos autres ressources: 

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: conf-map-name
data:
  keyA: valueA
  keyB: valueB
  keyC: valueC
  # ...
```

Pour nous en servir dans notre déploiement, iul nous suffit désormais de modifier l'attribut `env` de sorte à récupérer la valeur depuis la **ConfigMap**: 

```yml
containers:
- name: container-name
  env:
    - name: VAR_NAME
      valueFrom:
        configMapKeyRef:
          name: configmap-name
          key: key-name-in-config-map
```

---

[Retour](../../README.md)