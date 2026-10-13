import json,sys,html
d=json.load(open(sys.argv[1]))
CSS="""@page{size:1000px 562px;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Liberation Sans",Arial,Helvetica,sans-serif;color:#1d1d1f}
.p{width:1000px;height:562px;background:#f7f6f2;padding:44px 64px;position:relative;page-break-after:always;overflow:hidden}
.ey{color:#e8692e;font-weight:700;font-size:13px;letter-spacing:.02em}
h1{font-size:36px;font-weight:700;line-height:1.05;margin-top:2px}
.cmp{position:absolute;right:64px;top:50px;text-align:right}.cmp .l{color:#8a8f99;font-weight:700;font-size:12px}.cmp .v{font-weight:700;font-size:14px;margin-top:2px}
.logo{position:absolute;right:64px;top:42px;font-weight:700;font-size:16px}
.sh{color:#e8692e;font-weight:700;font-size:14px;margin-bottom:6px}
.k{display:flex;gap:20px;margin-top:16px}
.kc{background:#fff;border-left:3px solid #e8692e;padding:9px 10px;width:108px;height:88px}
.kc .t{font-size:10px;font-weight:700;color:#55595f}.kc .n{font-size:20px;font-weight:700;margin:6px 0 3px}
.up{color:#2e8b3a;font-weight:700;font-size:10px}.dn{color:#e8692e;font-weight:700;font-size:10px}.y{font-size:8.5px;font-style:italic;color:#333;margin-top:5px}
.cc{background:#eeede9;padding:9px 10px;width:108px;height:88px;position:relative;margin-top:6px}
.cc .b{position:absolute;right:6px;top:-8px;background:#e2e1dd;border-radius:8px;font-size:8px;font-weight:700;color:#55595f;padding:1px 5px}
.cc .t{font-size:10px;font-weight:700;color:#8a8f99}.cc .n{font-size:20px;font-weight:700;color:#8a8f99;margin:6px 0 3px}.cc .y{color:#8a8f99}
.bub{background:#eeede9;border-radius:5px;padding:8px 10px;font-size:9.5px;line-height:1.4;margin-top:8px;color:#333}
.bub.alert{background:#fbe9e1;color:#8a3412}
.interp{background:#fff;border-left:3px solid #1d1d1f;padding:8px 12px;font-size:10px;line-height:1.45;margin-top:10px;width:404px}
.qi{display:flex;gap:16px;margin-top:6px}.qc{background:#fff;flex:1;padding:12px 16px;height:178px}
.qc h4{font-size:12px;color:#55595f}.qc .s{font-size:9.5px;font-style:italic;color:#8a8f99;margin:2px 0 8px}
.wc span{font-weight:700;margin-right:6px;line-height:1.35;display:inline-block}
.rq{font-size:9.5px;padding:4px 0;border-bottom:1px solid #eee}
.cat{display:flex;align-items:flex-end;font-size:9.5px;margin:3px 0}.cat .l{flex:1}.cat .tr{height:3px;background:#eee;margin-top:2px}.cat .fi{height:3px}.cat .v{width:38px;text-align:right;font-weight:700;font-size:11px}
.obj{color:#e8692e;font-weight:700;font-size:15px;margin-top:10px}.obj span{color:#1d1d1f;font-weight:400}
.ih{color:#55595f;font-weight:700;font-size:15px;margin:10px 0 8px}
.ig{display:grid;grid-template-columns:1fr 1fr;gap:14px 28px}
.ic{background:#fff;padding:14px 22px;min-height:180px}
.ic .hd{display:flex;gap:16px;align-items:flex-start}.ic .nm{color:#e8692e;font-weight:700;font-size:24px}.ic h3{font-size:16px;line-height:1.25;padding-top:2px}
.ic p{font-size:11.5px;line-height:1.45;color:#444;margin-top:9px}.ic .so{color:#1d1d1f;font-weight:700}
.ic .a{font-size:11.5px;font-weight:700;color:#55595f;margin-top:8px;line-height:1.4}
"""
def kpi(t,n,dl,y):
    cls='up' if dl.startswith('▲') else 'dn'
    return f'<div class="kc"><div class="t">{t}</div><div class="n">{n}</div><div class="{cls}">{dl}</div><div class="y">YTD {y}</div></div>'
def conv(t,n,y): return f'<div class="cc"><span class="b">INDICATIF</span><div class="t">{t}</div><div class="n">{n}</div><div class="y">—</div><div class="y">YTD {y}</div></div>'
k=d['kpi'];c=d['conv']
wc=''.join(f'<span style="font-size:{s}px;color:{"#e8692e" if o else "#1d1d1f"}">{html.escape(w)}</span>' for w,s,o in d['wc'])
rq=''.join(f'<div class="rq">{html.escape(q)}</div>' for q in d['req'])
mx=max(v for _,v,_ in d['cat'])
cat=''.join(f'<div class="cat"><div class="l">{l}<div class="tr"><div class="fi" style="width:{v/mx*100:.0f}%;background:{"#e8692e" if i==0 else "#8a8f99"}"></div></div></div><div class="v">{t}</div></div>' for i,(l,v,t) in enumerate(d['cat']))
p1=f'''<div class="p"><div class="ey">RAPPORT MENSUEL SEPTEMBRE (01/09/26 → 30/09/26)</div><h1>{d["name"]}</h1>
<div class="cmp"><div class="l">COMPARAISON</div><div class="v">vs AOÛT 01/08/26 → 31/08/26</div></div>
<div class="k"><div><div class="sh">DIFFUSION</div>{kpi(*k[0])}</div><div><div class="sh">ENGAGEMENT</div><div style="display:flex;gap:20px">{kpi(*k[1])}{kpi(*k[2])}</div></div>
<div style="margin-left:14px"><div class="sh" style="margin-bottom:0">CONVERSION</div><div style="display:flex;gap:16px">{conv(*c[0])}{conv(*c[1])}{conv(*c[2])}</div>
<div class="bub {d.get("trk_cls","")}">{d["trk"]}</div></div></div>
<div class="interp" style="margin-top:-52px"><b>Ce que disent ces chiffres :</b> {d["interp"]}</div>
<div class="sh" style="margin-top:14px">INSIGHTS QUALITATIFS</div>
<div class="qi"><div class="qc"><h4>CHAMP LEXICAL</h4><div class="s">Termes les plus fréquents</div><div class="wc">{wc}</div></div>
<div class="qc"><h4>EXEMPLES DE REQUÊTES</h4><div class="s">Questions posées aux IA</div>{rq}</div>
<div class="qc"><h4>CATÉGORIES DE PRODUITS</h4><div class="s">Répartition des requêtes</div>{cat}</div></div></div>'''
ins=''.join(f'<div class="ic"><div class="hd"><div class="nm">0{i+1}</div><h3>{x["t"]}</h3></div><p>{x["c"]} <span class="so">{x["so"]}</span></p><div class="a">→ {x["a"]}</div></div>' for i,x in enumerate(d['ins']))
p2=f'''<div class="p"><div class="ey">INSIGHTS QUALITATIFS · SEPTEMBRE 2026</div><h1>{d["name"]}</h1><div class="logo">Lemrock</div>
<div class="obj">OBJECTIF <span>{d["obj"]}</span></div><div class="ih">INSIGHTS QUALITATIFS</div><div class="ig">{ins}</div></div>'''
open(sys.argv[2],'w').write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{p1}{p2}</body></html>')
