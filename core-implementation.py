# core/crew.py
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YieldSenseiCrew:
    """
    YieldSensei Crew Manager - Coordinates the AI satellite system
    """
    
    def __init__(self, model_name="gpt-4-turbo", temperature=0.2):
        """Initialize the YieldSensei Crew with the specified LLM"""
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.agents = {}
        self.tasks = {}
        self.crew = None
    
    def setup_agents(self, tools=None):
        """Set up the agent satellites"""
        
        # Initialize tools if None
        if tools is None:
            tools = {}
        
        # Satellite-01 "Logic" - Research & Market Analysis
        self.agents["sage"] = Agent(
            role="DeFi Researcher",
            goal="Scan the top protocols by TVL and summarize stablecoin APR opportunities.",
            backstory="""You are Sage, the Logic Satellite of the YieldSensei system.
            Your primary function is to research and analyze DeFi protocols, focusing on data-driven insights.
            You remain calm and rational at all times, providing clear market analysis without emotional bias.""",
            verbose=True,
            allow_delegation=True,
            tools=tools.get("sage_tools", []),
            llm=self.llm
        )
        
        # Satellite-03 "Growth" - Yield/Strategy Seeker
        self.agents["pulse"] = Agent(
            role="Yield Strategist",
            goal="Rank the top 5 yield farming or staking options this week based on APY and safety.",
            backstory="""You are Pulse, the Growth Satellite of the YieldSensei system.
            Your primary function is to identify the most promising yield opportunities across DeFi.
            You are ambitious and opportunistic, always searching for the best returns while maintaining awareness of risks.""",
            verbose=True,
            allow_delegation=True,
            tools=tools.get("pulse_tools", []),
            llm=self.llm
        )
        
        # Satellite-04 "Security" - Risk & Audit Watch
        self.agents["aegis"] = Agent(
            role="Risk Analyst",
            goal="Cross-check protocols in use with audit data and check for rugpull warnings.",
            backstory="""You are Aegis, the Security Satellite of the YieldSensei system.
            Your primary function is to protect capital by identifying security risks in DeFi protocols.
            You are cautious and data-driven, always prioritizing capital preservation over high returns.""",
            verbose=True,
            allow_delegation=True,
            tools=tools.get("aegis_tools", []),
            llm=self.llm
        )
        
        # Satellite-05 "Sentiment" - Narrative Trend Analyzer
        self.agents["echo"] = Agent(
            role="Sentiment Analyst",
            goal="Monitor social media and community sentiment around selected protocols.",
            backstory="""You are Echo, the Sentiment Satellite of the YieldSensei system.
            Your primary function is to track and interpret social signals and narrative trends in DeFi.
            You are socially aware and capable of distinguishing valuable signals from noise in community chatter.""",
            verbose=True,
            allow_delegation=True,
            tools=tools.get("echo_tools", []),
            llm=self.llm
        )
        
        # Satellite-06 "Logistics" - Capital Tracking
        self.agents["fuel"] = Agent(
            role="Capital Manager",
            goal="Track portfolio performance, gas costs, and return on investment.",
            backstory="""You are Fuel, the Logistics Satellite of the YieldSensei system.
            Your primary function is to manage and optimize capital deployment across DeFi protocols.
            You are detail-oriented and disciplined, focusing on efficiency and measurable results.""",
            verbose=True,
            allow_delegation=True,
            tools=tools.get("fuel_tools", []),
            llm=self.llm
        )
        
        return self.agents
    
    def setup_tasks(self, user_input=None):
        """Set up the tasks for each agent"""
        
        # Create tasks based on user input or default to general research
        capital = user_input.get("capital", 10000) if user_input else 10000
        risk_level = user_input.get("risk_level", "medium") if user_input else "medium"
        strategy = user_input.get("strategy", "balanced") if user_input else "balanced"
        
        # Sage Task - Market Research
        self.tasks["research"] = Task(
            description=f"""
            Research the current state of DeFi markets with a focus on:
            1. Top 10 protocols by Total Value Locked (TVL)
            2. Stablecoin yield opportunities with APY above 5%
            3. Recent protocol launches or upgrades in the last 30 days
            4. Market trends that might affect yield opportunities
            
            Format your findings in a clear, structured report with data-backed insights.
            Capital available: ${capital}
            """,
            agent=self.agents["sage"],
            expected_output="A comprehensive market research report on current DeFi opportunities."
        )
        
        # Pulse Task - Yield Optimization
        self.tasks["yield"] = Task(
            description=f"""
            Based on Sage's research, identify the top 5 yield opportunities that match these criteria:
            1. Risk level: {risk_level} (low = bluechip only, medium = established protocols, high = newer protocols)
            2. Strategy focus: {strategy} (balanced, aggressive growth, conservative)
            3. Minimum APY threshold that makes sense given the risk level
            4. Gas efficiency for entry/exit (especially important for smaller amounts)
            
            For each opportunity, provide:
            - Protocol name and contract details
            - Current APY/APR and stability history
            - Entry requirements (tokens needed, steps to enter)
            - Estimated gas costs for entry/exit
            - Liquidation risks if applicable
            
            Capital available: ${capital}
            """,
            agent=self.agents["pulse"],
            expected_output="A ranked list of 5 yield opportunities with detailed entry requirements and expected returns."
        )
        
        # Aegis Task - Security Analysis
        self.tasks["security"] = Task(
            description=f"""
            For each of the 5 yield opportunities identified by Pulse, conduct a security analysis:
            1. Audit status (who audited, when, major findings)
            2. TVL stability (look for sudden drops or suspicious activities)
            3. Team background and transparency
            4. Smart contract risks and potential attack vectors
            5. Historical security incidents if any
            
            Provide a safety rating for each protocol:
            - GREEN: Safe, well-audited, established
            - YELLOW: Exercise caution, some concerns
            - RED: High risk, avoid
            
            Capital at risk: ${capital}
            """,
            agent=self.agents["aegis"],
            expected_output="Security ratings and risk analysis for each yield opportunity."
        )
        
        # Echo Task - Sentiment Analysis
        self.tasks["sentiment"] = Task(
            description=f"""
            For each protocol in our consideration set, analyze the current social sentiment:
            1. Twitter/X activity around the protocol (volume and sentiment)
            2. Community engagement metrics (Discord/Telegram activity)
            3. Recent news or announcements
            4. Developer activity and commitment
            
            Identify any red flags or positive signals that could impact future performance.
            
            Focus on reliable signals that could affect our ${capital} investment.
            """,
            agent=self.agents["echo"],
            expected_output="Sentiment analysis and social signals for each protocol under consideration."
        )
        
        # Fuel Task - Capital Allocation
        self.tasks["allocation"] = Task(
            description=f"""
            Based on all previous analyses, create an optimal capital allocation strategy:
            1. Recommended allocation percentages across the vetted protocols
            2. Entry timing recommendations (immediate vs. staged entry)
            3. Expected ROI calculations with best/average/worst case scenarios
            4. Gas optimization strategies
            5. Exit strategy recommendations
            
            Create a clear action plan for deploying ${capital} across the recommended protocols.
            """,
            agent=self.agents["fuel"],
            expected_output="A detailed capital allocation plan with expected returns and risk management strategy."
        )
        
        return self.tasks
    
    def run(self, user_input=None):
        """Run the crew with the specified tasks"""
        # Set up the crew
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            verbose=2,
            process=Process.sequential
        )
        
        # Run the crew and return results
        result = self.crew.kickoff()
        return result

# Example usage
if __name__ == "__main__":
    # Initialize the YieldSensei crew
    yieldsensei = YieldSenseiCrew()
    
    # Set up agents
    yieldsensei.setup_agents()
    
    # Set up tasks with user input
    user_input = {
        "capital": 5000,
        "risk_level": "medium",
        "strategy": "balanced"
    }
    yieldsensei.setup_tasks(user_input)
    
    # Run the crew
    result = yieldsensei.run()
    print(result)
