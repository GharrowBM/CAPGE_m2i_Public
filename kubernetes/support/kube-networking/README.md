# La communication dans Kubernetes

Pour permettre dans un premier temps la communication entre le cluster et le monde extérieur, il est important de réaliser un fichier de ressource de service. Via l'utilisation de services, il est possible de créer des adresses IP pouvany être la cible de requêtes, que cela soit d'un pod à un autre, d'une node à l'autre, ou du monde extérieur à un pod. Pour communiquer entre notre machine et le cluster, le plus simple est la création d'un service de type `LoadBalancer`.

```yml
apiVersion: v1
kind: Service
metadata:
  name: service-name
spec:
  selector:
    key: value
  type: LoadBalancer
  ports:
  - port: 80 
    # Port extérieur
    targetPort: 5000 
    # Port dans le conteneur
```

Via un service de ce type, et dans le cas où l'on déploie sur un cloud-provider gérant le load balancing, il est possible de bénéficier directement d'une adresse IP externe via la commande `kubectl get svc` pour lister les services.

Si l'on est en développement local, alors via minikube il est aussi possible de réaliser l'exposition de notre IP via l'utilisation de `minikube service service-name`. Via cette commande, notre navigateur va s'ouvrir automatiquement à l'adresse et au port générés. Il ne nous rester plus qu'à récupérer ses informations si notre application n'est pas une application web, et de les exploiter, par exemple via un client REST dans le cadre d'une API.

---

### Communication intra-pod

Dans le cadre de la communication entre deux conteneurs se trouvant dans le même pod, il est possible de réaliser celle-ci via l'utilisation de `localhost` ainsi que les ports demandés par les différents services. Il suffit alors d'ajouter soit via l'attribut `env`, soit via un service de type `ConfigMap` pour plus de sécurité.

---

### Communication inter-pod

Pour permettre à différents pods de communiquer entre eux, il nous faut déjà avoir créé un service pour chacun d'entre eux. Dans le cadre de pods devant communiquer entre eux mais ne pas être exposés à l'extérieur du cluster, il est possible de le faire via un service de type `ClusterIP`. Il nous sera ensuite possible de récupérer l'adresse IP via un `kubectl get svc`. 

Il est également possible de se servir de variables d'environnement créées automatiques par Kubernetes, qui peuvent servir à rediriger automatiquement vers l'adresse IP d'un service. Pour les utiliser, il suffit de respecter la syntaxe, qui est de la sorte:

```bash
SERVICE_NAME_SERVICE_HOST

# Par exemple, pour un service nommé 'blabla':
BLABLA_SERVICE_HOST

# Et pour un service nommé 'truc-bidule':
TRUC_BIDULE_SERVICE_HOST
```

Depuis l'avancement des technologies Kubernetes, il est aussi possible d'utiliser une feature qui se nomme **CoreDNS** dans le but de manipuler la communication inter-pods. A la façon de Docker compose, il est possible de simplement utiliser comme nom de domaine le nom de notre service suivi de son **namespace** (les namespaces ont pour rôle de séparer les ressources dans le but de les assigner à différentes équipes par exemple) et Kubernetes se chargera de rediriger les requêtes entrantes vers ce dernier.

```yml
environment: 
  - name: VAR_A
    value: "service-name.namespace-name"
```

Dans le cadre de l'utilisation de minikube, on peut se contenter du namespace `default` qui est assigné par défaut à toutes nos ressources.

---

[Retour](../../README.md)