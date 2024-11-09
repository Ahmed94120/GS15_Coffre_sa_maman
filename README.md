# GS15_Coffre_sa_maman

Ce projet implémente un coffre-fort numérique en Python pour le stockage sécurisé de données sensibles. Il est développé dans le cadre du cours GS15 en cryptologie, avec des exigences strictes en matière de sécurité.

## Fonctionnalités

1. **Gestion des Utilisateurs**
   - Création de comptes avec génération de clés publique/privée.
   - Dérivation de clé sécurisée (KDF) basée sur un mot de passe.
   
2. **Authentification et Sécurisation des Accès**
   - Authentification à divulgation nulle (Zero-Knowledge Proof) avec protocole de Schnoor ou de Guillou-Quisquater.
   - Authentification bidirectionnelle.

3. **Chiffrement Symétrique et Asymétrique**
   - Chiffrement des fichiers avec l’algorithme COBRA, inspiré de Serpent.
   - Chiffrement des échanges avec une clé de session sécurisée via Diffie-Hellman.

4. **Audit et Traçabilité**
   - Suivi d’audit pour journaliser les accès et les modifications.

5. **Gestion des Fichiers et Accès**
   - Stockage chiffré des fichiers, avec gestion des droits d’accès.

## Structure du Projet

### `src`
Contient l’ensemble des modules Python pour le coffre-fort.

- **encryption** : Gestion des méthodes de chiffrement symétrique avec l'algorithme COBRA.
- **authentication** : Implémentation des protocoles ZKP (Schnoor et Guillou-Quisquater) pour la vérification des utilisateurs.
- **key_management** : Gestion de la génération et de la dérivation des clés.
- **session_management** : Gestion de l’échange de clés Diffie-Hellman pour les sessions.
- **storage** : Fonctions pour chiffrer et déchiffrer les fichiers stockés.
- **utils** : Fonctions utilitaires (e.g., hashing, I/O).

### `docs`
Dossier de documentation, incluant le rapport du projet et les diagrammes d'architecture.

## Exécution

1. Cloner le dépôt.
2. Installer les dépendances générales via pip (numpy, bitarray, etc.).
3. Lancer `main.py` dans `src`.

```bash
python src/main.py
