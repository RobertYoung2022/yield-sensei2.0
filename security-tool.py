# tools/security.py
import requests
import json
from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool

class SecurityAnalysisTool(BaseTool):
    """Tool for analyzing the security posture of DeFi protocols"""
    
    name = "security_analysis_tool"
    description = """
    Use this tool to check the security status of DeFi protocols.
    This tool can check audit status, look for security incidents,
    and evaluate TVL stability as a security indicator.
    """
    
    def __init__(self):
        """Initialize the Security Analysis tool"""
        super().__init__()
        self.defillama_url = "https://api.llama.fi"
        self.certik_url = "https://raw.githubusercontent.com/SCV-Security/PublicReports/main/CERTIKsecurity.json"
        
        # In a real implementation, you would use actual APIs for these services
        # For this MVP, we'll simulate some audit data
        self.audit_data = self._load_audit_data()
    
    def _load_audit_data(self) -> Dict:
        """Load simulated audit data for protocols"""
        # In a production system, this would pull from CertiK, WatchPug, or other audit databases
        # For the MVP, we'll use a simple dictionary with some common protocols
        return {
            "aave": {
                "audited": True,
                "auditors": ["CertiK", "PeckShield", "OpenZeppelin"],
                "last_audit_date": "2023-11-15",
                "audit_score": 95,
                "security_incidents": [],
                "risk_level": "LOW"
            },
            "compound": {
                "audited": True,
                "auditors": ["Trail of Bits", "OpenZeppelin"],
                "last_audit_date": "2023-09-22",
                "audit_score": 93,
                "security_incidents": ["Minor oracle issue (2022)"],
                "risk_level": "LOW"
            },
            "uniswap": {
                "audited": True,
                "auditors": ["CertiK", "Trail of Bits", "ABDK"],
                "last_audit_date": "2023-06-10",
                "audit_score": 97,
                "security_incidents": [],
                "risk_level": "LOW"
            },
            "curve": {
                "audited": True,
                "auditors": ["MixBytes", "Trail of Bits"],
                "last_audit_date": "2023-08-05",
                "audit_score": 91,
                "security_incidents": ["Frontend exploit (2023)"],
                "risk_level": "MEDIUM"
            },
            "pancakeswap": {
                "audited": True,
                "auditors": ["CertiK"],
                "last_audit_date": "2023-07-18",
                "audit_score": 88,
                "security_incidents": [],
                "risk_level": "MEDIUM"
            },
            "sushiswap": {
                "audited": True,
                "auditors": ["PeckShield", "Quantstamp"],
                "last_audit_date": "2022-11-30",
                "audit_score": 85,
                "security_incidents": ["Miso platform exploit (2021)"],
                "risk_level": "MEDIUM"
            },
            "balancer": {
                "audited": True,
                "auditors": ["Trail of Bits"],
                "last_audit_date": "2023-05-12",
                "audit_score": 90,
                "security_incidents": ["Flash loan attack (2020)"],
                "risk_level": "MEDIUM"
            }
        }
    
    def _run(self, query: str) -> str:
        """Run the tool with the specified query"""
        query = query.lower().strip()
        
        if "audit" in query or "security" in query:
            # Check if we're querying about a specific protocol
            for protocol in self.audit_data.keys():
                if protocol in query:
                    return self.get_protocol_security_info(protocol)
            
            # If no specific protocol mentioned, return a general security overview
            return self.get_general_security_overview()
        
        elif "tvl" in query and "stability" in query:
            # Extract protocol name from query if present
            for protocol in self.audit_data.keys():
                if protocol in query:
                    return self.check_tvl_stability(protocol)
            
            # If no specific protocol mentioned, explain what we need
            return "Please specify a protocol name to check TVL stability."
        
        elif "risk" in query or "rating" in query:
            # Extract protocol name from query if present
            for protocol in self.audit_data.keys():
                if protocol in query:
                    return self.get_risk_rating(protocol)
            
            # If no specific protocol mentioned, return risk ratings for all protocols
            return self.get_all_risk_ratings()
        
        else:
            return """
            I can help with the following security analysis queries:
            - Audit information for a specific protocol
            - TVL stability analysis for a protocol
            - Risk ratings for protocols
            
            Please specify your query more clearly.
            """
    
    def get_protocol_security_info(self, protocol_name: str) -> str:
        """Get security information for a specific protocol"""
        protocol_name = protocol_name.lower()
        
        if protocol_name in self.audit_data:
            data = self.audit_data[protocol_name]
            
            result = {
                "protocol": protocol_name,
                "security_info": {
                    "audited": data["audited"],
                    "auditors": data["auditors"],
                    "last_audit_date": data["last_audit_date"],
                    "audit_score": data["audit_score"],
                    "security_incidents": data["security_incidents"],
                    "risk_level": data["risk_level"]
                }
            }
            
            return json.dumps(result, indent=2)
        
        # If protocol not in our database, try to fetch from DeFiLlama for audit links
        try:
            # Get all protocols first to find the matching slug
            response = requests.get(f"{self.defillama_url}/protocols")
            data = response.json()
            
            matching_protocols = [
                p for p in data
                if protocol_name in p.get('name', '').lower()
            ]
            
            if not matching_protocols:
                return f"No security information found for '{protocol_name}'"
            
            protocol = matching_protocols[0]
            audit_links = protocol.get('audit_links', [])
            
            result = {
                "protocol": protocol.get('name', protocol_name),
                "limited_security_info": {
                    "audit_links": audit_links,
                    "note": "This protocol is not in our security database. Basic information gathered from DeFiLlama.",
                    "recommendation": "Conduct further research before investing."
                }
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return f"Error fetching security data for {protocol_name}: {str(e)}"
    
    def check_tvl_stability(self, protocol_name: str) -> str:
        """Check TVL stability for a protocol as a security indicator"""
        try:
            protocol_name = protocol_name.lower()
            
            # Get all protocols first to find the matching slug
            response = requests.get(f"{self.defillama_url}/protocols")
            data = response.json()
            
            matching_protocols = [
                p for p in data
                if protocol_name in p.get('name', '').lower()
            ]
            
            if not matching_protocols:
                return f"No protocol found matching '{protocol_name}'"
            
            protocol = matching_protocols[0]
            protocol_slug = protocol.get('slug', '')
            
            if not protocol_slug:
                return f"Could not find protocol slug for '{protocol_name}'"
            
            # Get TVL history
            detail_response = requests.get(f"{self.defillama_url}/protocol/{protocol_slug}")
            detail_data = detail_response.json()
            
            # Get 30-day TVL chart for stability analysis
            tvl_chart = detail_data.get('tvl', {}).get('chart', {})
            if not tvl_chart:
                return f"Could not retrieve TVL history for '{protocol_name}'"
            
            # Calculate TVL stability metrics
            # For a production system, you would do more sophisticated statistical analysis
            # For the MVP, we'll do a simple volatility check
            
            # Extract the most recent 30 days of data if available
            recent_tvl = tvl_chart[-30:] if len(tvl_chart) >= 30 else tvl_chart
            
            # Calculate basic stability metrics
            if len(recent_tvl) > 1:
                tvl_values = [entry[1] for entry in recent_tvl]  # TVL values
                max_tvl = max(tvl_values)
                min_tvl = min(tvl_values)
                avg_tvl = sum(tvl_values) / len(tvl_values)
                
                # Calculate volatility as a percentage of average TVL
                volatility = (max_tvl - min_tvl) / avg_tvl * 100
                
                # Determine stability rating
                stability_rating = "HIGH" if volatility < 10 else "MEDIUM" if volatility < 30 else "LOW"
                
                result = {
                    "protocol": protocol.get('name', protocol_name),
                    "tvl_stability": {
                        "current_tvl": tvl_values[-1],
                        "30d_avg_tvl": avg_tvl,
                        "30d_volatility_pct": volatility,