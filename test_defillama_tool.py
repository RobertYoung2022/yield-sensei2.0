import sys
import json
import importlib.util
import os

# Dynamically import DefiLlamaTool from defillama-tool.py
spec = importlib.util.spec_from_file_location("defillama_tool", os.path.join(os.path.dirname(__file__), "defillama-tool.py"))
defillama_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(defillama_module)
DefiLlamaTool = defillama_module.DefiLlamaTool

def print_result(title, result):
    print(f"\n=== {title} ===")
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(result)

def main():
    tool = DefiLlamaTool()
    
    # Test TVL query
    tvl_result = tool._run("tvl")
    print_result("Top TVL Protocols", tvl_result)

    # Test APY query
    apy_result = tool._run("apy")
    print_result("Top Yield Opportunities", apy_result)

    # Test Stablecoin Yields
    stablecoin_result = tool._run("stablecoin apy")
    print_result("Top Stablecoin Yields", stablecoin_result)

    # Test Protocol Info (Aave)
    protocol_result = tool._run("protocol info Aave")
    print_result("Aave Protocol Info", protocol_result)

    # Test Unknown Query
    unknown_result = tool._run("foobar")
    print_result("Unknown Query", unknown_result)

if __name__ == "__main__":
    main() 