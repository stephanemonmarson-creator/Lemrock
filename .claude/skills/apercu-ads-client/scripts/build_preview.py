#!/usr/bin/env python3
"""Construit l'aperçu ads (HTML autonome + HTML widget) à partir d'une config marque.
Les images produit sont embarquées en base64 pour un rendu fiable partout (widget, PNG headless)."""
import base64, json, sys, os, html

def data_uri(path):
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp", "svg": "svg+xml"}.get(ext, "jpeg")
    with open(path, "rb") as f:
        return f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()

def esc(s):
    return html.escape(str(s), quote=True)

CSS = """
* { box-sizing: border-box; }
.ap-root { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", system-ui, sans-serif; -webkit-font-smoothing: antialiased; color: #1d1d1f; background: #fbfbfc; padding: 34px 0 44px; }
.ap-page { width: var(--ap-page-w, 680px); margin: 0 auto; }
.ap-head { padding: 0 30px 8px; }
.ap-head .kicker { font-size: 12px; letter-spacing: .09em; text-transform: uppercase; color: #a2a2a8; font-weight: 700; }
.ap-head .title { font-size: 24px; font-weight: 700; margin-top: 5px; color: #111114; }
.ap-head .sub { font-size: 14.5px; color: #86868b; margin-top: 4px; }
.ap-seclabel { font-size: 12px; letter-spacing: .07em; text-transform: uppercase; color: #b0b0b6; font-weight: 700; margin: 30px 30px 12px; }
.ap-only { padding: 24px 0; background: #fff; }
.ap-seclabel span { color: #6e6e73; }
/* chatbot */
.ap-chatwrap { display: flex; justify-content: center; }
.ap-chatbot { width: 440px; background: #e7e7e9; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,.10); overflow: hidden; }
.ap-cb-head { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px 12px; }
.ap-cb-logo { font-size: 17px; font-weight: 800; color: #1d1d1f; line-height: 1; }
.ap-cb-logo img { display:block; height: 24px; width:auto; }
.ap-cb-logo small { display:block; font-size: 11px; font-weight: 600; color:#8a8a8e; letter-spacing:.16em; margin-top:3px; }
.ap-cb-head-right { display: flex; align-items: center; gap: 12px; }
.ap-cb-newchat { background: #fff; border: 1px solid #dcdce0; border-radius: 20px; padding: 7px 13px; font-size: 13px; font-weight: 600; color: #2b2b2e; }
.ap-cb-x { color: #86868b; font-size: 20px; line-height: 1; }
.ap-cb-tabs { display: flex; padding: 0 18px; border-bottom: 1px solid #d7d7db; }
.ap-cb-tab { flex: 1; text-align: center; padding: 12px 0 13px; font-size: 15px; font-weight: 600; color: #8a8a8e; }
.ap-cb-tab.active { color: #0f9d8f; box-shadow: inset 0 -2.5px 0 #14b8a6; }
.ap-cb-body { padding: 18px; }
.ap-cb-user { background: #f4f4f6; border-radius: 16px; padding: 12px 16px; font-size: 15px; color: #2b2b2e; margin-bottom: 16px; }
.ap-cb-asst { font-size: 15px; color: #1d1d1f; line-height: 1.5; margin-bottom: 14px; }
.ap-carousel-wrap { position: relative; }
.ap-carousel { display: flex; gap: 14px; overflow: hidden; }
.ap-card { width: 190px; flex: none; background: #fff; border-radius: 14px; box-shadow: 0 2px 12px rgba(0,0,0,.08); overflow: hidden; }
.ap-card-img { height: 180px; background: #f2f2f4 center/cover no-repeat; position: relative; }
.ap-brand-tag { position: absolute; left: 10px; bottom: 10px; background: rgba(255,255,255,.88); color: #333; font-size: 11.5px; padding: 4px 9px; border-radius: 7px; font-weight: 600; }
.ap-card-body { padding: 12px 14px 14px; }
.ap-card-title { font-weight: 700; font-size: 14.5px; color: #1d1d1f; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 38px; }
.ap-card-price { font-weight: 700; font-size: 16px; color: #1d1d1f; margin-top: 8px; }
.ap-next-btn { position: absolute; right: -6px; top: 32%; width: 38px; height: 38px; border-radius: 50%; background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,.2); display: flex; align-items: center; justify-content: center; font-size: 17px; color: #444; }
.ap-carousel-sponso { margin: 9px 2px 0; font-size: 11.5px; color: #9a9aa0; letter-spacing: .02em; }
.ap-cb-li { font-size: 15px; color: #1d1d1f; line-height: 1.5; margin: 0 0 8px 2px; padding-left: 16px; position: relative; }
.ap-cb-li::before { content: "•"; position: absolute; left: 2px; color: #6e6e73; }
.ap-cb-fb { display: flex; gap: 16px; margin: 16px 2px 4px; color: #9a9aa0; font-size: 16px; }
.ap-cb-sugg { display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }
.ap-sugg { position: relative; background: #f4f4f6; border-radius: 14px; padding: 13px 16px; font-size: 14.5px; color: #2b2b2e; line-height: 1.4; }
.ap-sugg.sponso { padding-right: 44px; }
.ap-sugg .ad { position: absolute; right: 12px; bottom: 10px; background: #e2e2e5; color: #8a8a8e; font-size: 11px; padding: 2px 8px; border-radius: 9px; font-weight: 600; }
.ap-cb-input { display: flex; align-items: center; gap: 10px; margin-top: 18px; }
.ap-cb-field { flex: 1; background: #fff; border-radius: 22px; padding: 13px 18px; font-size: 14.5px; color: #a0a0a5; }
.ap-cb-send { width: 42px; height: 42px; border-radius: 50%; background: #d9d9dd; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 18px; flex: none; }
.ap-cb-foot { text-align: center; font-size: 12px; color: #9a9aa0; margin-top: 14px; }
/* variante "publisher" : widget de chatbot intégré à un média */
.ap-ctx { width: 440px; margin: 0 auto 11px; font-size: 11.5px; color: #a2a2a8; line-height: 1.4; }
.ap-ctx b { color: #6e6e73; font-weight: 700; }
.ap-chatbot.pub .ap-cb-head { justify-content: flex-end; padding: 14px 16px 0; }
.ap-cb-publogo { text-align: center; padding: 12px 0 24px; }
.ap-cb-publogo img { height: 34px; width: auto; display: inline-block; }
.ap-chatbot.pub .ap-cb-body { padding: 0 18px 18px; }
.ap-cb-suggintro { font-size: 14.5px; font-weight: 600; color: #2b2b2e; margin: 20px 0 11px; }
.ap-chatbot.pub .ap-sugg { background: #fff; padding-right: 38px; }
.ap-chatbot.pub .ap-sugg .chev { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); color: #9a9aa0; font-size: 15px; }
.ap-chatbot.pub .ap-sugg.sponso { padding-right: 76px; }
.ap-chatbot.pub .ap-sugg.sponso .ad { right: 34px; bottom: auto; top: 50%; transform: translateY(-50%); }
.ap-chatbot.pub .ap-cb-input { position: relative; }
.ap-chatbot.pub .ap-cb-field { border: 1.5px solid #6b5cff; padding-right: 48px; }
.ap-chatbot.pub .ap-cb-send { position: absolute; right: 5px; top: 50%; transform: translateY(-50%); width: 32px; height: 32px; background: #fff; border: 1px solid #e2e2e5; color: #6e6e73; font-size: 15px; }
/* vue "en contexte" : capture de la page du média + widget incrusté */
.ap-ctxshot { position: relative; margin: 0 auto; }
.ap-ctxshot > img { width: 100%; display: block; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,.13); }
.ap-ctxshot-cap { font-size: 12.5px; color: #86868b; text-align: center; margin-top: 11px; line-height: 1.45; }
.ap-ctxshot-w { position: absolute; overflow: hidden; border-radius: 14px; background: #fff; box-shadow: 0 6px 24px rgba(0,0,0,.18); }
.ap-ctxshot-s { transform-origin: top left; }
.ap-ctxshot .ap-chatbot { width: 440px; height: 100%; border-radius: 14px; box-shadow: none; display: flex; flex-direction: column; }
.ap-ctxshot .ap-cb-body { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.ap-ctxshot .ap-carousel-wrap { flex: none; overflow: hidden; }
.ap-ctxshot .ap-cb-sugg { flex: 1; min-height: 0; overflow: hidden; }
.ap-ctxshot .ap-cb-input, .ap-ctxshot .ap-cb-foot { flex: none; }
.ap-ctxshot.compact .ap-cb-fb, .ap-ctxshot.compact .ap-cb-suggintro, .ap-ctxshot.compact .ap-sugg:not(.sponso) { display: none; }
.ap-ctxshot.compact .ap-card-img { height: 114px; }
.ap-ctxshot.compact .ap-card-title { min-height: 0; }
/* generaliste */
.ap-searchwrap { display: flex; justify-content: center; }
.ap-search { width: 640px; background: #fff; border-radius: 16px; box-shadow: 0 8px 34px rgba(0,0,0,.09); padding: 22px 28px 26px; }
.ap-s-top { display: flex; align-items: center; gap: 14px; }
.ap-s-mark { font-size: 22px; font-weight: 800; color: #1d1d1f; flex: none; }
.ap-s-bar { flex: 1; display: flex; align-items: center; border: 1px solid #dcdce0; border-radius: 24px; padding: 10px 16px; box-shadow: 0 1px 4px rgba(0,0,0,.05); }
.ap-s-bar .q { flex: 1; font-size: 15px; color: #2b2b2e; }
.ap-s-bar .mag { color: #1a56db; font-size: 16px; }
.ap-s-tabs { display: flex; gap: 10px; margin: 16px 0 20px; }
.ap-s-tab { font-size: 13.5px; color: #5f6368; padding: 6px 14px; border: 1px solid #e3e3e6; border-radius: 18px; }
.ap-s-tab.active { color: #1a56db; border-color: #b9cdfa; background: #f2f6ff; font-weight: 600; }
.ap-s-h { font-size: 16px; font-weight: 700; color: #1d1d1f; margin: 14px 0 8px; }
.ap-s-li { font-size: 14.5px; color: #303034; line-height: 1.5; margin: 6px 0 6px 4px; padding-left: 16px; position: relative; }
.ap-s-li:before { content: "\\2022"; position: absolute; left: 0; color: #8a8a8e; }
.ap-s-icons { display: flex; gap: 16px; color: #9a9aa0; font-size: 15px; margin: 16px 2px; }
.ap-s-divider { height: 1px; background: #eeeef0; margin: 4px 0 18px; }
.ap-textad-head { display: flex; align-items: center; gap: 11px; }
.ap-favicon { width: 30px; height: 30px; border-radius: 50%; background: #eef0f2 center/cover no-repeat; flex: none; display:flex; align-items:center; justify-content:center; font-size:14px; color:#8a8a8e; font-weight:700; }
.ap-dom { font-size: 14px; color: #202124; }
.ap-dom .ann { color: #5f6368; }
.ap-headline { display: block; margin-top: 8px; color: #1a56db; font-size: 19px; line-height: 1.34; text-decoration: none; font-weight: 400; }
.ap-headline b { font-weight: 700; }
.ap-s-more-h { font-size: 13.5px; font-weight: 700; color: #5f6368; margin: 24px 0 12px; }
.ap-s-more { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.ap-s-more .c { background: #f1f3f5; border-radius: 12px; padding: 13px 15px; font-size: 13.5px; color: #303034; line-height: 1.35; display: flex; gap: 9px; align-items: flex-start; }
.ap-s-more .c .ic { color: #1a56db; font-weight: 700; flex: none; }
.ap-s-qc { margin-top: 18px; background: #eef1fb; border-radius: 22px; padding: 14px 18px; font-size: 14.5px; color: #9aa1b5; }
.ap-s-foot { text-align: center; font-size: 12px; color: #a0a0a5; margin-top: 16px; }

/* ---- ChatGPT Ads (chat card + product ad) ---- */
.ap-gptwrap { display: flex; justify-content: center; }
.ap-gpt { width: 640px; background: #fff; border: 1px solid #e6e6e8; border-radius: 18px; box-shadow: 0 8px 34px rgba(0,0,0,.07); padding: 22px 24px 20px; }
.ap-gpt + .ap-gpt { margin-top: 18px; }
.ap-gpt-sublabel { font-size: 12px; letter-spacing: .07em; text-transform: uppercase; color: #b0b0b6; font-weight: 700; margin: 22px 30px 10px; }
.ap-gpt-sublabel span { color: #6e6e73; }
.ap-gpt-user { display: flex; justify-content: flex-end; margin-bottom: 18px; }
.ap-gpt-user span { background: #f4f4f4; border-radius: 18px; padding: 11px 16px; font-size: 14.5px; color: #0d0d0d; line-height: 1.45; max-width: 76%; }
.ap-gpt-row { display: flex; gap: 13px; }
.ap-gpt-avatar { width: 30px; height: 30px; border-radius: 50%; border: 1px solid #e6e6e8; flex: none; display: flex; align-items: center; justify-content: center; }
.ap-gpt-avatar svg { width: 17px; height: 17px; }
.ap-gpt-msg { flex: 1; font-size: 14.5px; color: #0d0d0d; line-height: 1.55; }
.ap-gpt-li { margin: 7px 0 7px 18px; position: relative; }
.ap-gpt-li:before { content: "\\2022"; position: absolute; left: -14px; color: #0d0d0d; }
.ap-gpt-li b { font-weight: 700; }
.ap-gpt-outro { margin-top: 12px; }
.ap-gpt-divider { height: 1px; background: #ececee; margin: 20px 0 12px; }
.ap-gpt-sponso { font-size: 13px; color: #6e6e73; margin-bottom: 9px; }
.ap-gpt-ad { border: 1px solid #e6e6e8; border-radius: 14px; padding: 13px; display: flex; gap: 15px; align-items: center; }
.ap-gpt-ad-img { width: 96px; height: 96px; flex: none; border-radius: 10px; background: #f7f7f8 center/cover no-repeat; }
.ap-gpt-ad-body { flex: 1; min-width: 0; }
.ap-gpt-adv { display: flex; align-items: center; gap: 8px; font-size: 13.5px; color: #3c3c40; margin-bottom: 6px; }
.ap-gpt-adv .pill { width: 22px; height: 22px; border-radius: 6px; background: #fff center/76% no-repeat; border: 1px solid #ececef; flex: none; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; color: #3c3c40; }
.ap-gpt-ad-title { font-size: 15.5px; font-weight: 700; color: #0d0d0d; line-height: 1.3; }
.ap-gpt-ad-desc { font-size: 14px; color: #4a4a4e; margin-top: 5px; line-height: 1.4; }
.ap-gpt-ad-price { font-size: 16.5px; font-weight: 700; color: #0d8a6a; margin-top: 6px; }
.ap-gpt-ad-adv2 { font-size: 13.5px; color: #6e6e73; margin-top: 5px; }
.ap-gpt-cta { display: inline-block; margin-top: 11px; border: 1px solid #cfd6d3; border-radius: 9px; padding: 8px 15px; font-size: 13.5px; font-weight: 700; color: #0d8a6a; }
.ap-gpt-ad.split .ap-gpt-cta { margin-top: 0; }
.ap-gpt-ad.split .ap-gpt-cta-col { flex: none; padding-left: 10px; }
.ap-gpt-composer { display: flex; align-items: center; gap: 11px; border: 1px solid #e6e6e8; border-radius: 24px; padding: 12px 14px; margin-top: 18px; }
.ap-gpt-composer .clip { color: #8a8a8e; font-size: 15px; }
.ap-gpt-composer .ph { flex: 1; font-size: 14.5px; color: #a0a0a5; }
.ap-gpt-composer .send { width: 30px; height: 30px; border-radius: 50%; background: #e8e8ea; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 15px; flex: none; }
"""

PREMIUM_CSS = """
.ap-root { background: #f6f3ec; }
.ap-head { padding: 32px 34px 14px; }
.ap-head .kicker { color: #a2916c; letter-spacing: .28em; }
.ap-head .title { font-family: "Didot","Bodoni 72",Georgia,"Times New Roman",serif; font-weight: 500; font-size: 30px; letter-spacing: .01em; }
.ap-head .sub { color: #8c8474; font-style: italic; }
.ap-wordmark { font-family: "Futura","Century Gothic",Helvetica,Arial,sans-serif; font-size: 13px; letter-spacing: .34em; color: #1d1d1f; margin-bottom: 14px; }
.ap-goldrule { height: 1px; background: linear-gradient(90deg,#d8c9a5,#efe7d5); margin: 4px 34px 0; }
.ap-seclabel { color: #b7ac8f; }
.ap-seclabel span { color: #8f8262; }
"""

OPENAI_MARK = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#0d0d0d" d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"/></svg>"""

STRINGS = {
    "fr": {
        "kicker": "Aperçu contenu sponsorisé · Lemrock",
        "title": "{brand} dans les IA conversationnelles",
        "sub": "Voici à quoi ressembleraient vos {n} formats publicitaires, en conditions réelles.",
        "sec_specialized": "Dans une IA spécialisée {vertical} — <span>carrousel produit + question sponsorisée</span>",
        "sec_generalist": "Dans une IA généraliste — <span>texte ads</span>",
        "new_chat": "+ Nouveau chat",
        "tab_chat": "Chat", "tab_shopping": "Shopping",
        "input_ph": "Écrivez un message…",
        "cb_foot": "Ce contenu est généré par IA, il peut contenir des erreurs.",
        "s_tabs": ["Tous", "Chat IA", "Images", "Vidéos", "Actualités", "Shopping"],
        "ad_label": "Annonce",
        "more_h": "Pour aller plus loin",
        "followup_ph": "Question complémentaire",
        "s_foot": "Les réponses générées peuvent contenir des erreurs.",
        "sec_chatgpt": "Dans ChatGPT — <span>chat card + product ad</span>",
        "gpt_chatcard": "Format 1 — <span>chat card</span>",
        "gpt_productad": "Format 2 — <span>product ad</span>",
        "gpt_sponso": "Sponsorisé",
        "gpt_ph": "Envoyer un message à ChatGPT…",
        "gpt_cta_card": "Découvrir",
        "gpt_cta_prod": "Voir le produit",
    },
    "en": {
        "kicker": "Sponsored content preview · Lemrock",
        "title": "{brand} in conversational AI",
        "sub": "Here is what your {n} ad formats would look like in real conditions.",
        "sec_specialized": "In a specialist {vertical} AI — <span>product carousel + sponsored question</span>",
        "sec_generalist": "In a general-purpose AI — <span>text ads</span>",
        "new_chat": "+ New chat",
        "tab_chat": "Chat", "tab_shopping": "Shopping",
        "input_ph": "Write a message…",
        "cb_foot": "This content is AI-generated and may contain errors.",
        "s_tabs": ["All", "AI Chat", "Images", "Videos", "News", "Shopping"],
        "ad_label": "Sponsored",
        "more_h": "Explore further",
        "followup_ph": "Ask a follow-up",
        "s_foot": "Generated answers may contain errors.",
        "sec_chatgpt": "In ChatGPT — <span>chat card + product ad</span>",
        "gpt_chatcard": "Format 1 — <span>chat card</span>",
        "gpt_productad": "Format 2 — <span>product ad</span>",
        "gpt_sponso": "Sponsored",
        "gpt_ph": "Message ChatGPT…",
        "gpt_cta_card": "Learn more",
        "gpt_cta_prod": "View product",
    },
}

def _img_size(path):
    """Dimensions (w, h) d'un PNG, JPEG ou WEBP, sans dépendance externe."""
    with open(path, "rb") as f:
        d = f.read(64000)
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(d[16:20], "big"), int.from_bytes(d[20:24], "big")
    if d[:4] == b"RIFF" and d[8:12] == b"WEBP":
        if d[12:16] == b"VP8X":
            return (int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1)
        if d[12:16] == b"VP8 ":
            return int.from_bytes(d[26:28], "little") & 0x3fff, int.from_bytes(d[28:30], "little") & 0x3fff
        if d[12:16] == b"VP8L":
            b = int.from_bytes(d[21:25], "little")
            return (b & 0x3fff) + 1, ((b >> 14) & 0x3fff) + 1
    i = 2
    while i < len(d) - 9:                      # JPEG : on cherche un marqueur SOF
        if d[i] != 0xFF:
            i += 1
            continue
        m = d[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            return int.from_bytes(d[i + 7:i + 9], "big"), int.from_bytes(d[i + 5:i + 7], "big")
        i += 2 + int.from_bytes(d[i + 2:i + 4], "big")
    raise ValueError("format d'image non reconnu : " + path)


def _gpt_answer(g, t):
    """Bloc réponse ChatGPT : intro + puces (lead-in en gras) + conclusion."""
    lis = ""
    for it in g.get("answer_bullets", []):
        if isinstance(it, dict):
            lis += f'<div class="ap-gpt-li"><b>{esc(it["b"])}</b> : {esc(it["t"])}</div>'
        else:
            lis += f'<div class="ap-gpt-li">{esc(it)}</div>'
    outro = f'<div class="ap-gpt-outro">{esc(g["answer_outro"])}</div>' if g.get("answer_outro") else ""
    return f"""
      <div class="ap-gpt-user"><span>{esc(g["user_query"])}</span></div>
      <div class="ap-gpt-row">
        <div class="ap-gpt-avatar">{OPENAI_MARK}</div>
        <div class="ap-gpt-msg">
          <div>{esc(g["answer_intro"])}</div>
          {lis}
          {outro}
        </div>
      </div>
      <div class="ap-gpt-divider"></div>
      <div class="ap-gpt-sponso">{esc(t["gpt_sponso"])}</div>"""


def _gpt_pill(b):
    """Pastille annonceur du bloc sponsorisé (logo de marque, sinon initiale)."""
    if b.get("logo"):
        return f"""<span class="pill" style="background-image:url('{data_uri(b["logo"])}')"></span>"""
    return f'<span class="pill">{esc(b["initial"])}</span>'


def build_chatgpt(cfg, b, t):
    """Les 2 formats ChatGPT Ads, chacun dans une interface ChatGPT complète :
    - chat card : image + titre + courte description + lien vers la landing page
    - product ad : annonce issue d'un flux catalogue (image + prix + lien fiche produit)"""
    g = cfg.get("chatgpt")
    if not g:
        return ""
    answer = _gpt_answer(g, t)
    pill = _gpt_pill(b)
    composer = (f'<div class="ap-gpt-composer"><span class="clip">&#128206;</span>'
                f'<span class="ph">{esc(t["gpt_ph"])}</span><span class="send">&uarr;</span></div>')

    cc = g["chat_card"]
    chat_card = f"""
    <div class="ap-gpt-sublabel">{t["gpt_chatcard"]}</div>
    <div class="ap-gptwrap"><div class="ap-gpt">
      {answer}
      <div class="ap-gpt-ad">
        <div class="ap-gpt-ad-img" style="background-image:url('{data_uri(cc["image"])}')"></div>
        <div class="ap-gpt-ad-body">
          <div class="ap-gpt-adv">{pill} {esc(cc.get("advertiser", b["name"]))}</div>
          <div class="ap-gpt-ad-title">{esc(cc["title"])}</div>
          <div class="ap-gpt-ad-desc">{esc(cc["desc"])}</div>
          <div class="ap-gpt-cta">{esc(cc.get("cta", t["gpt_cta_card"]))}</div>
        </div>
      </div>
      {composer}
    </div></div>"""

    pa = g["product_ad"]
    product_ad = f"""
    <div class="ap-gpt-sublabel">{t["gpt_productad"]}</div>
    <div class="ap-gptwrap"><div class="ap-gpt">
      {answer}
      <div class="ap-gpt-ad split">
        <div class="ap-gpt-ad-img" style="background-image:url('{data_uri(pa["image"])}')"></div>
        <div class="ap-gpt-ad-body">
          <div class="ap-gpt-ad-title">{esc(pa["title"])}</div>
          <div class="ap-gpt-ad-price">{esc(pa["price"])}</div>
          <div class="ap-gpt-ad-adv2">{esc(pa.get("advertiser", b["name"]))}</div>
        </div>
        <div class="ap-gpt-cta-col"><div class="ap-gpt-cta">{esc(pa.get("cta", t["gpt_cta_prod"]))}</div></div>
      </div>
      {composer}
    </div></div>"""

    return f'<div class="ap-seclabel">{t["sec_chatgpt"]}</div>{chat_card}{product_ad}'


def build_context_shot(cfg, chatbot_html):
    """Capture de la page du média avec le widget de chatbot incrusté à sa place réelle."""
    cs = cfg.get("context_shot")
    if not cs:
        return ""
    from struct import unpack
    W = cs.get("width", 1000)
    iw, ih = _img_size(cs["image"])
    k = W / iw
    x0, y0, x1, y1 = cs["rect"]
    left, top = x0 * k, y0 * k
    bw, bh = (x1 - x0) * k, (y1 - y0) * k
    sc = bw / 440.0
    inner_h = bh / sc
    cap = f'<div class="ap-ctxshot-cap">{esc(cs["caption"])}</div>' if cs.get("caption") else ""
    compact = " compact" if cs.get("compact", True) else ""
    page_w = cfg.get("page_width", 680)
    return f"""
  <div class="ap-ctxshot{compact}" style="width:{W}px;margin-left:{(page_w - W) / 2:.0f}px">
    <img src="{data_uri(cs['image'])}" alt="">
    <div class="ap-ctxshot-w" style="left:{left:.1f}px;top:{top:.1f}px;width:{bw:.1f}px;height:{bh:.1f}px">
      <div class="ap-ctxshot-s" style="width:440px;height:{inner_h:.1f}px;transform:scale({sc:.4f})">{chatbot_html}</div>
    </div>
  </div>
  {cap}"""


def build(cfg):
    b = cfg["brand"]
    lang = cfg.get("lang", "fr")
    t = STRINGS.get(lang, STRINGS["fr"])
    premium = cfg.get("theme") == "premium"
    fit = cfg.get("image_fit", "cover")
    img_extra = "background-size:contain;background-color:#fff;" if fit == "contain" else ""
    cards = ""
    for p in cfg.get("products") or []:
        cards += f"""
          <div class="ap-card">
            <div class="ap-card-img" style="background-image:url('{data_uri(p['image'])}');{img_extra}"><div class="ap-brand-tag">{esc(p.get('brand', b['name']))}</div></div>
            <div class="ap-card-body"><div class="ap-card-title">{esc(p['title'])}</div><div class="ap-card-price">{esc(p['price'])}</div></div>
          </div>"""
    pub = cfg.get("chatbot_style") == "publisher"
    chev = '<span class="chev">&rsaquo;</span>' if pub else ""
    suggs = ""
    for q in cfg["suggested"]:
        suggs += f'<div class="ap-sugg">{esc(q)}{chev}</div>'
    if cfg.get("sponsored_q"):   # optionnel : un aperçu « carrousel seul » n'a pas de question sponsorisée
        suggs += f'<div class="ap-sugg sponso">{esc(cfg["sponsored_q"])}<span class="ad">Ad</span>{chev}</div>'
    # Logo de la marque dans la pastille du texte ads (sinon initiale en secours)
    if b.get("logo"):
        favicon = f'<div class="ap-favicon" style="background-image:url(\'{data_uri(b["logo"])}\'); background-size:76%; background-color:#fff; border:1px solid #ececef"></div>'
    else:
        favicon = f'<div class="ap-favicon">{esc(b["initial"])}</div>'
    bullets = "".join(f'<div class="ap-s-li">{esc(x)}</div>' for x in cfg["answer_bullets"])
    more = "".join(f'<div class="c"><span class="ic">&#8635;</span> {esc(x)}</div>' for x in cfg["followups"])

    # onglets du moteur généraliste : le 2e (Chat IA) est actif, avec l'icône de rafraîchissement
    stabs = ""
    for i, lbl in enumerate(t["s_tabs"]):
        if i == 1:
            stabs += f'<div class="ap-s-tab active">&#8635; {esc(lbl)}</div>'
        else:
            stabs += f'<div class="ap-s-tab">{esc(lbl)}</div>'
    gen_logo = cfg.get("generalist_ai_logo")
    gen_mark = (f'<img src="{data_uri(gen_logo)}" alt="{esc(cfg["generalist_ai_name"])}" style="display:block;height:34px;width:auto">'
                if gen_logo else esc(cfg["generalist_ai_name"]))
    ai_logo = cfg.get("specialized_ai_logo")
    ai_name_html = (f'<img src="{data_uri(ai_logo)}" alt="{esc(cfg["specialized_ai_name"])}">'
                    if ai_logo else esc(cfg["specialized_ai_name"]))
    sep = " : " if lang == "fr" else ": "   # pas d'espace avant le deux-points en anglais

    # en-tête du chatbot : bandeau média (logo centré + croix) ou en-tête générique
    if pub:
        cb_head = (f'<div class="ap-cb-head"><div class="ap-cb-x">&times;</div></div>'
                   f'<div class="ap-cb-publogo">{ai_name_html}</div>')
    else:
        cb_head = (f'<div class="ap-cb-head">'
                   f'<div class="ap-cb-logo">{ai_name_html}<small>{esc(cfg["specialized_ai_sub"])}</small></div>'
                   f'<div class="ap-cb-head-right"><div class="ap-cb-newchat">{esc(t["new_chat"])}</div>'
                   f'<div class="ap-cb-x">&times;</div></div></div>'
                   f'<div class="ap-cb-tabs"><div class="ap-cb-tab active">{esc(t["tab_chat"])}</div>'
                   f'<div class="ap-cb-tab">{esc(t["tab_shopping"])}</div></div>')
    sugg_intro = f'<div class="ap-cb-suggintro">{esc(cfg["sugg_intro"])}</div>' if cfg.get("sugg_intro") else ""
    # mention de transparence sous le carrousel produit
    car_sponso = (f'<div class="ap-carousel-sponso">{esc(cfg["carousel_sponso"])}</div>'
                  if cfg.get("carousel_sponso") else "")
    # réponse texte en puces (optionnel, utile quand il n'y a pas de carrousel)
    asst_bullets = "".join(f'<div class="ap-cb-li">{esc(x)}</div>' for x in cfg.get("assistant_bullets", []))
    carousel = (f'<div class="ap-carousel-wrap"><div class="ap-carousel">{cards}</div><div class="ap-next-btn">&rarr;</div></div>'
                if cards else "")
    ac = cfg.get("article_context")
    ctx = f'<div class="ap-ctx"><b>{esc(ac["source"])}</b> &middot; {esc(ac["title"])}</div>' if ac else ""
    sec_spe = cfg.get("sec_specialized_label") or t["sec_specialized"].format(vertical=esc(cfg["vertical_label"]))
    sec_gen = cfg.get("sec_generalist_label") or t["sec_generalist"]

    chatbot_html = f"""<div class="ap-chatbot{' pub' if pub else ''}">
    {cb_head}
    <div class="ap-cb-body">
      <div class="ap-cb-user">{esc(cfg['user_query_specialized'])}</div>
      <div class="ap-cb-asst">{esc(cfg['assistant_intro'])}</div>
      {asst_bullets}
      {carousel}
      {car_sponso}
      <div class="ap-cb-fb">&#128077; &#128078;</div>
      {sugg_intro}
      <div class="ap-cb-sugg">{suggs}</div>
      <div class="ap-cb-input"><div class="ap-cb-field">{esc(t['input_ph'])}</div><div class="ap-cb-send">&uarr;</div></div>
      <div class="ap-cb-foot">&#9432; {esc(t['cb_foot'])}</div>
    </div>
  </div>"""
    context_shot = build_context_shot(cfg, chatbot_html)
    sec_zoom = (f'<div class="ap-seclabel">{cfg["sec_zoom_label"]}</div>'
                if context_shot and cfg.get("sec_zoom_label") else "")
    gpt_section = build_chatgpt(cfg, b, t)
    n_formats = 5 if cfg.get("chatgpt") else 3
    wordmark = f'<div class="ap-wordmark">{esc(b["name"]).upper()}</div>' if premium else ""
    goldrule = '<div class="ap-goldrule"></div>' if premium else ""
    page_w = cfg.get("page_width", 680)
    search_html = f"""  <div class="ap-searchwrap"><div class="ap-search">
    <div class="ap-s-top">
      <div class="ap-s-mark">{gen_mark}</div>
      <div class="ap-s-bar"><div class="q">{esc(cfg['user_query_generalist'])}</div><div class="mag">&#9906;</div></div>
    </div>
    <div class="ap-s-tabs">{stabs}</div>
    <div class="ap-s-h">{esc(cfg['answer_title'])}</div>
    {bullets}
    <div class="ap-s-icons">&#128203; &#128077; &#128078;</div>
    <div class="ap-s-divider"></div>
    <div class="ap-textad-head">{favicon}<div class="ap-dom">{esc(b['domain'])} <span class="ann">• {esc(t['ad_label'])}</span></div></div>
    <a class="ap-headline"><b>{esc(b['name'])}</b>{esc(sep)}{esc(cfg['textad_phrase'])}</a>
    <div class="ap-s-more-h">{esc(t['more_h'])}</div>
    <div class="ap-s-more">{more}</div>
    <div class="ap-s-qc">{esc(t['followup_ph'])}</div>
    <div class="ap-s-foot">{esc(t['s_foot'])}</div>
  </div></div>
"""
    content = f"""
<div class="ap-root" style="--ap-page-w:{page_w}px"><div class="ap-page">
  <div class="ap-head">
    {wordmark}<div class="kicker">{t['kicker']}</div>
    <div class="title">{esc(cfg['head_title']) if cfg.get('head_title') else t['title'].format(brand=esc(b['name']))}</div>
    <div class="sub">{esc(cfg['head_sub']) if cfg.get('head_sub') else t['sub'].format(n=n_formats)}</div>
  </div>
  {goldrule}

  <div class="ap-seclabel">{sec_spe}</div>
  {ctx}
  {context_shot}
  {sec_zoom}
  <div class="ap-chatwrap">{chatbot_html}</div>

  <div class="ap-seclabel">{sec_gen}</div>
  {search_html}

  {gpt_section}
</div></div>
"""
    # « only » : un seul format, sans en-tête ni libellés (visuel à poser dans un deck)
    only = cfg.get("only")
    if only:
        block_html = {"specialized": f'<div class="ap-chatwrap">{chatbot_html}</div>',
                      "generalist": search_html,
                      "chatgpt": gpt_section}[only]
        content = f'<div class="ap-root ap-only" style="--ap-page-w:{page_w}px"><div class="ap-page">{block_html}</div></div>'
    inner = f"<style>{CSS}{PREMIUM_CSS if premium else ''}</style>\n{content}"
    full = f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'></head><body style='margin:0'>{inner}</body></html>"
    return inner, full

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    outdir = os.path.dirname(os.path.abspath(sys.argv[1]))
    os.chdir(outdir)  # images référencées relativement au fichier config
    inner, full = build(cfg)
    open(os.path.join(outdir, "widget_inner.html"), "w").write(inner)
    open(os.path.join(outdir, "preview_full.html"), "w").write(full)
    print("written widget_inner.html + preview_full.html")
