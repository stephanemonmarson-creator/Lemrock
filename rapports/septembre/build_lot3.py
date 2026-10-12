import json,subprocess,pandas as pd
df=pd.read_excel('/root/.claude/uploads/78238b78-4021-5852-8246-f64175041d1c/da679589-Advertiser_campaign_tracking_export_2026-10-12.xlsx')
df['d']=pd.to_datetime(df['Metric date day'])
def agg(c,a,b):
    x=df[(df.Campagne==c)&(df.d>=a)&(df.d<=b)]
    return [x[k].sum() for k in ['Impressions (Lemrock)','Clics (Lemrock)','Conversions (affiliate)','GMV (€)','Budget consommé (€)']]
fr=lambda n:f"{n:,.0f}".replace(',',' ')
pc=lambda v:f"{v:.2f} %".replace('.',',')
def dl(a,b): v=(a/b-1)*100; return (f"▲ +{v:.0f} %" if v>=0 else f"▼ −{-v:.0f} %"),('up' if v>=0 else 'down')
def dp(a,b,u=' pt'): v=a-b; return (f"▲ +{v:.2f}{u}" if v>=0 else f"▼ −{-v:.2f}{u}").replace('.',','),('up' if v>0 else 'n' if v==0 else 'down')
def kp(c,compare,conv):
    i,k,cv,g,sp=agg(c,'2026-09-01','2026-09-30');ia,ka,cva,ga,spa=agg(c,'2026-08-01','2026-08-31');Y=agg(c,'2026-01-01','2026-09-30')
    if not compare:
        out=[["IMPRESSIONS",fr(i),"—","n",f"YTD {fr(i)}"],["CLICS",fr(k),"—","n",f"YTD {fr(k)}"],["CTR",pc(k/i*100),"—","n",f"YTD {pc(k/i*100)}"]]
        return out+[["CONVERSIONS","N/C","—","n","YTD —"],["CVR","N/C","—","n","YTD —"],["ROAS","N/C","—","n","YTD —"]]
    out=[["IMPRESSIONS",fr(i),*dl(i,ia),f"YTD {fr(Y[0])}"],["CLICS",fr(k),*dl(k,ka),f"YTD {fr(Y[1])}"],["CTR",pc(k/i*100),*dp(k/i*100,ka/ia*100),f"YTD {pc(Y[1]/Y[0]*100)}"]]
    if not conv: return out+[["CONVERSIONS","N/C","—","n","YTD —"],["CVR","N/C","—","n","YTD —"],["ROAS","N/C","—","n","YTD —"]]
    d=cv-cva
    return out+[["CONVERSIONS",fr(cv),("+" if d>=0 else "−")+f"{abs(d):.0f}" if d else "—",'up' if d>0 else 'n',f"YTD {fr(Y[2])}"],
      ["CVR",pc(cv/k*100),*(dp(cv/k*100,cva/ka*100) if d else ("—","n")),f"YTD {pc(Y[2]/Y[1]*100)}"],
      ["ROAS",f"{g/sp:.2f}".replace('.',','),*(dp(g/sp,ga/spa,'') if g or ga else ("—","n")),f"YTD {Y[3]/Y[4]:.2f}".replace('.',',')]]
W=lambda *l:[[[t,c,s,b] for t,c,s,b in x] for x in l]
A={}
A['Cdiscount_Voyages_Sejours']=dict(client='Cdiscount Voyages · Séjours',kpi=('cdiscount-voyages-sejours-awin-2026',1,1),cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs',
 words=W([('départ en vacances','O',18,1),('   séjour','K',16,1)],[('Airbnb','G',15,1),('   Booking','K',14,1)],[('Club Med','O',13,1),('   Pierre & Vacances','G',12,0)],[('billets d\'avion','O',11,1),('   Transavia','K',11,1)],[('valise cabine','K',11,1),('   trousse de toilette','G',11,0)],[('Center Parcs','K',11,1),('   TUI','G',11,0),('   Lastminute','O',11,0)]),
 queries=["Comment choisir un sac cabine conforme aux dimensions des compagnies ?","Comment organiser une trousse de toilette conforme aux règles de sécurité ?","Quelles offres ou prix pour une pochette Faraday ?"],
 cats=[["Airbnb",32],["Booking",22],["Opodo",7],["Club Med",7],["Pierre & Vacances",6],["Autres (Cdiscount Voyages < 0,1 %)",26]],
 insights=[["Le départ en vacances concentre la demande","82,3 % des conversations du secteur sont déclenchées par un départ en vacances, avec des recherches de billets d'avion et d'agence.","Associer chaque séjour à une date de départ proche : « Partez aux vacances de la Toussaint »."],
 ["Gagner en visibilité face à Airbnb et Booking","Cdiscount Voyages reste sous 0,1 % de part de voix (13e), face à Airbnb (31,8 %) et Booking (21,6 %). Côté ads : 4,0 %.","Élargir les topics ciblés (séjours, clubs, tout compris) pour augmenter la présence publicitaire."],
 ["Des réservations en hausse","4 réservations en septembre pour 1 119 € de GMV (2 en août). Le ROAS passe de 0,82 à 1,30.","Accélérer sur les offres qui convertissent, avant la fin de tranche."],
 ["Moins d'impressions, plus de clics","Les impressions baissent de 52 %, mais les clics progressent de 26 %. Le CTR passe de 0,19 % à 0,50 %.","Conserver le ciblage resserré et tester des accroches prix / dernière minute."]])
A['Cdiscount_Voyages_Vols']=dict(client='Cdiscount Voyages · Vols',kpi=('cdiscount-voyages-vol-awin-2026',1,1),cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs',
 words=W([('départ en vacances','O',18,1),('   billets d\'avion','K',16,1)],[('SNCF','G',15,1),('   easyJet','K',14,1)],[('Transavia','O',13,1),('   Ryanair','G',12,0)],[('sac cabine','O',11,1),('   Air France','K',11,1)],[('trousse de toilette','K',11,1),('   Volotea','G',11,0)],[('Skyscanner','K',11,1),('   Kayak','G',11,0)]),
 queries=["Comment choisir un sac cabine conforme aux dimensions des compagnies ?","Comment organiser une trousse de toilette conforme aux règles de sécurité ?","Montre-moi des sacoches Faraday disponibles."],
 cats=[["SNCF",32],["easyJet",15],["Transavia",14],["Ryanair",11],["Air France",11],["Autres (Cdiscount Vols < 0,1 %)",17]],
 insights=[["Le départ en vacances concentre la demande","85,3 % des conversations sont déclenchées par un départ en vacances : billets d'avion, sac cabine, trousse de toilette.","Mettre en avant les vols vers les destinations des vacances de la Toussaint et de Noël."],
 ["Exister face aux compagnies et au train","Cdiscount Vols reste sous 0,1 % de part de voix (13e). La SNCF (31,7 %), easyJet et Transavia dominent. Côté ads : 6,1 %.","Renforcer la présence ads sur les requêtes de comparaison de vols et de prix."],
 ["Un trafic multiplié par 5,5","Les clics passent de 1 694 à 9 406 (+455 %) et les impressions de 965 665 à 1 855 410 (+92 %). Le CTR passe de 0,18 % à 0,51 %.","Profiter de ce trafic pour pousser les offres les plus compétitives."],
 ["Aucune réservation attribuée","Aucune conversion n'est remontée par Awin en septembre malgré 9 406 clics.","Vérifier le tracking Awin et le parcours jusqu'à la réservation."]])
A['Levis']=dict(client="Levi's",kpi=('levis-rakuten-2026',1,0),
 words=W([('jean','O',18,1),('   501 Original Fit','K',16,1)],[('jean tulipe','G',15,1),('   élasthanne','K',14,1)],[('hauts ajustés','O',13,1),('   doudoune','G',12,0)],[('jupe en jean','O',11,1),('   veste','K',11,1)],[('Zara','K',11,1),('   Uniqlo','G',11,0),('   Wrangler','O',11,1)],[('collants','K',11,1),('   Celio','G',11,0)]),
 queries=["Montre-moi des hauts ajustés pour accompagner ce jean gris","Où trouver des jeans tulipe confortables avec un peu d'élasthanne ?","Montre-moi des idées de tenues complètes avec la jupe en jean longue","C'est quoi la vraie différence entre une softshell et une doudoune ?","Peut-on porter ce short au bureau sans être trop décontractée ?"],
 cats=[["Hauts et pantalons",29],["Vestes et plein air",21],["Sport et cyclisme",11],["Robes et jupes",13],["Lingerie et chaussettes",12],["Autres",14]],
 insights=[["Le jean comme pièce centrale du look","Les requêtes partent souvent du jean pour construire une tenue : hauts à associer, jupe en jean, jean tulipe avec élasthanne.","Construire les accroches autour du look complet : « Le 501 et le haut qui va avec »."],
 ["Mettre en avant le 501","Levi's représente 41,1 % des recherches qui nomment une marque, et le 501 Original Fit est le seul modèle cité.","Faire du 501 le produit d'appel des campagnes."],
 ["3e marque, devant tous les spécialistes du jean","Levi's est 3e en part de voix (17,6 %, +5,7 pts), derrière Zara et Uniqlo. Dans les recommandations spontanées des IA, Levi's recule à 7,9 % (−4,4 pts). Côté ads : 14,1 % (−0,6 pt).","Maintenir la présence ads et renforcer les contenus pour regagner les recommandations spontanées."],
 ["Moins d'impressions, plus de clics","Les impressions baissent de 29 %, mais les clics progressent de 46 %. Le CTR passe de 0,22 % à 0,44 %.","Garder le ciblage et décliner les accroches sur la saison froide (vestes, doudounes)."]])
A['Pierre_et_Vacances']=dict(client='Pierre & Vacances',kpi=('pierre-et-vacances-2026',0,0),cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs',
 words=W([('départ en vacances','O',18,1),('   résidence','K',16,1)],[('Airbnb','G',15,1),('   Booking','K',14,1)],[('Gîtes de France','O',13,1),('   Abritel','G',12,0)],[('vie en van','O',11,1),('   Odalys','K',11,1)],[('Club Med','K',11,1),('   Center Parcs','G',11,0),('   Lagrange','O',11,0)],[('Maeva','K',11,1),('   VVF','G',11,0)]),
 queries=["Comment choisir un sac cabine conforme aux dimensions des compagnies ?","Quel sac choisir pour combo randonnée et ski de rando ?","Comment organiser une trousse de toilette conforme aux règles de sécurité ?"],
 cats=[["Airbnb",25],["Booking",17],["Gîtes de France",11],["Abritel",7],["Pierre & Vacances",5],["Autres",35]],
 insights=[["Les vacances déclenchent presque toutes les conversations","91,2 % des conversations du secteur sont déclenchées par un départ en vacances.","Associer chaque résidence à une période de départ : vacances scolaires, week-ends prolongés."],
 ["7e marque citée, en progression","Pierre & Vacances pèse 4,7 % de part de voix (+2,1 pts), derrière Airbnb (24,8 %), Booking (16,6 %) et Gîtes de France (11,3 %).","Mettre en avant ce qui distingue les résidences : services, piscine, emplacements."],
 ["Être recommandé spontanément par les IA","Les IA recommandent spontanément Maeva (19,4 %) et Lagrange (19,0 %), mais citent Pierre & Vacances dans moins de 0,1 % des cas. Côté ads : 2,8 % (+2,8 pts).","Développer la présence ads et les contenus de marque pour entrer dans les recommandations."],
 ["Un premier mois encourageant","Lancée le 15/09, la campagne génère 638 950 impressions et 3 144 clics en 16 jours, pour un CTR de 0,49 %.","Poursuivre la diffusion et préparer les messages des vacances de Noël et d'hiver."]])
A['Qonto']=dict(client='Qonto',kpi=('qonto-2026',0,0),cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs',
 words=W([('création d\'entreprise','O',18,1),('   compte pro','K',16,1)],[('Boursorama','G',15,1),('   BNP Paribas','K',14,1)],[('Revolut Business','O',13,1),('   Shine','G',12,0)],[('retraite','O',11,1),('   vol de portefeuille','K',11,1)],[('carte perdue','K',11,1),('   LCL','G',11,0),('   Crédit Agricole','O',11,0)],[('banque en ligne','K',11,1),('   professionnels','G',11,0)]),
 queries=["À compléter : le rapport d'insights ne fournit pas d'exemples de requêtes pour Qonto"],
 cats=[["Boursorama",23],["BNP Paribas",14],["Revolut Business",10],["Crédit Agricole",10],["Banque Populaire",9],["Autres (dont Qonto 1,5 %)",34]],
 insights=[["Cibler la création d'entreprise","La création d'entreprise déclenche 15,1 % des conversations du secteur, un moment clé pour ouvrir un compte pro.","Construire les accroches autour du lancement : « Ouvrez votre compte pro en quelques minutes »."],
 ["Être présent après une perte ou un vol de carte","Le remplacement après perte (19,2 %) et le vol de portefeuille (5,4 %) déclenchent près d'un quart des conversations.","Mettre en avant la gestion des cartes depuis l'appli (blocage, carte virtuelle)."],
 ["Une forte présence ads, peu de recommandation spontanée","Qonto pèse 47,8 % de part de voix ads (+45,6 pts) et 1,5 % de part de voix (+0,8 pt). Les IA citent spontanément Shine (18,3 %) et Revolut Business (14,4 %), mais Qonto dans moins de 0,1 % des cas.","Enrichir les contenus de marque (comparatifs, guides de création) pour être recommandé sans être nommé."],
 ["Un premier mois solide","Lancée le 03/09, la campagne génère 1 094 021 impressions et 4 757 clics, pour un CTR de 0,43 %.","Mesurer les ouvertures de compte pour piloter la campagne au coût par acquisition."]])
A['SNCF']=dict(client='SNCF',kpi=('sncf-connect-2026',0,0),cats_title='MARQUES CITÉES',cats_sub='Part de voix dans les messages utilisateurs',
 words=W([('départ en vacances','O',18,1),('   train','K',16,1)],[('easyJet','G',15,1),('   Ryanair','K',14,1)],[('Air France','O',13,1),('   FlixBus','G',12,0)],[('Trainline','O',11,1),('   Eurostar','K',11,1)],[('BlaBlaCar','K',11,1),('   Trenitalia','G',11,0),('   Kombo','O',11,0)],[('valise','K',11,1),('   sac cabine','G',11,0)]),
 queries=["Comment choisir un sac cabine conforme aux dimensions des compagnies ?","Quel sac choisir pour combo randonnée et ski de rando ?","Comment organiser une trousse de toilette conforme aux règles de sécurité ?"],
 cats=[["SNCF",56],["easyJet",7],["Ryanair",7],["Air France",6],["FlixBus",6],["Autres",18]],
 insights=[["Une marque leader dans les conversations","La SNCF domine avec 56,4 % de part de voix et 61,8 % des recommandations spontanées des IA, loin devant easyJet et Air France.","Capitaliser sur cette position pour orienter les voyageurs vers SNCF Connect."],
 ["Une part de voix qui recule","La part de voix baisse de 27,7 pts et la recommandation spontanée de 4,4 pts sur le mois. La part de voix ads reste sous 0,1 %, la campagne ayant démarré le 30/09.","Suivre l'effet de la campagne sur la part de voix dès octobre."],
 ["Les vacances, unique déclencheur","100 % des conversations du secteur sont déclenchées par un départ en vacances.","Associer les trajets aux périodes de vacances : Toussaint, Noël, vacances d'hiver."],
 ["Premier jour de diffusion","La campagne a démarré le 30/09 : 139 036 impressions et 788 clics sur la journée, pour un CTR de 0,57 %.","Premier bilan complet à faire sur le mois d'octobre."]])
for f,d in A.items():
    c,cmp,conv=d.pop('kpi');d['kpis']=kp(c,cmp,conv);d['out']=f'/home/user/Lemrock/rapports/septembre/{f}_sept2026.pptx'
    print(f,[x[1:3] for x in d['kpis']])
    json.dump(d,open(f.lower()+'.json','w'),ensure_ascii=False,indent=1);subprocess.run(['python3','gen.py',f.lower()+'.json'],check=True)
