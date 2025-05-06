import json
import importlib.util
import os

# Dynamically import StrategyTool from strategy-tool.py
spec = importlib.util.spec_from_file_location("strategy_tool", os.path.join(os.path.dirname(__file__), "strategy-tool.py"))
strategy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(strategy_module)
StrategyTool = strategy_module.StrategyTool

def print_result(title, result):
    print(f"\n=== {title} ===")
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(result)

def main():
    tool = StrategyTool()
    
    # 1. List available strategies
    list_result = tool._run("list strategies")
    print_result("List Strategies", list_result)

    # 2. Estimate yield for delta-neutral
    yield_result = tool._run("estimate yield for delta-neutral on Aave")
    print_result("Estimate Yield (Delta-Neutral)", yield_result)

    # 3. Assess risk for leveraged yield
    risk_result = tool._run("risk of leveraged yield farming")
    print_result("Assess Risk (Leveraged Yield)", risk_result)

    # 4. Step-by-step guide for stablecoin yield
    guide_result = tool._run("guide for stablecoin yield farming")
    print_result("Strategy Guide (Stablecoin Yield)", guide_result)

    # 5. Protocol support for delta-neutral
    support_result = tool._run("which protocols support delta-neutral farming")
    print_result("Protocol Support (Delta-Neutral)", support_result)

    # 6. Historical performance for leveraged yield
    perf_result = tool._run("historical performance of leveraged yield farming")
    print_result("Historical Performance (Leveraged Yield)", perf_result)

    # 7. Custom/unrecognized query
    custom_result = tool._run("explain advanced vault strategies")
    print_result("Custom Query (Unrecognized)", custom_result)

    # 8. Edge case: empty query
    empty_result = tool._run("")
    print_result("Empty Query", empty_result)

    # 9. Edge case: malformed query
    malformed_result = tool._run("yield123")
    print_result("Malformed Query (yield123)", malformed_result)

if __name__ == "__main__":
    main() 