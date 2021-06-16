# lab-cv
_Dépot qui permet de construire une image docker boîte à outil en Computer-Vision, avec une sur-couche ovh pour profiter du service ai-training (notebook, gestion mémoire...)._

# Prérequis

- Avoir des identifiants de connexion à ovh ai training

- Installer la [CLI ovh](https://docs.ovh.com/gb/en/ai-training/install-client/).

- Installer Make pour makefile

- Installer [docker](https://docs.docker.com/engine/install/)


# Fonctionnement

En tant qu'utilisateur:

0. Spécifier les options dans le fichier artifacts (à completer avec VERSION, NB_GPUS, NB_CPUS)

1. Lancer un job (= 1 container): `make deploy-job`

2. Voir les logs et les jobs en cours [(docs)](https://docs.ovh.com/gb/en/ai-training/usage-client/). Par exemple, suivre le lien url de `make data-upload SRC=mon.fichier DST=lab-cv-data`

3. Pour lancer un script sans notebook : `make deploy-job command="python /workspace/code/myscript.py"`

4. Pour transférer des données sur le bucket :
`make data-upload SRC=my.file DST=bucket.name`

5. Arrêter le job (Pour ne pas faire exploser la facturation) `ovhai job stop <id>`
