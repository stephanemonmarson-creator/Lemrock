# Préparer les images (produits + logo)

Les images sont **embarquées en base64** dans le HTML → rendu fiable et sans réseau, mais il faut donc disposer des fichiers en local.

## 1. Récupérer les images

Par ordre de préférence :
1. **Vraies photos du site client** : les télécharger (`curl -sL <url> -o cN.jpg`). Les sites de luxe (ex. louisvuitton.com) bloquent souvent l'accès bot — dans ce cas, demander les visuels à Eve.
2. **Images fournies par Eve** : ⚠️ **les images collées dans le chat ne sont PAS accessibles sur le disque**. Demander à Eve de les **enregistrer dans son dossier Téléchargements** (`~/Downloads`), puis :
   ```bash
   ls -t ~/Downloads/*.{png,jpg,jpeg} 2>/dev/null | head -5   # les plus récentes
   ```

## 2. Recadrer les captures (enlever nom + prix intégrés)

Souvent les visuels fournis sont des captures d'écran produit **avec le nom et le prix en dessous**. Le carrousel ajoute déjà titre + prix : il faut donc **ne garder que la photo**. Sans PIL ni ImageMagick, on recadre par capture headless (crop ancré en haut = on coupe le bas) :

```bash
# page qui affiche l'image en haut à gauche
printf '<!doctype html><body style="margin:0;padding:0"><img src="p1.png" style="display:block"></body>' > crop1.html
python3 -m http.server 8788 &                 # servir le dossier
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# window-size = largeur d'origine × hauteur SANS la légende (à ajuster en regardant l'image)
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 \
  --window-size=<W>,<H_sans_legende> --default-background-color=FFFFFFFF \
  --virtual-time-budget=1500 --screenshot=c1.png "http://localhost:8788/crop1.html"
```
Vérifier le résultat (Read sur `c1.png`) : la légende doit avoir disparu, sans couper le produit. Ajuster `H` si besoin.

## 3. Alléger

```bash
for f in c1 c2 c3; do sips -Z 540 -s format jpeg -s formatOptions 82 "$f.png" --out "$f.jpg"; done
```
Viser un `widget_inner.html` final < ~300 Ko (sinon l'Artifact est lourd).

## 4. Logo (pastille du texte ads)

- Si Eve fournit un **fichier logo** (dans Téléchargements) : le redimensionner (`sips -Z 240`) et le référencer dans `brand.logo`.
- **Sinon**, créer un petit **SVG monogramme** avec les initiales en sérif (rendu net, premium) :
  ```bash
  cat > logo.svg <<'SVG'
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100"><text x="60" y="78" font-family="Didot,'Bodoni 72',Georgia,serif" font-size="90" font-weight="700" text-anchor="middle" fill="#111111" letter-spacing="-12">LV</text></svg>
  SVG
  ```
  Puis `brand.logo = "logo.svg"`. Le générateur gère le SVG. Sans logo du tout, l'initiale (`brand.initial`) est utilisée en secours.
