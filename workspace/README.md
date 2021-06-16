# lab-cv
Bienvenu dans l'espace lab cv, équipé de GPU, de _pytorch_ et _open-cv_

Le container dans lequel vous travaillez à été génerer automatiquement à chaque push sur main du [dépot](https://github.com/datalab-mi/lab-cv). L'image docker est stockée [ici](https://github.com/orgs/datalab-mi/packages/container/package/lab-cv).

# Consignes
Dans cet espace (`/workspace`), vous pouvez sauver des objets, fichiers, dossiers... Ils seront **synchronisés** dans un stockage objet ovh, à **la clôture** de votre job.

Point de montage :
- `/workspace/data` : contient les données d'entraînements, sorties de modèles...
- `/workspace/notebook` : contient les notebooks. Si vous souhaitez protéger votre notebook, placez le dans un dossier qui porte votre nom.
