import json,subprocess,pandas as pd
df=pd.read_excel('/root/.claude/uploads/78238b78-4021-5852-8246-f64175041d1c/da679589-Advertiser_campaign_tracking_export_2026-10-12.xlsx');df['d']=pd.to_datetime(df['Metric date day'])
def agg(c,m):
    x=df[(df.Campagne==c)&(df.d.dt.month==m)]
    return [x[k].sum() for k in ['Impressions (Lemrock)','Clics (Lemrock)','Conversions (affiliate)','GMV (€)','Budget consommé (€)']]
fr=lambda n:f"{n:,.0f}".replace(',',' ');pc=lambda v:f"{v:.2f} %".replace('.',',')
def dl(a,b): v=(a/b-1)*100; return (f"▲ +{v:.0f} %" if v>=0 else f"▼ −{-v:.0f} %"),('up' if v>=0 else 'down')
def dp(a,b,u=' pt'): v=a-b; return (f"▲ +{v:.2f}{u}" if v>=0 else f"▼ −{-v:.2f}{u}").replace('.',','),('up' if v>0 else 'n' if v==0 else 'down')
def kp(c,yi,yc,yconv,roas_aug_known=True):
    i,k,cv,g,sp=agg(c,9);ia,ka,cva,ga,spa=agg(c,8);YI,YC=yi+i,yc+k
    o=[["IMPRESSIONS",fr(i),*dl(i,ia),f"YTD {fr(YI)}"],["CLICS",fr(k),*dl(k,ka),f"YTD {fr(YC)}"],["CTR",pc(k/i*100),*dp(k/i*100,ka/ia*100),f"YTD {pc(YC/YI*100)}"]]
    if yconv is None: return o+[["CONVERSIONS","N/C","—","n","YTD —"],["CVR","N/C","—","n","YTD —"],["ROAS","N/C","—","n","YTD —"]]
    d=cv-cva;Yc=yconv+cv
    return o+[["CONVERSIONS",fr(cv),(("+" if d>0 else "−")+f"{abs(d):.0f}") if d else "—",'up' if d>0 else 'down' if d<0 else 'n',f"YTD {fr(Yc)}"],
      ["CVR",pc(cv/k*100),*dp(cv/k*100,cva/ka*100),f"YTD {pc(Yc/YC*100)}"],
      ["ROAS",f"{g/sp:.2f}".replace('.',','),*(dp(g/sp,ga/spa,'') if roas_aug_known else ("—","n")),"YTD —"]]
W=lambda *l:[[[t,c,s,b] for t,c,s,b in x] for x in l]
MB=dict(cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs')
A={}
A['Monoprix_Courses']=dict(client='Monoprix Courses',k=kp('monoprix-courses-kwanko-2026',7313304,11964,9,False),**MB,
 words=W([('sans additifs','O',18,1),('   étiquette','K',16,1)],[('vin','G',15,1),('   viande','K',14,1)],[('fromage','O',13,1),('   plats préparés','G',12,0)],[('frais de livraison','O',11,1),('   congeler','K',11,1)],[('grossesse','K',11,1),('   fleur de sel','G',11,0),('   comté','O',11,1)],[('Lidl','K',11,1),('   E.Leclerc','G',11,0),('   Picard','K',11,0)]),
 queries=["Comment repérer une vraie tablette sans additifs sur l'étiquette ?","Quel vin prendre si tu veux un goût moins tannique ?","C'est quoi le meilleur morceau de bœuf pour un pot-au-feu ?","Où je peux l'acheter en ligne et y a-t-il des frais de livraison ?","Peut-on préparer ce gratin à l'avance et le congeler ?"],
 cats=[["Lidl",27],["E.Leclerc",20],["Auchan",11],["Carrefour",11],["Intermarché",8],["Autres (dont Monoprix 5,5 %)",23]],
 insights=[["Une diffusion relancée en septembre","Après un mois d'août quasi à l'arrêt (41 893 impressions), la campagne repart : 1 263 529 impressions et 4 813 clics, pour un CTR de 0,38 %.","Campagne terminée le 23/09 : bilan à partager pour préparer une éventuelle reprise."],
 ["Rassurer sur la composition","La composition et les ingrédients (29,0 %) et le doute sur l'utilité réelle (21,4 %) sont les premiers freins : l'audience lit les étiquettes.","Mettre en avant la qualité des produits Monoprix (origine, labels, recettes simples)."],
 ["Exister face aux enseignes discount","Monoprix pèse 5,5 % de part de voix (+2,5 pts, 7e) et 8,2 % des recommandations spontanées des IA, loin de Lidl et E.Leclerc. Côté ads : 24,2 % (+6,1 pts).","Différencier Monoprix par la qualité et la proximité plutôt que par le prix."],
 ["Plus de ventes, mais un ROAS faible","8 conversions en septembre (2 en août) pour 337 € de GMV, soit un ROAS de 0,27 et un CVR de 0,17 %.","Vérifier le panier moyen attribué et le tracking Kwanko avant une reprise."]])
A['Ryobi']=dict(client='Ryobi',k=kp('ryobi-kwanko-2026',3505458,7087,4),objectif='Acquérir de nouveaux clients.',
 words=W([('perceuse','O',18,1),('   visseuse','K',16,1)],[('atelier','G',15,1),('   compresseur','K',14,1)],[('scie-sabre','O',13,1),('   brushless','G',12,0)],[('humidimètre','O',11,1),('   multimètre','K',11,1)],[('Bosch','K',11,1),('   Parkside','G',11,0),('   Makita','O',11,1)],[('béton','K',11,1),('   élagage','G',11,0)]),
 queries=["Quel outil Makita je devrais acheter en premier pour mon atelier ?","Quelle perceuse pour percer du béton et poser des étagères ?","C'est quoi la perceuse visseuse idéale pour bricoler à la maison ?","Un compresseur 50 L suffit-il pour un usage domestique ?","Je peux utiliser la scie-sabre sans être bricoleur ?"],
 cats=[["Mesure et détection",40],["Outils et coffrets",30],["Électroportatif",17],["Autres",13]],
 insights=[["Cibler le premier équipement","Les requêtes portent souvent sur le premier outil à acheter : atelier, perceuse visseuse pour bricoler, compresseur pour un usage domestique.","Présenter les kits de démarrage Ryobi comme le bon premier achat."],
 ["Parler à des bricoleurs non experts","Les questions montrent une audience peu experte : « Je peux utiliser la scie-sabre sans être bricoleur ? ».","Mettre en avant la simplicité d'usage et la polyvalence de la batterie unique."],
 ["Regagner face à Bosch et Parkside","Ryobi recule à 6,9 % de part de voix (−1,1 pt, 4e) et à 0,8 % des recommandations spontanées des IA, loin de Bosch (43,5 %) et Parkside (21,7 %). Côté ads : 8,2 % (−1,3 pt).","Renforcer la présence ads sur les requêtes perceuse et visseuse lors d'une prochaine campagne."],
 ["Un dernier mois plus performant","Diffusion jusqu'au 24/09 : 5 969 clics (+222 %) et un CTR de 0,52 %. 3 conversions attribuées.","Campagne terminée : partager le bilan pour préparer un renouvellement."]])
A['Iopole']=dict(client='Iopole',k=kp('iopole-2026',4829226,8515,None),**MB,
 words=W([('facturation électronique','O',18,1)],[('Chorus Pro','G',15,1),('   Pennylane','K',14,1)],[('Indy','O',13,1),('   Odoo','G',12,0)],[('retraite','O',11,1),('   séparation','K',11,1)],[('Sage','K',11,1),('   Shine','G',11,0),('   Tiime','O',11,1)],[('Cegid','K',11,1),('   EBP','G',11,0)]),
 queries=["À compléter : le rapport d'insights ne fournit pas d'exemples de requêtes pour Iopole"],
 cats=[["Chorus Pro",36],["Pennylane",12],["Indy",11],["Odoo",10],["Tiime",7],["Autres (dont Iopole 0,2 %)",24]],
 insights=[["Une catégorie dominée par Chorus Pro","Chorus Pro concentre 36,2 % des citations du secteur, devant Pennylane (11,7 %) et Indy (10,9 %). Iopole pèse 0,2 % (19e).","Positionner Iopole sur la réforme de la facturation électronique, en complément de Chorus Pro."],
 ["Les IA recommandent Sage et Shine","Sage (57,5 %) et Shine (37,8 %) captent presque toutes les recommandations spontanées des IA. Iopole y est sous 0,1 %.","Produire des contenus de référence (guides réforme 2026, comparatifs) pour être cité."],
 ["Une présence ads en recul","La part de voix ads d'Iopole passe à 25,2 % (−30,3 pts) avec la baisse de la diffusion.","Préparer une reprise avant les échéances de la réforme."],
 ["Une fin de campagne plus efficace","Diffusion jusqu'au 21/09 : 765 216 impressions (−79 %) et 3 523 clics (−45 %). Le CTR passe de 0,17 % à 0,46 %.","Campagne terminée : partager le bilan et proposer un renouvellement."]])
A['La_Redoute']=dict(client='La Redoute',k=kp('la-redoute-affilae-2026',4964272,10802,19),objectif='Générer des ventes avec un focus sur les nouveaux clients (~40 %) et les marques propres Fashion & Home.',**MB,
 words=W([('mariage','O',18,1),('   cadeau','K',16,1)],[('chaussures','G',15,1),('   rideaux','K',14,1)],[('déménagement','O',13,1),('   plante','G',12,0)],[('housses anti-acariens','O',11,1),('   livraison','K',11,1)],[('IKEA','K',11,1),('   Amazon','G',11,0),('   Kiabi','O',11,1)],[('réveillon','K',11,1),('   Maisons du Monde','G',11,0)]),
 queries=["Les housses anti-acariens sont-elles vraiment efficaces ?","Y a-t-il des risques d'allergies avec des rideaux recyclés ?","Quels modèles de chaussures montantes conseilles-tu pour la randonnée ?","Montre-moi des modèles de chaussures aquatiques fermées pour rochers"],
 cats=[["IKEA",35],["Amazon",32],["Kiabi",14],["La Redoute",6],["Zalando",4],["Autres",9]],
 insights=[["Des ventes en hausse","13 conversions en septembre (9 en août) pour 779 € de GMV. Le ROAS passe de 0,62 à 0,95.","Prolonger sur les catégories qui convertissent, en priorité les marques propres."],
 ["Activer les moments de vie","Le mariage (18,3 %), le cadeau (12,8 %), les vacances (12,4 %) et le déménagement (8,0 %) déclenchent les conversations.","Décliner des accroches mode (tenue de mariage) et maison (déménagement, réveillon)."],
 ["2e marque recommandée par les IA","La Redoute est 2e des recommandations spontanées des IA (19,1 %), derrière Amazon, mais recule à 6,1 % de part de voix (−1,8 pt). Côté ads : 11,8 % (+4,8 pts).","Maintenir la présence ads pour convertir cette recommandation en ventes."],
 ["Rassurer sur l'utilité et le prix","Le doute sur l'utilité réelle (21,8 %) et le prix (19,2 %) sont les premiers freins, devant la fiabilité (16,6 %).","Mettre en avant la qualité des matières et les retours gratuits."]])
A['Bayard_Jeunesse']=dict(client='Bayard Jeunesse',k=kp('bayard-jeunesse-kwanko-2026',382681,722,None),
 words=W([('livres papier','O',18,1),('   abonnement','K',16,1)],[('magazine','G',15,1),('   audiobook','K',14,1)],[('numéros numériques','O',13,1),('   BD','G',12,0)],[('Nathan','O',11,1),('   Mon Quotidien','K',11,1)],[('Glénat','K',11,1),('   Fleurus','G',11,0),('   Milan Presse','O',11,0)],[('livres audio','K',11,1),('   Spotify','G',11,0)]),
 queries=["Ça vaut le coup en audiobook ou mieux en lecture papier ?","Où je peux acheter le livre et à quel prix ?","Comment je m'abonne pour accéder aux numéros numériques ?","Comment je reçois le magazine papier chez moi ?","Montre-moi les livres audio disponibles sur Spotify"],
 cats=[["Livres papier",54],["Livres",28],["Journaux",7],["Magazines",7],["Livres audio et e-books",4]],
 insights=[["Simplifier l'abonnement","Les requêtes sur les magazines portent sur la façon de s'abonner et de recevoir les numéros, papier ou numériques.","Mettre en avant l'abonnement en quelques clics et la livraison à domicile."],
 ["Une marque très recommandée par les IA","Bayard Jeunesse est 2e des recommandations spontanées des IA (34,7 %, +12,3 pts), juste derrière Nathan (36,3 %). Côté ads : 11,1 % (+7,0 pts).","Capitaliser sur cette recommandation pour pousser l'abonnement."],
 ["Une part de voix en recul face à Nathan","La part de voix baisse à 23,1 % (−12,6 pts), loin de Nathan (59,3 %).","Renforcer la présence sur les requêtes lecture jeunesse et rentrée."],
 ["Les clics triplent","Les clics passent de 722 à 2 277 (+215 %) pour 7 % d'impressions en plus. Le CTR passe de 0,19 % à 0,56 %.","Campagne terminée le 11/10 : partager le bilan et proposer un renouvellement."]])
A['1001_Pneus']=dict(client='1001 Pneus',k=kp('1001-pneus-affilae-2026',1921449,3534,None),objectif='Acquérir de nouveaux clients (automobilistes, motards, cyclistes) avec un CPA cible de 10 €.',
 words=W([('pneu hiver','O',20,1),('    jante','K',18,1)],[('3PMSF','G',16,1),('    roue de secours','K',14,1)],[('voiture électrique','O',14,1),('    freinage','G',13,0)],[('Michelin Alpin','O',12,1),('    loi montagne','K',12,1)],[('Continental WinterContact','K',11,1)],[('chaînes à neige','O',11,1),('    kit anti-crevaison','G',11,0)]),
 queries=["Quels pneus pas chers sont quand même sûrs ?","Quels pneus VE recommandez-vous pour une Zoé 2020 ?","Peux-tu comparer Michelin Alpin 7 et Continental WinterContact TS870 ?","Chaînes, chaussettes ou pneus hiver : quoi privilégier ?","Mes pneus toutes saisons suffisent-ils pour la loi montagne ?"],
 cats=[["Pneus auto et dimensions",66],["Jantes et roues",15],["Pneus hiver et neige",9],["Crevaison et dépannage",7],["Pneus été et toutes saisons",2],["Pneus connectés",1]],
 insights=[["Préparer la saison hiver","Pneus hiver et chaînes à neige pèsent 8,9 % des produits nommés, avec des questions sur la loi montagne et le marquage 3PMSF.","Lancer des messages hiver dès octobre lors d'une reprise de campagne."],
 ["Cibler les voitures électriques","Les requêtes citent des modèles électriques (Zoé, MG4 EV) et l'impact des jantes sur l'autonomie.","Créer des accroches dédiées aux pneus pour véhicules électriques."],
 ["Gagner en visibilité face à Norauto et Michelin","1001 Pneus pèse 1,8 % de part de voix (+1,2 pt, 8e) et reste sous 0,1 % des recommandations spontanées des IA. Côté ads : 1,6 % (−21,1 pts).","Reprendre la présence ads avant la saison hiver."],
 ["Une diffusion relancée puis arrêtée","Diffusion du 01 au 10/09 : 159 222 impressions et 781 clics (+292 %), CTR de 0,49 %.","Vérifier le tracking Affilae et préparer la reprise pour viser le CPA cible de 10 €."]])
for f,d in A.items():
    d['kpis']=d.pop('k');d['out']=f'/home/user/Lemrock/rapports/septembre/{f}_sept2026.pptx'
    print(f,[x[1:3] for x in d['kpis']])
    json.dump(d,open(f.lower()+'.json','w'),ensure_ascii=False,indent=1);subprocess.run(['python3','gen.py',f.lower()+'.json'],check=True)
