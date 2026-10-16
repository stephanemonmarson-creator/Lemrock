---
name: apercu-ads-client
description: >
  Génère un aperçu visuel (image PNG) montrant à quoi ressemblerait un client/prospect affiché en contenu sponsorisé dans les IA conversationnelles de Lemrock (GEA). L'aperçu reproduit fidèlement les 2 interfaces réelles : une IA spécialisée (avec carrousel produit + question sponsorisée) et une IA généraliste (avec texte ads). À partir du nom + site web du client (et de son logo s'il est fourni), la skill récupère l'univers de la marque, ses vrais produits, invente une requête utilisateur réaliste du secteur, et produit une image prête à montrer au client. À déclencher dès qu'Eve mentionne "montrer à un client à quoi ça ressemble", "aperçu ads", "afficher la marque en contenu ads", "je vais voir/rencontrer [client]", "mockup pour [marque]", "exemple de rendu pour [prospect]", "à quoi ça ressemblerait pour [marque]", ou donne simplement un nom de marque + une URL en contexte de rendez-vous ou de démo commerciale — même sans demande explicite d'image.
---

# Aperçu Ads Client — Lemrock

## Objectif

Quand Eve rencontre un prospect/client, lui montrer **concrètement** à quoi ressemblerait sa marque affichée en contenu sponsorisé dans les IA conversationnelles (produit GEA de Lemrock). Le livrable est **une image PNG** personnalisée à la marque, reproduisant les interfaces réelles.

Les 5 formats vivent dans **3 interfaces distinctes** :

| Interface | Formats affichés |
|-----------|------------------|
| **IA spécialisée** (verticale du secteur : IA mode, beauté, voyage, déco, parentalité…) | **Carrousel produit** + **Question sponsorisée** (glissée parmi des questions non sponsorisées, badge « Ad ») |
| **IA généraliste** (moteur + Chat IA) | **Texte ads** (logo/favicon + domaine + « Annonce » + phrase bleue) |
| **ChatGPT** (deux écrans distincts, un par format) | **Chat Card** (image + titre + courte description + lien vers la landing page) + **Product Ad** (annonce issue d'un flux catalogue : image + prix + lien fiche produit) |

---

## Inputs attendus

Eve fournit au minimum :
- **Le nom de la marque/client** (obligatoire)
- **Le site web** (fortement recommandé — sert à récupérer produits, couleurs, ton)
- Éventuellement un **logo** (uploadé) → placé dans la pastille du texte ads. Sinon, l'initiale de la marque est utilisée en secours.

Si seul le nom est donné, chercher le site officiel et en déduire l'univers de la marque.

---

## Déroulé

### 1. Récupérer l'univers de la marque
- Ouvrir le site du client (navigateur intégré / WebFetch) pour relever :
  - **3 produits phares** : nom exact, prix, et **URL de l'image produit** (indispensable pour le carrousel — on veut de vrais produits).
  - Le **secteur** → en déduire la **verticale** de l'IA spécialisée (voir table ci-dessous).
  - Le **domaine** (ex. `sezane.com`) et le ton de marque.
- Si Eve a fourni un **logo**, le récupérer ; sinon garder l'initiale.

**Table verticale → IA spécialisée** (adapter le nom, rester crédible) :
| Secteur client | `vertical_label` | Exemple `specialized_ai_name` |
|---|---|---|
| Mode / vêtements | mode | Modéa, StyleIA |
| Beauté / cosmétique | beauté | Belma, IA Beauté |
| Voyage / tourisme | voyage | Voyagea, TripIA |
| Déco / maison | déco | Maisonéa |
| Parentalité / bébé | parentalité | Parentéa |
| Sport / outdoor | sport | Sportea |
| High-tech / électro | tech | Techa |
| Alimentaire / épicerie | courses | Cuisinéa |

### 2. Écrire le contenu (crédible pour le secteur)
- **Requête utilisateur** (IA spécialisée) : une vraie question shopping du secteur.
- **Intro assistant** : une phrase qui introduit la sélection.
- **Produits** : les 3 vrais produits (titre + prix + image).
- **Questions suggérées** : 2 questions non sponsorisées + 1 **question sponsorisée** qui mentionne la marque (préfixée d'un emoji, comme dans les vraies interfaces).
- **Requête généraliste** : une requête plus large tapée dans le moteur.
- **Réponse IA généraliste** : un titre + 3 puces de conseils génériques et crédibles.
- **Texte ads** : `[Marque] : [phrase d'accroche produit]` (phrase bleue).
- **Follow-ups** : 2 questions « Pour aller plus loin ».
- **ChatGPT** (bloc `chatgpt`, à renseigner systématiquement) : une **requête ChatGPT** plus large que celle de l'IA spécialisée, une **réponse** (intro + 3-4 puces avec lead-in en gras + phrase de conclusion), puis les 2 annonces :
  - **Chat Card** : titre accrocheur + description courte + CTA (« Découvrir »). L'annonceur apparaît en haut avec la pastille logo.
  - **Product Ad** : titre = le produit exact du flux catalogue, prix, CTA (« Voir le produit »). Pas de description : le format vient du flux.
  - Les deux annonces partagent la même conversation, comme dans les vraies interfaces — seule l'annonce change.

⚠️ Rester honnête : pas de faux avis clients, pas de fausses promesses. Les prix/produits doivent venir du site réel quand c'est possible.

### 3. Préparer les visuels en local
Voir `references/images.md` pour le détail. En résumé :
- **Récupérer les images** : idéalement les vraies photos produit du site client. ⚠️ Les images **collées dans le chat ne sont pas lisibles sur le disque** — demander à Eve de les **enregistrer dans son dossier Téléchargements**, puis récupérer les plus récentes.
- **Recadrer** si les images sont des captures avec nom/prix intégrés : ne garder que le produit (technique de crop headless dans `references/images.md`).
- **Alléger** pour un rendu fluide (les images sont embarquées en base64) :
  ```bash
  for f in c1 c2 c3; do sips -Z 540 -s format jpeg -s formatOptions 82 "$f.png" --out "$f.jpg"; done
  ```
- **Fit produit** : pour des photos catalogue sur fond blanc (luxe, cosmétique…), utiliser `"image_fit": "contain"` → produit entier sur blanc, sans rognage. Sinon `"cover"` (défaut).
- **Logo** : placé dans la pastille du texte ads. Si pas de fichier logo, créer un petit SVG monogramme (initiales en sérif) — voir `references/images.md`.

### 4. Construire le HTML puis l'image
- Écrire un fichier de config JSON (voir `references/config-schema.md` pour le schéma complet et `references/example-config.json` pour un exemple).
- Lancer le générateur :
  ```bash
  python3 scripts/build_preview.py <chemin>/config.json
  # → produit widget_inner.html (pour Artifact) et preview_full.html (pour le PNG)
  ```
- **Rendre le PNG** : suivre `references/render.md` (mesure de la hauteur + capture headless Chrome haute résolution).

**Thème premium** — pour une marque de luxe (mode, joaillerie, maroquinerie haut de gamme…), ajouter `"theme": "premium"` dans la config : fond ivoire, wordmark de la marque en capitales espacées, titre en sérif Didot, filet or. L'habillage devient luxe **sans dénaturer le réalisme des 2 interfaces**. Par défaut (`"theme"` absent), rendu standard clair.

### 5. Livrer à Eve
- **Toujours montrer l'aperçu à Eve** — jamais l'envoyer directement au client.
- Deux livrables :
  1. **Le PNG** (`apercu_<marque>.png`) — c'est ce qu'Eve enverra au client. Il contient les 5 formats, dans l'ordre : IA spécialisée, IA généraliste, ChatGPT chat card, ChatGPT product ad.
  2. **Un lien Artifact** (publier `widget_inner.html`) pour qu'Eve voie le rendu en grand dans son navigateur, si le PNG ne s'affiche pas directement dans le chat.
- Terminer par une phrase courte : marque + requêtes utilisées.

---

## Notes de style (fidélité au produit réel)

- **IA spécialisée** = un widget chatbot gris arrondi : en-tête (nom de l'IA + « + Nouveau chat » + ✕), onglets « Chat » / « Shopping » (onglet actif souligné en turquoise), bulle question utilisateur, réponse assistant, carrousel de cartes blanches (image + tag marque + titre + prix + flèche →), pouce ↑/↓, questions suggérées, champ « Écrivez un message… », mention « Ce contenu est généré par IA… ».
- **IA généraliste** = interface type moteur : barre de recherche + onglets (Tous / Chat IA actif / Images / Vidéos / Actualités / Shopping), réponse en puces, texte ads (pastille logo + « domaine • Annonce » + phrase bleue), « Pour aller plus loin », « Question complémentaire », mention « Les réponses générées peuvent contenir des erreurs. »
- **ChatGPT** = interface épurée blanche : bulle utilisateur grise alignée à droite, réponse précédée du logo OpenAI, puces à lead-in gras, filet de séparation, mention « Sponsorisé », puis l'encart publicitaire (bordure fine, image carrée à gauche), et le champ « Envoyer un message à ChatGPT… ». Les CTA sont en vert ChatGPT (`#0d8a6a`), le prix du product ad aussi.
- La **question sponsorisée** se distingue uniquement par le petit badge gris « Ad » ; elle doit se fondre parmi les autres.
- Le **logo de la marque** va dans la pastille ronde du texte ads (fond blanc, logo non rogné).

Le gabarit et tout le CSS sont dans `scripts/build_preview.py` — ne pas réécrire le HTML à la main, passer par la config + le script.
