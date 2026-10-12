import re
s=open('gen.py').read()
head,body=s.split("s=p.slides.add_slide(p.slide_layouts[6])\n",1)
head=head.replace("D=json.load(open(sys.argv[1]))\n","D={}\n")
body="s=p.slides.add_slide(p.slide_layouts[6])\n"+body.replace("p.save(D['out'])\n","")
order=['allo_pneus','archipel','basket4ballers','bayard_jeunesse','bosch','cdiscount_mobile','cdiscount_voyages_sejours','cdiscount_voyages_vols','dorel','dsr','fidme','levis','mabex','marshall','monoprix','pierre_et_vacances','pour_de_bon','qonto','smartphone_id','sncf']
open('compile.py','w').write(head+"for name in %r:\n    D=json.load(open(name+'.json'))\n"%order+"\n".join("    "+l for l in body.splitlines())+"\np.save(sys.argv[1])\n")
