import requests
from config import cfg

GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
HEADERS = {"Authorization": f"Bearer {cfg.PH_TOKEN}"}

# Забираем пачку свежих постов (топ Product Hunt)
QUERY = """
query FetchPosts($per: Int!) {
  posts(order: RANKING, first: $per) {
    edges {
      node {
        id
        name
        tagline
        description
        votesCount
        commentsCount
        website
        slug
        topics { edges { node { name } } }
      }
    }
  }
}
"""

def fetch_candidates(limit: int = 40) -> list[dict]:
    r = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={"query": QUERY, "variables": {"per": limit}},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    edges = data["data"]["posts"]["edges"]
    return [e["node"] for e in edges]