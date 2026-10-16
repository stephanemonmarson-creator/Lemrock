# Rendre le PNG haute résolution

Le générateur produit `preview_full.html` (HTML autonome, images embarquées en base64). Il faut le capturer en image. Le contenu fait 680px de large ; il faut connaître sa **hauteur** exacte pour cadrer sans marge blanche.

## Méthode recommandée (fiable)

### 1. Servir le fichier en local
`file://` est bloqué dans le navigateur intégré : passer par un petit serveur HTTP.
```bash
cd <dossier_de_travail>
python3 -m http.server 8799 >/tmp/mockserver.log 2>&1 &
sleep 1; cat /tmp/mockserver.log   # doit être vide
```
⚠️ **Vérifier le log.** Si un serveur d'un aperçu précédent occupe déjà le port, le lancement échoue (`Address already in use`) **mais la page répond quand même en 200** : on capture alors l'aperçu d'un autre client sans s'en rendre compte. Dans ce cas, prendre un autre port (8831, 8845…).

### 2. Mesurer la hauteur du contenu
Ouvrir la page dans le navigateur intégré (`preview_start` avec l'URL `http://localhost:8799/preview_full.html`), puis lire la hauteur :
```js
document.body.scrollHeight
```
(via l'outil javascript du navigateur). Noter la valeur, ex. `1779`.

### 3. Capturer en PNG avec Chrome headless (retina x2)
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=680,<HAUTEUR> \
  --default-background-color=FFFFFFFF --virtual-time-budget=2500 \
  --screenshot="<dossier>/apercu_<marque>.png" \
  "http://localhost:8799/preview_full.html"
```
- `--window-size=680,<HAUTEUR>` : largeur 680 (= largeur du gabarit), hauteur = la valeur mesurée.
- `--force-device-scale-factor=2` : rend en 1360px de large → net sur écran.
- `--virtual-time-budget=2500` : laisse le temps aux images base64 de s'afficher.

Le PNG obtenu fait `1360 x (2·HAUTEUR)`.

## Chemin de Chrome selon l'OS
- macOS : `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Chromium/Edge/Brave sont des alternatives si Chrome est absent.

## Secours si le navigateur intégré n'est pas disponible
Si on ne peut pas mesurer `scrollHeight` : rendre avec une hauteur généreuse (ex. `--window-size=680,2600`). Le fond étant blanc, l'excédent est du blanc en bas — acceptable, ou recadrable avec `sips` si la hauteur cible est connue.
