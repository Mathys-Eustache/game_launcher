# Feuille de Route : Application de Jeux pour Senior

Ce document retrace toutes les étapes pour créer l'application de bureau hybride (Go/React + Python) destinée à la voisine de ta grand-mère.

## 🛠️ Phase 1 : Préparation de l'environnement
- [X] Installer **Go** (langage backend).
- [X] Installer **Node.js** (pour faire tourner React/Vite).
- [X] Installer **Python** (pour la logique des jeux).
- [X] Installer **Wails** via le terminal (`go install github.com/wailsapp/wails/v2/cmd/wails@latest`).
- [X] Initialiser le projet Wails (`wails init -n senior_games_launcher -t react-ts`).
- [X] Mettre en place l'arborescence des dossiers (créer `games_logic`, organiser `frontend` et `backend`).

## 🎨 Phase 2 : Interface Utilisateur (React + CSS)
*Objectif : Une interface ultra-accessible, lisible et simple.*
- [X] Nettoyer le code généré par défaut dans `frontend/src`.
- [X] Créer le composant `GameCard.jsx` (Gros bouton pour chaque jeu).
- [X] Configurer le fichier `index.css` (Polices très grandes, couleurs à fort contraste).
- [X] Créer le menu principal dans `App.jsx` avec 4 gros boutons :
  - [X] Mahjong
  - [X] Mots Fléchés
  - [X] Solitaire
  - [X] Quitter l'application (Bouton rouge très visible).

## 🌉 Phase 3 : Le Pont et le Backend (Go)
*Objectif : Relier les boutons React aux scripts Python.*
- [X] Dans `backend/app.go`, créer les fonctions Go qui seront appelées par les boutons :
  - [X] `LaunchSolitaire()`
  - [X] `LaunchMotsFleches()`
  - [X] `LaunchMahjong()`
- [X] Implémenter l'exécution de processus (`os/exec`) en Go pour lancer les scripts Python de manière invisible.
- [X] Connecter ces fonctions Go aux événements "onClick" des boutons React.

## 🐍 Phase 4 : Développement des Jeux (Python)
*Objectif : Coder la logique des jeux de manière indépendante.*
- [ ] **Jeu 1 : Solitaire**
  - [ ] Initialiser `games_logic/solitaire/engine.py`.
  - [ ] Coder la logique du jeu de cartes.
  - [ ] Tester le lancement depuis le menu principal.
- [ ] **Jeu 2 : Mots Fléchés**
  - [ ] Initialiser `games_logic/mots_fleches/engine.py`.
  - [ ] Créer le générateur de grilles.
  - [ ] Tester le lancement depuis le menu principal.
- [ ] **Jeu 3 : Mahjong**
  - [ ] Initialiser `games_logic/mahjong/engine.py`.
  - [ ] Coder la logique d'association des tuiles.
  - [ ] Tester le lancement depuis le menu principal.

## 🚀 Phase 5 : Finalisation et Déploiement
- [ ] Lancer la commande de compilation `wails build`.
- [ ] Vérifier que l'application génère bien un exécutable unique (`.exe` ou `.app`).
- [ ] Tester l'exécutable final sur le bureau (double-clic) pour s'assurer que l'interface s'ouvre et que les jeux Python se lancent correctement.
- [ ] Installer l'application sur le bureau de la voisine de ta grand-mère en créant un gros raccourci bien visible !