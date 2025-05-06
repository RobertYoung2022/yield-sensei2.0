# 🧠 YieldSensei: DeFi AI Satellite System

YieldSensei is a multi-agent DeFi Investment Advisor inspired by Vegapunk's satellite model. Each AI agent serves a distinct function (research, growth, security, etc.) and works together to provide intelligent crypto investment support.

## 🚀 Features

- 🧠 **Sage (Logic)**: Researches DeFi protocols and market trends
- 🌾 **Pulse (Growth)**: Identifies high-yield farming and staking opportunities
- 🛡️ **Aegis (Security)**: Analyzes protocol security and risk factors
- 📣 **Echo (Sentiment)**: Monitors social sentiment and community trends
- 🔋 **Fuel (Logistics)**: Tracks portfolio performance and optimizes capital deployment

## 📋 Requirements

- Python 3.9+
- OpenAI API key (for GPT-4 access)
- Internet connection (for API calls to DeFiLlama, etc.)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yieldsensei.git
cd yieldsensei
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Usage

### CLI Interface

Run YieldSensei from the command line:

```bash
python main.py --capital 5000 --risk medium --strategy balanced
```

Parameters:
- `--capital`: Amount of capital to deploy (in USD)
- `--risk`: Risk tolerance (low, medium, high)
- `--strategy`: Investment strategy (conservative, balanced, aggressive)

### Streamlit Dashboard (Optional)

For a more visual experience, launch the Streamlit dashboard:

```bash
streamlit run ui/streamlit_app.py
```

Then visit http://localhost:8501 in your browser.

## 🛠️ Agent Architecture

YieldSensei uses CrewAI to orchestrate multiple specialized agents:

1. **Sage (Logic)** - Collects and analyzes market data about DeFi protocols
2. **Pulse (Growth)** - Identifies and ranks yield opportunities based on APY and safety
3. **Aegis (Security)** - Performs security checks and risk analysis on protocols
4. **Echo (Sentiment)** - Analyzes social signals and community sentiment
5. **Fuel (Logistics)** - Tracks and optimizes capital deployment

Each agent has specific tools and prompts designed for their function.

## 📊 Data Sources

- [DeFiLlama](https://defillama.com/): TVL and APY data
- [CertiK](https://www.certik.com/): Security audits information
- [Twitter/X](https://x.com): Sentiment analysis
- [Etherscan](https://etherscan.io/): On-chain activity

## 🗂️ Project Structure

```
yieldsensei/
├── agents/             # Agent definitions and logic
├── tools/              # API integrations and tools
├── core/               # Core system functionality
├── ui/                 # User interfaces (CLI & Streamlit)
├── data/               # Local data storage
├── requirements.txt    # Project dependencies
├── main.py             # Application entry point
└── README.md           # This file
```

## 📈 Sample Output

The system will provide recommendations like:

```
🧠 YieldSensei Investment Recommendation
=======================================
Capital: $5,000
Risk Profile: Medium
Strategy: Balanced

Top 3 Opportunities:
1. USDC Lending on Aave (Polygon)
   - APY: 4.32%
   - Security: GREEN ✅
   - Sentiment: Positive
   - Capital: $2,500 (50%)

2. ETH-USDC LP on Uniswap V3 (Ethereum)
   - APY: 8.76%
   - Security: GREEN ✅
   - Sentiment: Very Positive
   - Capital: $1,500 (30%)

3. MATIC Staking on Polygon
   - APY: 12.45%
   - Security: YELLOW ⚠️
   - Sentiment: Neutral
   - Capital: $1,000 (20%)

Expected Monthly Return: $42.88 (10.3% APY)
Gas Costs: Approx. $15 for initial setup
```

## 🌱 Future Improvements

- Add Forge satellite for infrastructure development
- Implement real-time monitoring of positions
- Create mobile notification system for opportunity alerts
- Add direct wallet integration for automated deployment

## 📜 License

MIT

## 🙏 Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [DeFiLlama](https://defillama.com/) for comprehensive DeFi data