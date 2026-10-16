# Schéma du fichier config JSON

Le générateur `scripts/build_preview.py` prend un fichier JSON décrivant la marque et le contenu. Les chemins d'images sont **relatifs au dossier du fichier config**.

```jsonc
{
  "theme": "premium",            // optionnel — "premium" (luxe) sinon rendu standard clair
  "image_fit": "contain",        // optionnel — "contain" (photos catalogue sur blanc) ou "cover" (défaut)

  "brand": {
    "name": "Sézane",              // nom affiché partout
    "domain": "sezane.com",        // affiché dans le texte ads
    "initial": "S",                // secours si pas de logo
    "logo": "logo.png"             // optionnel — pastille du texte ads (sinon retirer la clé)
  },

  "vertical_label": "mode",              // verticale de l'IA spécialisée (mode, beauté, voyage…)
  "specialized_ai_name": "Modéa",        // nom du chatbot spécialisé
  "specialized_ai_logo": "mt_logo.svg",  // optionnel — logo affiché en en-tête du chatbot (remplace le nom en texte)
  "specialized_ai_sub": "IA MODE · SHOPPING",  // sous-titre sous le nom
  "generalist_ai_name": "Assistant IA",  // nom du moteur généraliste

  // ---- variante "chatbot d'un média" (widget intégré à un article, ex. 20 Minutes) ----
  "chatbot_style": "publisher",          // logo du média centré + croix, ni onglets ni "+ Nouveau chat"
  "sugg_intro": "Cliquez sur une des questions ci-dessous :",  // phrase au-dessus des questions
  "article_context": {                   // rappel de l'article sur lequel le chatbot répond
    "source": "20 Minutes",
    "title": "Article « … » — le chatbot répond dans le contexte de l'article."
  },
  "sec_specialized_label": "Dans le chatbot IA de 20 Minutes — <span>carrousel produit + question sponsorisée</span>",
  "sec_generalist_label": "Dans Qwant — <span>texte ads</span>",  // libellés de section sur mesure (HTML autorisé)

  // ---- IA spécialisée (carrousel + question sponsorisée) ----
  "user_query_specialized": "Quelles pièces pour un vestiaire de mi-saison élégant ?",
  "assistant_intro": "Voici une sélection de pièces parfaites pour la mi-saison.",
  "products": [
    { "title": "Manteau en laine mélangée camel", "price": "185.00 €", "image": "img1.jpg" },
    { "title": "Blouse en coton brodée col claudine", "price": "95.00 €", "image": "img2.jpg" },
    { "title": "Sac en cuir grainé porté épaule", "price": "160.00 €", "image": "img3.jpg" }
  ],
  "carousel_sponso": "Sponsorisé · Boulanger",  // optionnel — mention de transparence sous le carrousel
  "suggested": [                         // questions NON sponsorisées
    "Propose-moi une tenue complète pour moins de 300 €",
    "Quelles couleurs pour un vestiaire capsule ?"
  ],
  "sponsored_q": "🧥 Quelles nouveautés découvrir chez Sézane cette saison ?",  // question sponsorisée (badge Ad ajouté auto)

  // ---- IA généraliste (texte ads) ----
  "user_query_generalist": "veste mi-saison femme",
  "answer_title": "Comment choisir sa veste de mi-saison",
  "answer_bullets": [
    "Privilégiez des matières respirantes comme la laine légère ou le coton.",
    "Optez pour des coupes intemporelles (blazer, trench) faciles à associer.",
    "Misez sur des teintes neutres — camel, écru, bleu marine."
  ],
  "textad_phrase": "composez votre vestiaire de mi-saison avec le manteau en laine camel",
  "followups": [
    "meilleures matières pour une veste de mi-saison",
    "veste légère ou trench : comment choisir ?"
  ],

  // ---- ChatGPT (chat card + product ad) — bloc à renseigner systématiquement ----
  "chatgpt": {
    "user_query": "Comment composer une garde-robe de mi-saison sans multiplier les achats ?",
    "answer_intro": "Pour une garde-robe de mi-saison efficace, quelques principes suffisent :",
    "answer_bullets": [                       // {b: lead-in en gras, t: suite} ou simple chaîne
      { "b": "Superposition", "t": "privilégiez des pièces fines qui s'empilent." },
      { "b": "Palette", "t": "trois teintes neutres suffisent à tout combiner." },
      { "b": "Matières", "t": "laine légère et coton restent confortables toute la journée." }
    ],
    "answer_outro": "Avec ces repères, une dizaine de pièces couvrent la saison.",
    "chat_card": {                            // image + titre + description courte + lien landing page
      "advertiser": "Sézane",                 // optionnel — défaut : brand.name
      "title": "Composez votre vestiaire de mi-saison",
      "desc": "Des pièces intemporelles pensées pour durer, fabriquées en Europe.",
      "cta": "Découvrir",                     // optionnel
      "image": "img1.jpg"
    },
    "product_ad": {                           // annonce issue d'un flux catalogue
      "title": "Manteau en laine mélangée camel",
      "price": "185,00 €",
      "advertiser": "Sézane",                 // optionnel
      "cta": "Voir le produit",               // optionnel
      "image": "img1.jpg"
    }
  }
}
```

## Règles
- Toujours **3 produits** (le 3e apparaît en partie, ce qui rend le carrousel réaliste).
- `sponsored_q` : commencer par un emoji du secteur et **mentionner la marque**.
- Prix au format `"185.00 €"`.
- Les images produit doivent être de **vrais produits** du site client quand c'est possible.
- Le bloc `chatgpt` est **optionnel côté script** (une config sans lui produit l'aperçu 3 formats), mais il faut **toujours le renseigner** : le livrable attendu par Eve compte 5 formats.
- Les deux annonces ChatGPT réutilisent la **même conversation** — c'est le générateur qui la duplique, il n'y a qu'un seul jeu de `user_query` / `answer_*`.
- `chat_card` porte une **description** (pas de prix) ; `product_ad` porte un **prix** (pas de description) : c'est ce qui distingue les deux formats.

## Un seul format (visuel pour un deck)
- `"only": "specialized" | "generalist" | "chatgpt"` : n'affiche que ce bloc, sans en-tête ni libellés de section. Utile pour l'emplacement « Exemple de diffusion » d'une slide (rendu 686 px de large, x2 → 1371 px).
- `"products": []` : pas de carrousel (ex. visuel « question sponsorisée seule »).
- `"assistant_bullets": ["…", "…"]` : réponse texte en puces sous `assistant_intro`, à utiliser quand il n'y a pas de carrousel.
- `"sponsored_q"` est optionnel : sans lui, aucune question sponsorisée (ex. visuel « carrousel seul »).
- `products[].brand` : tag marque d'une carte, si différent de `brand.name`.
- Les champs de la partie non affichée restent requis par le script : y mettre `"-"`.
