import json
import os
from datetime import datetime

class CostController:
    """
    Tracks token usage and estimated costs for LLM requests.
    Supports Gemini and OpenAI price estimation.
    """
    STATS_DIR = "stats"
    COST_FILE = os.path.join(STATS_DIR, "costs.json")

    # Pricing per 1M tokens (Approximate)
    PRICING = {
        "gemini-1.5-pro": {"input": 3.5, "output": 10.5},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.3},
        "gpt-4o": {"input": 5.0, "output": 15.0},
        "claude-3-5-sonnet": {"input": 3.0, "output": 15.0}
    }

    def __init__(self):
        if not os.path.exists(self.STATS_DIR):
            os.makedirs(self.STATS_DIR)
        self.current_session_cost = 0.0
        self.current_session_tokens = 0

    def track_request(self, model_name: str, input_tokens: int, output_tokens: int):
        """
        Calculates and logs the cost of a single request.
        """
        # Simple lookup for base model families
        pricing_key = next((k for k in self.PRICING if k in model_name), "gemini-1.5-flash")
        prices = self.PRICING[pricing_key]

        cost = (input_tokens / 1_000_000 * prices["input"]) + (output_tokens / 1_000_000 * prices["output"])
        
        self.current_session_cost += cost
        self.current_session_tokens += (input_tokens + output_tokens)

        self._save_to_history(model_name, input_tokens, output_tokens, cost)
        return cost

    def _save_to_history(self, model, input_t, output_t, cost):
        history = []
        if os.path.exists(self.COST_FILE):
            with open(self.COST_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except:
                    history = []

        history.append({
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_t,
            "output_tokens": output_t,
            "cost_usd": round(cost, 6)
        })

        with open(self.COST_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def get_total_historical_cost(self):
        if not os.path.exists(self.COST_FILE):
            return 0.0
        with open(self.COST_FILE, "r") as f:
            history = json.load(f)
            return sum(item["cost_usd"] for item in history)
