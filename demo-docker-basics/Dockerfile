FROM python
# On travaille à partir de l'image officielle de Python

WORKDIR /app
# On créé un dossier dans lequel notre code se verra être isolé

COPY . .
# On copie tout ce qui est dans le dossier où se trouve le Dockerfile dans le dossier courant du conteneur (défini à app/ par l'instruction précédente)

CMD [ "python", "main.py" ]
# On fait en sorte d'exécuter la commande adaptée pour notre application, ici une simple commande comme celle ci-dessous:

# python main.py
