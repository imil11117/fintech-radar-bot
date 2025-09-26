FINTECH_TOPICS = {"Fintech","Finance","Payments","Crypto","Banking","Insurtech"}

FINTECH_KEYWORDS = [
    "fintech","finance","payments","payment","payroll","banking","bank","card","cards",
    "lending","loan","credit","insurtech","insurance","crypto","defi","wallet","exchange",
    "kyc","aml","onboarding","identity","fraud","accounting","billing","invoice","invoicing",
    "open banking","baas","psd2"
]

def is_fintech(post: dict) -> bool:
    topics = {t["node"]["name"] for t in post.get("topics", {}).get("edges", [])}
    if topics & FINTECH_TOPICS:
        return True
    text = " ".join([
        post.get("name",""), post.get("tagline",""), post.get("description","")
    ]).lower()
    return any(kw in text for kw in FINTECH_KEYWORDS)

def score(post: dict) -> float:
    votes = post.get("votesCount", 0)
    comments = post.get("commentsCount", 0)
    topics = {t["node"]["name"] for t in post.get("topics", {}).get("edges", [])}
    bonus = 10 if (topics & FINTECH_TOPICS) else 0
    return votes + 0.5*comments + bonus