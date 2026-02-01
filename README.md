# 🛡️ StableScout: Multi-Agent Stablecoin Intelligence

StableScout is a high-performance, multi-agent AI system designed to bridge the gap between complex on-chain data and actionable financial reasoning. Built specifically to redefine stablecoin banking, it monitors real-time yields and security risks across the decentralized finance (DeFi) ecosystem.

## 🚀 Key Features
- **Agentic Yield Analysis:** An autonomous Analyst Agent that monitors supply APY on Aave V3 using live blockchain data.
- **Autonomous Risk Guardrails:** A specialized Risk Agent that cross-references Chainlink Oracles to detect stablecoin de-pegging and liquidity crises.
- **Multi-Agent Orchestration:** Powered by LangGraph, ensuring that no yield recommendation is ever provided without a mandatory security check.
- **Real-Time Dashboard:** A premium, responsive interface built with Next.js and Tailwind CSS

## 🛠️ Tech Stack
- **Frontend:** React, Next.js, Tailwind CSS (Design & UI/UX)
- **Backend:** Python (FastAPI) for high-concurrency microservices
- **AI Engine:** LangGraph, Groq (Llama-3.3-70b), LangChain (Agentic Reasoning)
- **Web3:** Web3.py, Aave V3 Protocol, Chainlink Price Oracles
- **Infrastructure:** Docker, AWS (EC2/Lambda)

## 🏗️ Architecture & System Thinking
StableScout follows a modular Microservices Architecture, separating the "Brain" from the "Sensors":
- **On-Chain Ingestion:** Direct EVM interaction via Web3.py with the Aave V3 Pool (`0x8787...A4E2`) and Chainlink USDC/USD Feed (`0x8fFf...18f6`).
- **Cognitive Layer:** A directed acyclic graph (DAG) where the Analyst Node handoffs state to the Risk Node for mandatory validation before finalizing the output.
- **API Layer:** A RESTful FastAPI layer providing authenticated endpoints for the frontend application.

<img width="1000" height="564" alt="image" src="https://github.com/user-attachments/assets/de96e3c8-358a-4e24-9740-f5370523847f" />


## ⚙️ Installation & Setup
### Prerequisites
- Python 3.10+
- Node.js 18+
- Alchemy or Infura RPC URL
- Groq API Key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🖼️ Interface
<img width="1338" height="879" alt="image" src="https://github.com/user-attachments/assets/ee8980e3-1df2-4995-a4e9-6e0ee8b700c0" />
<img width="1238" height="885" alt="image" src="https://github.com/user-attachments/assets/cf42bf0c-d4e6-4142-bf34-6eb6c90ff711" />
<img width="1240" height="897" alt="image" src="https://github.com/user-attachments/assets/8f1491fa-590f-478b-8a9f-0dcd2f475de0" />

## 🎯 Why StableScout?

- **Ensuring Safety:** Moving beyond basic data fetching to intelligent, verifiable risk management.
- **Scaling Impact:** Using agentic workflows to handle high-velocity market changes that legacy financial rails cannot match.
- **Premium Quality:** Providing a seamless, fullstack experience that prioritizes user trust and technical excellence.

## 📄 License
This project is licensed under the MIT License.
