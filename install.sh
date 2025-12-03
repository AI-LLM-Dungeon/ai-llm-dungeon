# This is a test comment.
#!/bin/bash
set -e
echo "Entering the AI-LLM-Dungeon..."

# Install Ollama if missing
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama (local LLM runner)..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull the tiny fast model
echo "Downloading phi3:mini (runs on any laptop)..."
ollama pull phi3:mini

# Clone the game
echo "Opening the dungeon gates..."
mkdir -p ~/ai-llm-dungeon
git clone https://github.com/AI-LLM-Dungeon/ai-llm-dungeon.git ~/ai-llm-dungeon 2>/dev/null || (cd ~/ai-llm-dungeon && git pull)

# Drop player in the entrance
cd ~/ai-llm-dungeon/entrance
clear
echo "========================================"
echo "   WELCOME TO AI-LLM-DUNGEON"
echo "========================================"
cat README.md
echo -e "\nYour first battle begins NOW:"
echo "python tokenizer_fight.py 'Hello, world!'"
