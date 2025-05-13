# Job Tracker

Une application web pour suivre vos candidatures et recherches d'emploi.

## Structure du Projet

Le projet est divisé en deux parties principales :

- `frontend/` : Application React pour l'interface utilisateur
- `backend/` : API REST FastAPI pour la gestion des données

## Prérequis

- Python 3.8 ou supérieur
- uv (gestionnaire de paquets Python moderne)
- Node.js (pour le frontend)
- Un navigateur web moderne

## Installation

### Backend (FastAPI)

1. Accédez au dossier backend :
```bash
cd backend
```

2. Créez un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installez les dépendances avec uv :
```bash
uv pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
# Modifiez les variables dans le fichier .env selon vos besoins
```

5. Démarrez le serveur de développement :
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Accédez au dossier frontend :
```bash
cd frontend
```

2. Installez les dépendances :
```bash
npm install
# ou
yarn install
```

3. Démarrez l'application :
```bash
npm start
# ou
yarn start
```

## Fonctionnalités

- Suivi des candidatures
- Gestion des contacts
- Statistiques de recherche d'emploi
- Rappels et notifications

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. 
