import json
import importlib.util
import os

# Dynamically import SecurityAnalysisTool from security-tool.py
spec = importlib.util.spec_from_file_location("security_tool", os.path.join(os.path.dirname(__file__), "security-tool.py"))
security_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security_module)
SecurityAnalysisTool = security_module.SecurityAnalysisTool

def print_result(title, result):
    print(f"\n=== {title} ===")
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(result)

def main():
    tool = SecurityAnalysisTool()
    
    # Test audit info for Aave
    audit_result = tool._run("audit aave")
    print_result("Aave Audit Info", audit_result)

    # Test TVL stability for Aave
    tvl_result = tool._run("tvl stability aave")
    print_result("Aave TVL Stability", tvl_result)

    # Test risk rating for Uniswap
    risk_result = tool._run("risk uniswap")
    print_result("Uniswap Risk Rating", risk_result)

    # Test general security overview
    overview_result = tool._run("security overview")
    print_result("General Security Overview", overview_result)

    # Test unknown query
    unknown_result = tool._run("foobar")
    print_result("Unknown Query", unknown_result)

if __name__ == "__main__":
    main() 