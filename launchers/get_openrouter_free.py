import urllib.request
import json

url = "https://openrouter.ai/api/v1/models"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        
    models = data.get("data", [])
    free_models = []
    for m in models:
        m_id = m.get("id", "")
        pricing = m.get("pricing", {})
        prompt_cost = float(pricing.get("prompt", 1.0) or 0.0)
        completion_cost = float(pricing.get("completion", 1.0) or 0.0)
        if ":free" in m_id or (prompt_cost == 0.0 and completion_cost == 0.0):
            free_models.append((m_id, m.get("name", m_id)))
            
    print(f"Total live free models on OpenRouter right now: {len(free_models)}\n")
    for mid, name in sorted(free_models):
        print(f"- {mid} ({name})")
        
    # Also write directly to hermes cache
    cache_path = r"C:\Users\Imran\AppData\Local\hermes\provider_models_cache.json"
    clean_ids = [mid for mid, _ in sorted(free_models)]
    cache_obj = {
        "openrouter": {
            "fp": "openrouter_live_free",
            "at": 9999999999,
            "models": clean_ids
        }
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_obj, f, indent=2)
    print(f"\nUpdated Hermes cache ({cache_path}) with the {len(clean_ids)} live verified free models.")
    
except Exception as e:
    print(f"Error fetching OpenRouter models: {e}")
