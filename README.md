# Budget & Dépenses Simplifiées 💰

Une application web moderne pour la gestion des finances personnelles, développée avec FastAPI (Python) et React.

## 🎯 Fonctionnalités

### Phase 1 - MVP (Produit Minimum Viable)
- ✅ **Gestion des revenus et dépenses** : Ajout, modification, suppression avec catégorisation automatique
- ✅ **Tableau de bord interactif** : Visualisation du solde et des graphiques en temps réel
- ✅ **Authentification sécurisée** : Inscription/connexion avec JWT
- ✅ **Interface responsive** : Design adaptatif mobile/desktop avec Tailwind CSS
- ✅ **Graphiques dynamiques** : Camembert des dépenses par catégorie avec Chart.js

### Phase 2 - Fonctionnalités Avancées (À venir)
- 🔄 **Gestion des budgets** : Définition de limites et alertes de dépassement
- 🔄 **Import CSV** : Import automatique de transactions depuis fichiers bancaires
- 🔄 **Multi-utilisateurs** : Comptes familiaux partagés
- 🔄 **Export PDF** : Génération de rapports mensuels
- 🔄 **Conseils IA** : Suggestions d'optimisation basées sur les habitudes

## 🏗️ Architecture Technique

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐    SQL    ┌─────────────────┐
│     Frontend    │◄───────────────►│     Backend      │◄─────────►│   PostgreSQL    │
│   React + Vite  │     (JWT)       │  FastAPI + JWT   │           │   (Supabase)    │
│  Tailwind CSS   │                 │   SQLModel ORM   │           │                 │
│   Chart.js      │                 │                  │           │                 │
└─────────────────┘                 └──────────────────┘           └─────────────────┘
```

### Technologies Utilisées

#### Backend (Python)
- **FastAPI** : Framework API moderne et rapide
- **SQLModel** : ORM moderne avec validation Pydantic
- **PostgreSQL** : Base de données relationnelle
- **JWT** : Authentification sécurisée
- **Uvicorn** : Serveur ASGI haute performance

#### Frontend (React)
- **React 18** : Bibliothèque UI avec hooks
- **Vite** : Build tool rapide et moderne
- **Tailwind CSS** : Framework CSS utilitaire
- **Chart.js** : Graphiques interactifs
- **Axios** : Client HTTP pour les API calls

#### Infrastructure
- **Vercel** : Déploiement frontend (gratuit)
- **Render** : Déploiement backend (gratuit)
- **Supabase** : Base de données PostgreSQL (gratuit)
- **GitHub Actions** : CI/CD automatisé

## 🚀 Installation et Démarrage

### Prérequis
- **Node.js** 18+ et **npm**
- **Python** 3.11+ et **pip**
- **PostgreSQL** (ou compte Supabase)
- **Git**

### Option 1 : Développement avec Docker (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/Tarekazabou/Budget-D-penses-Simplifi-es.git
cd Budget-D-penses-Simplifi-es

# Lancer avec Docker Compose
docker-compose up --build

# L'application sera disponible sur :
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Documentation API: http://localhost:8000/docs
```

### Option 2 : Installation Manuelle

#### 1. Backend (FastAPI)

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Ou sur macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres de base de données

# Lancer le serveur de développement
uvicorn app.main:app --reload

# API accessible sur http://localhost:8000
```

#### 2. Frontend (React)

```bash
# Dans un nouveau terminal, aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api/v1

# Lancer le serveur de développement
npm run dev

# Application accessible sur http://localhost:3000
```

## ⚙️ Configuration

### Variables d'Environnement Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/budget_app
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
DEBUG=True
```

### Variables d'Environnement Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Budget & Dépenses Simplifiées
```

### Configuration Base de Données

#### Option A : PostgreSQL Local
```bash
# Installer PostgreSQL
# Créer une base de données
createdb budget_app

# Les tables seront créées automatiquement au premier lancement
```

#### Option B : Supabase (Recommandé pour la production)
1. Créer un compte sur [Supabase](https://supabase.com)
2. Créer un nouveau projet
3. Récupérer l'URL de connexion dans Settings > Database
4. Mettre à jour `DATABASE_URL` dans le fichier `.env`

## 📡 API Documentation

### Endpoints Principaux

#### Authentification
- `POST /api/v1/auth/register` - Créer un compte
- `POST /api/v1/auth/login` - Se connecter (retourne JWT)

#### Transactions
- `GET /api/v1/transactions` - Lister les transactions
- `POST /api/v1/transactions` - Créer une transaction
- `PUT /api/v1/transactions/{id}` - Modifier une transaction
- `DELETE /api/v1/transactions/{id}` - Supprimer une transaction

#### Dashboard
- `GET /api/v1/dashboard/balance` - Obtenir le solde
- `GET /api/v1/dashboard/expenses-by-category` - Dépenses par catégorie
- `GET /api/v1/dashboard/summary` - Résumé complet

### Documentation Interactive
Une fois le backend lancé, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🧪 Tests

### Backend
```bash
cd backend
pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm test
```

### Tests E2E (À venir)
```bash
npm run test:e2e
```

## 🚀 Déploiement

### Frontend sur Vercel
1. Connecter le repository GitHub à Vercel
2. Configurer les variables d'environnement :
   - `VITE_API_URL` : URL de votre API backend
3. Déploiement automatique à chaque push sur `main`

### Backend sur Render
1. Créer un nouveau Web Service sur Render
2. Connecter le repository GitHub
3. Configurer :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Ajouter les variables d'environnement
5. Déploiement automatique à chaque push sur `main`

### Base de Données Supabase
1. Créer un projet Supabase
2. Les tables seront créées automatiquement
3. Configurer Row Level Security (RLS) pour la sécurité

## 📁 Structure du Projet

```
Budget-D-penses-Simplifi-es/
├── 📁 backend/                 # API FastAPI
│   ├── 📁 app/
│   │   ├── 📁 core/           # Configuration et sécurité
│   │   ├── 📁 crud/           # Opérations base de données
│   │   ├── 📁 models/         # Modèles SQLModel
│   │   ├── 📁 routers/        # Endpoints API
│   │   ├── 📁 schemas/        # Schémas Pydantic
│   │   ├── dependencies.py    # Injections de dépendances
│   │   └── main.py           # Point d'entrée FastAPI
│   ├── 📁 tests/             # Tests unitaires
│   ├── requirements.txt      # Dépendances Python
│   └── .env.example         # Variables d'environnement
├── 📁 frontend/              # Application React
│   ├── 📁 public/           # Assets statiques
│   ├── 📁 src/
│   │   ├── 📁 components/   # Composants réutilisables
│   │   ├── 📁 pages/        # Pages principales
│   │   ├── 📁 services/     # API calls
│   │   ├── 📁 hooks/        # Custom hooks
│   │   └── 📁 utils/        # Utilitaires
│   ├── package.json         # Dépendances Node.js
│   └── .env.example        # Variables d'environnement
├── 📁 .github/workflows/    # CI/CD GitHub Actions
├── docker-compose.yml       # Configuration Docker
└── README.md               # Documentation
```

## 🛠️ Développement

### Commandes Utiles

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m pytest

# Frontend  
cd frontend
npm install
npm run dev
npm run build
npm test

# Docker
docker-compose up --build
docker-compose down
```

### Contribution
1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📊 Roadmap

### Version 1.0 (MVP) ✅
- [x] Authentification JWT
- [x] CRUD Transactions
- [x] Dashboard avec graphiques
- [x] Interface responsive
- [x] Déploiement automatique

### Version 1.1 (En cours)
- [ ] Gestion des budgets et alertes
- [ ] Filtres avancés
- [ ] Export des données
- [ ] Notifications push

### Version 2.0 (Futur)
- [ ] Import CSV automatique
- [ ] Comptes multi-utilisateurs
- [ ] Application mobile (React Native)
- [ ] Intégration bancaire
- [ ] Conseils IA personnalisés

## 🤝 Support

- **Documentation** : Consultez ce README et la doc API
- **Issues** : Créez une issue GitHub pour les bugs
- **Discussions** : Utilisez les GitHub Discussions pour les questions

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Tarek Azabou** - *Développeur principal* - [@Tarekazabou](https://github.com/Tarekazabou)

---

**Note** : Ce projet suit les meilleures pratiques de développement moderne avec une architecture scalable, sécurisée et facilement maintenable. Toutes les technologies utilisées sont open source et gratuites pour le développement et le déploiement de base.