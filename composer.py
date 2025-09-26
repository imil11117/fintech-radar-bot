import re

def _pro_notes(post: dict):
    text = f"{post.get('name','')} {post.get('tagline','')} {post.get('description','')}".lower()
    payment = any(k in text for k in ["payment","checkout","acquiring","pay in","card","pos","invoice","billing"])
    kyc     = any(k in text for k in ["kyc","aml","onboarding","identity","fraud","verification"])
    smb     = any(k in text for k in ["smb","invoic","accounting","bookkeep","erp","cash flow"])
    crypto  = any(k in text for k in ["crypto","defi","web3","wallet","token","onchain"])

    if payment:
        comp, integ, monet, risk, pilot = (
            "PCI DSS; возможна лицензия MSB/MTL (US)",
            "Stripe/Adyen/Rapyd; Plaid/Open Banking",
            "take-rate 10–50 bps",
            "chargebacks, fraud",
            "e-commerce/маркетплейсы (MX)",
        )
    elif kyc:
        comp, integ, monet, risk, pilot = (
            "AML/KYC, санкционные списки; хранение персональных данных",
            "Trulioo/Sumsub/Persona",
            "per-verification",
            "false positives, просадка конверсии",
            "необанк/BNPL",
        )
    elif smb:
        comp, integ, monet, risk, pilot = (
            "налоговые интеграции (например, CFDI в MX)",
            "QuickBooks/Xero; выгрузки банков",
            "subscription + add-ons",
            "retention/churn",
            "ритейл/HoReCa SME",
        )
    elif crypto:
        comp, integ, monet, risk, pilot = (
            "VASP/Travel Rule; custody/регулирование",
            "Fireblocks/Circle; on/off-ramp",
            "спред/комиссии",
            "регуляторные запреты, волатильность",
            "кошельки/нео-брокеры",
        )
    else:
        comp, integ, monet, risk, pilot = (
            "базовые требования к обработке платежных/персональных данных",
            "REST/Webhooks; аналитика (Amplitude/Mixpanel)",
            "subscription / usage-based",
            "низкая дифференциация",
            "SMB-банкинг/ERP интеграции",
        )
    return comp, integ, monet, risk, pilot

def compose_message(post: dict) -> str:
    name = (post.get("name") or "").strip()
    tagline = (post.get("tagline") or "").strip()
    desc = (post.get("description") or tagline or "").strip()
    desc = re.sub(r"\s+", " ", desc)
    votes = post.get("votesCount", 0)
    comments = post.get("commentsCount", 0)
    website = post.get("website") or ""
    ph_url = f"https://www.producthunt.com/posts/{post.get('slug','')}"
    comp, integ, monet, risk, pilot = _pro_notes(post)

    why = [
        f"• Killer фича: {tagline or 'фокус на UX/скорость запуска'}",
        "• ICP: SMB / финсерв",
        "• Go-to-market: product-led + партнёрства",
    ]

    body = (
f"🚀 Стартап дня: {name}\n"
f"{tagline}\n\n"
f"Что делает (1–2 строки):\n"
f"{desc}\n\n"
f"Почему это может “выстрелить”:\n"
f"{why[0]}\n{why[1]}\n{why[2]}\n\n"
f"Pro Notes для финтех-практиков:\n"
f"• Комплаенс: {comp}\n"
f"• Интеграции: {integ}\n"
f"• Монетизация: {monet}\n"
f"• Риски: {risk}\n"
f"• Где запускать пилот: {pilot}\n\n"
f"Сигналы интереса:\n"
f"• Product Hunt: {votes} апвоутов · {comments} комментариев\n"
f"• Линки: сайт {website} · Product Hunt {ph_url}\n\n"
f"#fintech #payments #smb #latam"
    )
    return body[:4000]