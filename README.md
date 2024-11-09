# GS15_Coffre_sa_maman A24

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

### Processus d'Utilisation

Le processus complet de l'utilisation du coffre-fort comprend plusieurs étapes pour garantir la sécurité et la confidentialité des données. Voici un schéma du flux d’utilisation :

```plaintext
Utilisateur                                         Coffre-Fort / Serveur
   │                                                        │
   │                       **1. Enrôlement**                │
   │───────────────────────────────────────────────────────>│
   │  - L'utilisateur crée un compte                        │
   │  - Un répertoire est créé pour l'utilisateur           │
   │  - Génération d'une paire de clés (publique/privée)    │
   │  - La clé publique est stockée en clair               │
   │<───────────────────────────────────────────────────────│

   │                       **2. Dérivation de la Clé (KDF)** │
   │───────────────────────────────────────────────────────>│
   │  - L'utilisateur entre un mot de passe                 │
   │  - Le mot de passe est transformé en clé privée        │
   │    via une fonction de dérivation (KDF)                │
   │  - Le sel est généré pour sécuriser la clé privée      │
   │  - La clé privée dérivée et le sel sont stockés        │
   │<───────────────────────────────────────────────────────│

   │                **3. Authentification à Double Sens**   │
   │───────────────────────────────────────────────────────>│
   │  - Demande de certificat au coffre-fort                │
   │  - Vérification par une Autorité de Certification      │
   │<───────────────────────────────────────────────────────│
   │───────────────────────────────────────────────────────>│
   │  - L'utilisateur s'authentifie au coffre-fort          │
   │  - Preuve de possession de la clé privée               │
   │    via une preuve à divulgation nulle (ZKP)            │
   │<───────────────────────────────────────────────────────│

   │                    **4. Échange de Clés**              │
   │───────────────────────────────────────────────────────>│
   │  - L'utilisateur et le serveur échangent une           │
   │    clé de session en utilisant Diffie-Hellman          │
   │  - La clé de session sécurise les échanges             │
   │<───────────────────────────────────────────────────────│

   │         **5. Dépôt / Consultation de Fichiers**        │
   │───────────────────────────────────────────────────────>│
   │  - Dépôt ou consultation de fichiers                   │
   │  - Les fichiers sont chiffrés avec l'algorithme COBRA  │
   │    (chiffrement symétrique)                            │
   │  - Utilisation d'un hash MAC pour authentifier         │
   │    chaque échange                                      │
   │  - Les fichiers sont chiffrés pour stockage avec       │
   │    la clé privée de l'utilisateur (chiffrement RSA)    │
   │<───────────────────────────────────────────────────────│
```
# Processus d'Utilisation du Coffre-Fort Numérique

```mermaid
flowchart TD

    %% Enrôlement
    A[Début] --> B[Enrôlement]
    B --> C1[Création d'un compte<br>create_account(username)]
    C1 --> C2[Génération d'un répertoire utilisateur<br>create_user_directory(username)]
    C2 --> C3[Génération d'une paire de clés RSA<br>generate_rsa_keypair(bits)]
    C3 --> C4[Stockage de la clé publique en clair<br>save_public_key(username, public_key)]

    %% Dérivation de la clé (KDF)
    C4 --> D[Dérivation de la Clé (KDF)]
    D --> D1[Entrée d'un mot de passe par l'utilisateur]
    D1 --> D2[Dérivation de la clé privée avec un KDF<br>kdf(password, salt, iterations)]
    D2 --> D3[Génération d'un sel pour la clé privée<br>generate_salt()]
    D3 --> D4[Stockage de la clé privée dérivée et du sel<br>save_private_key(username, private_key, salt)]

    %% Authentification à double sens
    D4 --> E[Authentification à Double Sens]
    E --> E1[Demande de certificat au coffre-fort<br>request_certificate()]
    E1 --> E2[Vérification du certificat avec l'Autorité de Certification<br>verify_certificate()]
    E2 --> E3[Preuve de connaissance de la clé privée<br>zkp_proof_of_knowledge(username)]
    E3 --> E4[Authentification réussie]

    %% Échange de clés
    E4 --> F[Échange de Clés]
    F --> F1[Échange d'une clé de session via Diffie-Hellman<br>diffie_hellman_exchange()]
    F1 --> F2[Création d'une clé temporaire pour les échanges]

    %% Dépôt/Consultation de fichiers
    F2 --> G[Dépôt/Consultation de Fichiers]
    G --> G1[Dépôt ou consultation des fichiers<br>access_file(username, file_name)]
    G1 --> G2[Chiffrement des fichiers avec COBRA<br>cobra_encrypt(file_content, session_key)]
    G2 --> G3[Authentification de chaque échange avec un HMAC<br>hmac_authenticate(session_key, message)]
    G3 --> G4[Chiffrement des fichiers pour le stockage avec RSA<br>rsa_encrypt(file_content, private_key)]

    %% Fin du processus
    G4 --> H[Fin]
