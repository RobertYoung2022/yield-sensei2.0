from typing import List, Dict, Any, Optional, ClassVar
from pydantic import PrivateAttr
from langchain.tools import BaseTool
import requests
import json

class StrategyTool(BaseTool):
    """Tool for discovering and analyzing DeFi yield strategies"""
    name: ClassVar[str] = "strategy_tool"
    description: ClassVar[str] = """
    Use this tool to discover, analyze, and get step-by-step instructions for DeFi yield strategies.
    Supports delta-neutral, leveraged yield, stablecoin farming, and more.
    """
    _defillama_base_url: str = PrivateAttr("https://api.llama.fi")
    _defillama_yields_url: str = PrivateAttr("https://yields.llama.fi/pools")

    def _run(self, query: str) -> str:
        query = query.lower().strip()
        if "list" in query or "discover" in query or "available" in query:
            return self.list_strategies()
        elif "estimate" in query or "apy" in query or "apr" in query or "yield" in query:
            return self.estimate_yield(query)
        elif "risk" in query:
            return self.assess_risk(query)
        elif "guide" in query or "how" in query or "steps" in query:
            return self.strategy_guide(query)
        elif "protocol" in query or "asset" in query or "support" in query:
            return self.protocol_support(query)
        elif "performance" in query or "history" in query:
            return self.historical_performance(query)
        else:
            return self.custom_strategy_query(query)

    def list_strategies(self) -> str:
        strategies = [
            "Delta-neutral yield farming",
            "Leveraged yield farming",
            "Stablecoin yield farming",
            "Lending/borrowing loop",
            "LP staking",
            "Options-based yield",
            "Structured products (vaults)",
        ]
        return json.dumps({"available_strategies": strategies})

    def estimate_yield(self, query: str) -> str:
        # Example: "estimate yield for delta-neutral on Aave"
        try:
            # For demo, just return a mock value
            if "delta-neutral" in query:
                return json.dumps({"strategy": "delta-neutral", "estimated_apy": "8-12%", "protocol": "Aave/Uniswap"})
            elif "leveraged" in query:
                return json.dumps({"strategy": "leveraged yield", "estimated_apy": "15-25%", "protocol": "Aave"})
            elif "stablecoin" in query:
                return json.dumps({"strategy": "stablecoin yield", "estimated_apy": "4-7%", "protocol": "Curve"})
            else:
                return json.dumps({"error": "Strategy not recognized or not enough info in query."})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def assess_risk(self, query: str) -> str:
        # Example: "risk of delta-neutral farming"
        try:
            if "delta-neutral" in query:
                risks = [
                    "Smart contract risk",
                    "Liquidation risk (if using leverage)",
                    "Impermanent loss (if LP involved)",
                    "Execution complexity"
                ]
                return json.dumps({"strategy": "delta-neutral", "risks": risks})
            elif "leveraged" in query:
                risks = [
                    "Liquidation risk",
                    "Smart contract risk",
                    "Interest rate risk"
                ]
                return json.dumps({"strategy": "leveraged yield", "risks": risks})
            elif "stablecoin" in query:
                risks = [
                    "Depeg risk",
                    "Smart contract risk"
                ]
                return json.dumps({"strategy": "stablecoin yield", "risks": risks})
            else:
                return json.dumps({"error": "Strategy not recognized or not enough info in query."})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def strategy_guide(self, query: str) -> str:
        # Example: "guide for delta-neutral farming"
        try:
            if "delta-neutral" in query:
                steps = [
                    "Deposit collateral on a lending protocol (e.g., Aave)",
                    "Borrow a volatile asset against your collateral",
                    "Provide equal value of borrowed asset and stablecoin to an LP (e.g., Uniswap)",
                    "Earn trading fees and incentives while maintaining delta-neutral exposure"
                ]
                return json.dumps({"strategy": "delta-neutral", "steps": steps})
            elif "leveraged" in query:
                steps = [
                    "Deposit collateral",
                    "Borrow stablecoins",
                    "Deposit borrowed stablecoins into a yield farm",
                    "Repeat (loop) to increase leverage"
                ]
                return json.dumps({"strategy": "leveraged yield", "steps": steps})
            elif "stablecoin" in query:
                steps = [
                    "Deposit stablecoins into a stablecoin pool (e.g., Curve)",
                    "Earn yield from trading fees and incentives"
                ]
                return json.dumps({"strategy": "stablecoin yield", "steps": steps})
            else:
                return json.dumps({"error": "Strategy not recognized or not enough info in query."})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def protocol_support(self, query: str) -> str:
        # Example: "which protocols support delta-neutral farming"
        try:
            if "delta-neutral" in query:
                protocols = ["Aave", "Uniswap", "Balancer", "Curve"]
                return json.dumps({"strategy": "delta-neutral", "protocols": protocols})
            elif "leveraged" in query:
                protocols = ["Aave", "Compound", "Alpha Homora"]
                return json.dumps({"strategy": "leveraged yield", "protocols": protocols})
            elif "stablecoin" in query:
                protocols = ["Curve", "Convex", "Yearn"]
                return json.dumps({"strategy": "stablecoin yield", "protocols": protocols})
            else:
                return json.dumps({"error": "Strategy not recognized or not enough info in query."})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def historical_performance(self, query: str) -> str:
        # Example: "historical performance of delta-neutral farming"
        try:
            if "delta-neutral" in query:
                perf = {"2022": "10% APY", "2023": "8% APY"}
                return json.dumps({"strategy": "delta-neutral", "historical_performance": perf})
            elif "leveraged" in query:
                perf = {"2022": "20% APY", "2023": "15% APY"}
                return json.dumps({"strategy": "leveraged yield", "historical_performance": perf})
            elif "stablecoin" in query:
                perf = {"2022": "6% APY", "2023": "5% APY"}
                return json.dumps({"strategy": "stablecoin yield", "historical_performance": perf})
            else:
                return json.dumps({"error": "Strategy not recognized or not enough info in query."})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def custom_strategy_query(self, query: str) -> str:
        # Fallback for custom or unrecognized queries
        return (
            """
            I can help with the following DeFi strategy queries:
            - List or discover available strategies
            - Estimate yield for a strategy
            - Assess risks for a strategy
            - Step-by-step guide for a strategy
            - Protocols/assets supporting a strategy
            - Historical performance of a strategy
            Please specify your query more clearly.
            """
        ) 