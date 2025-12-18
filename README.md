# 🔍 AI Code Review Agent

An intelligent code review system built with LangGraph that uses a multi-agent workflow to perform comprehensive code analysis (syntax, security, performance, best practices) with Human-in-the-Loop (HITL) approval

## ✨ Features

- 🔍 **Syntax Analysis** - Detects syntax errors and warnings
- 📋 **Best Practices Review** - Checks naming conventions, code organization, and documentation
- 🔒 **Security Audit** - Identifies vulnerabilities like SQL injection, XSS, hardcoded secrets
- ⚡ **Performance Optimization** - Analyzes memory usage, inefficient loops, and complexity
- 👤 **Human-in-the-Loop** - Interactive approval system for review findings
- 🔄 **Iterative Review** - Allows re-analysis if findings need improvement

## 🏗️ Architecture

### Subgraph (Analysis Engine)
- **Syntax Check Node** → **Best Practices Node** → **Security Check Node** → **Performance Review Node**

### Main Graph (Review Workflow)
```
Input → Validation → Analysis Subgraph → HITL Approval → Final Report
                                              ↓ 
                                    (if rejected, loop back to Analysis)
```

## 🛠️ Tech Stack

- **LangGraph** - Multi-agent workflow orchestration with subgraphs
- **LangChain** - LLM integration framework
- **Ollama** - Local LLM inference (llama3.2:1b)
- **Python 3.8+** - Core language

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed locally
- llama3.2:1b model

## 🚀 Setup

1. **Clone the repository**
```bash
git clone https://github.com/AkashR9702/code-review-agent.git
cd code-review-agent
```

2. **Install dependencies**
```bash
pip install langchain langchain-ollama langgraph
```

3. **Pull the Ollama model**
```bash
ollama pull llama3.2:1b
```

## 💡 Usage

Run the agent:
```bash
python code_review_agent.py
```

The agent will:
1. Analyze your code through 4 specialized nodes
2. Display comprehensive findings
3. Ask for your approval (yes/no)
4. Generate a detailed report if approved, or re-analyze if improvements needed

## 📊 Example Output
```
CODE REVIEW RESULTS
============================================================
🔍 Syntax Issues:
[Analysis results...]

📋 Best Practices:
[Analysis results...]

🔒 Security Issues:
[Analysis results...]

⚡ Performance Issues:
[Analysis results...]
============================================================

Do you approve these findings? (yes/no):
```

## 🔮 Advanced Features

The code includes two HITL implementations:

1. **Simple Terminal Input** (Active) - Uses `input()` for interactive demos
2. **Interrupt Pattern** (Commented) - For API/UI integration with programmatic control

## 🎯 Future Enhancements

- Multi-language support (JavaScript, Java, etc.)
- Streamlit web interface
- Integration with GitHub Actions
- Custom rule configuration
- Team collaboration features

## 👨‍💻 Author

Built by **Akash R** as a portfolio project demonstrating:
- Advanced LangGraph patterns (subgraphs, HITL, conditional routing)
- Multi-agent AI systems
- State management and checkpointing
- Real-world problem solving with LLMs

## 📝 License

MIT License - feel free to use and modify!
