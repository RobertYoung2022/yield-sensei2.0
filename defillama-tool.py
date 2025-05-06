# tools/defillama.py
import requests
import json
from typing import List, Dict, Any, Optional, ClassVar
from pydantic import BaseModel, PrivateAttr
from langchain.tools import BaseTool

class DefiLlamaTool(BaseTool):
    """Tool for querying DeFiLlama API to get protocol data"""
    
    name: ClassVar[str] = "defillama_tool"
    description: ClassVar[str] = """
    Use this tool to get data about DeFi protocols from DeFiLlama.
    This tool can fetch TVL (Total Value Locked), APY (Annual Percentage Yield),
    protocol information, and historical data.
    """
    
    _base_url: str = PrivateAttr("https://api.llama.fi")
    _yields_url: str = PrivateAttr("https://yields.llama.fi/pools")
    
    def __init__(self):
        """Initialize the DeFiLlama tool"""
        super().__init__()
        
    def _run(self, query: str) -> str:
        """Run the tool with the specified query"""
        query = query.lower().strip()
        
        if "tvl" in query:
            return self.get_top_tvl_protocols(limit=10)
        elif "apy" in query or "yield" in query:
            if "stablecoin" in query:
                return self.get_stablecoin_yields(limit=10)
            else:
                return self.get_top_yields(limit=10)
        elif "protocol" in query and any(x in query for x in ["info", "data", "details"]):
            # Improved protocol name extraction
            protocol_name = None
            words = query.split()
            for i, word in enumerate(words):
                if word == "protocol" and i+2 < len(words) and words[i+1] in ["info", "data", "details"]:
                    protocol_name = ' '.join(words[i+2:])
                    break
            if protocol_name:
                return self.get_protocol_info(protocol_name)
            return "Please specify a protocol name to get details."
        else:
            return """
            I can help with the following DeFiLlama queries:
            - TVL data (top protocols by TVL)
            - APY/Yield data (top yields or stablecoin yields)
            - Protocol information (details about a specific protocol)
            
            Please specify your query more clearly.
            """
    
    def get_top_tvl_protocols(self, limit: int = 10) -> str:
        """Get the top protocols by TVL"""
        try:
            response = requests.get(f"{self._base_url}/protocols")
            print("[DEBUG] TVL API response status:", response.status_code)
            print("[DEBUG] TVL API response text:", response.text[:500])
            data = response.json()
            
            # Sort by TVL (highest first) and limit results
            sorted_protocols = sorted(data, key=lambda x: x.get('tvl', 0) if x.get('tvl') is not None else 0, reverse=True)[:limit]
            
            result = {
                "top_tvl_protocols": [
                    {
                        "name": protocol.get('name', 'Unknown'),
                        "tvl": protocol.get('tvl', 0),
                        "chain": protocol.get('chain', 'Unknown'),
                        "category": protocol.get('category', 'Unknown'),
                        "url": protocol.get('url', '')
                    }
                    for protocol in sorted_protocols
                ]
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return f"Error fetching TVL data: {str(e)}"
    
    def get_top_yields(self, limit: int = 10) -> str:
        """Get the top yield opportunities"""
        try:
            response = requests.get(self._yields_url)
            print("[DEBUG] Yields API response status:", response.status_code)
            print("[DEBUG] Yields API response text:", response.text[:500])
            data = response.json()
            
            # Filter out zero or unrealistic APYs (> 1000%)
            filtered_pools = [
                pool for pool in data.get('data', [])
                if pool.get('apy', 0) is not None and 0 < pool.get('apy', 0) < 1000
            ]
            
            # Sort by APY (highest first) and limit results
            sorted_pools = sorted(filtered_pools, key=lambda x: x.get('apy', 0), reverse=True)[:limit]
            
            result = {
                "top_yield_opportunities": [
                    {
                        "pool": pool.get('pool', 'Unknown'),
                        "project": pool.get('project', 'Unknown'),
                        "chain": pool.get('chain', 'Unknown'),
                        "apy": pool.get('apy', 0),
                        "tvl": pool.get('tvlUsd', 0),
                        "il_risk": "Yes" if pool.get('ilRisk', False) else "No",
                        "stable_pool": "Yes" if pool.get('stablecoin', False) else "No",
                        "tokens": pool.get('symbol', 'Unknown')
                    }
                    for pool in sorted_pools
                ]
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return f"Error fetching yield data: {str(e)}"
    
    def get_stablecoin_yields(self, limit: int = 10) -> str:
        """Get the top stablecoin yield opportunities"""
        try:
            response = requests.get(self._yields_url)
            print("[DEBUG] Stablecoin Yields API response status:", response.status_code)
            print("[DEBUG] Stablecoin Yields API response text:", response.text[:500])
            data = response.json()
            
            # Filter for stablecoin pools with reasonable APY
            stablecoin_pools = [
                pool for pool in data.get('data', [])
                if pool.get('stablecoin', False) and pool.get('apy', 0) is not None and 0 < pool.get('apy', 0) < 100
            ]
            
            # Sort by APY (highest first) and limit results
            sorted_pools = sorted(stablecoin_pools, key=lambda x: x.get('apy', 0), reverse=True)[:limit]
            
            result = {
                "top_stablecoin_yields": [
                    {
                        "pool": pool.get('pool', 'Unknown'),
                        "project": pool.get('project', 'Unknown'),
                        "chain": pool.get('chain', 'Unknown'),
                        "apy": pool.get('apy', 0),
                        "tvl": pool.get('tvlUsd', 0),
                        "tokens": pool.get('symbol', 'Unknown')
                    }
                    for pool in sorted_pools
                ]
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return f"Error fetching stablecoin yield data: {str(e)}"
    
    def get_protocol_info(self, protocol_name: str) -> str:
        """Get information about a specific protocol"""
        try:
            # Get all protocols first
            response = requests.get(f"{self._base_url}/protocols")
            data = response.json()
            if not isinstance(data, list):
                return f"Unexpected response format: {type(data)}"
            # Find the protocol by name (case-insensitive partial match)
            protocol_name = protocol_name.lower()
            matching_protocols = [
                p for p in data
                if protocol_name in p.get('name', '').lower()
            ]
            if not matching_protocols:
                return f"No protocol found matching '{protocol_name}'"
            # Use the first match (most relevant)
            protocol = matching_protocols[0]
            protocol_slug = protocol.get('slug', '')
            # Get detailed info about the protocol
            if protocol_slug:
                detail_response = requests.get(f"{self._base_url}/protocol/{protocol_slug}")
                detail_data = detail_response.json()
                # If the response is a list, use the first item
                if isinstance(detail_data, list):
                    if len(detail_data) > 0:
                        detail_data = detail_data[0]
                    else:
                        return f"No detailed data found for protocol '{protocol_name}'"
                # Extract per-chain TVL summary if available
                chain_tvls = {}
                if 'chainTvls' in detail_data and isinstance(detail_data['chainTvls'], dict):
                    for chain, chain_data in detail_data['chainTvls'].items():
                        # Get the latest TVL value if available
                        tvl_list = chain_data.get('tvl', [])
                        if isinstance(tvl_list, list) and len(tvl_list) > 0:
                            latest_tvl = tvl_list[-1].get('totalLiquidityUSD', None)
                            chain_tvls[chain] = latest_tvl
                result = {
                    "protocol_info": {
                        "name": protocol.get('name', 'Unknown'),
                        "tvl": detail_data.get('tvl', 0),
                        "chains": detail_data.get('chains', []),
                        "category": protocol.get('category', 'Unknown'),
                        "description": protocol.get('description', 'No description available'),
                        "url": protocol.get('url', ''),
                        "twitter": protocol.get('twitter', ''),
                        "audit_links": protocol.get('audit_links', []),
                        "chain_tvls": chain_tvls
                    }
                }
                return json.dumps(result, indent=2)
            else:
                return json.dumps({"protocol_info": protocol}, indent=2)
        except Exception as e:
            return f"Error fetching protocol data: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async implementation of this tool"""
        raise NotImplementedError("DeFiLlama tool does not support async")
