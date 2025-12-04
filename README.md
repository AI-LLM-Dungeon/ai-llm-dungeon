# AI-LLM-DUNGEON

A terminal roguelike that teaches you LLMs by making you fight them.

**Play right now:**
```bash
curl -fSSL https://ai-llm-dungeon.github.io/ai-llm-dungeon/install.sh | bash
```

## 🏰 Ground Level: Ollama Mastery Tutorial

The **Ground Level** is a fully playable Python tutorial that teaches you the fundamentals of Ollama and local LLM management through an interactive dungeon adventure!

### What You'll Learn

- 🧙 **Sidekick Summoning**: Learn to summon local LLMs with precise commands
- 🧩 **Model Capabilities**: Understand the strengths and limitations of different model sizes
- 💾 **Memory Management**: Practice adding and removing models to manage system resources
- 🎯 **Benchmarking**: Test model capabilities with riddles and puzzles
- 💡 **Knowledge Tips**: Unlock practical insights about LLM usage

### Quick Start

```bash
# Clone the repository
git clone https://github.com/AI-LLM-Dungeon/ai-llm-dungeon.git
cd ai-llm-dungeon

# Run the Ground Level tutorial
python3 ground_level_cli.py
```

### The Journey

Navigate through 4 connected rooms, each teaching a key concept:

1. **The Summoning Chamber** - Learn to summon your first sidekick (Phi3 Mini)
2. **The Riddle Hall** - Discover model limitations through puzzle-solving
3. **The Upgrade Forge** - Master model management by upgrading to Llama3 8b
4. **The Victory Chamber** - Achieve success with a more capable model

### Game Features

- **ASCII Art Visualizations**: Beautiful terminal graphics for each sidekick
- **Interactive Storytelling**: Engaging narrative that makes learning fun
- **Progress Tracking**: Earn knowledge points and unlock educational tips
- **Simulated Ollama Commands**: Learn Ollama without needing to install it
- **Real-World Skills**: Commands and concepts directly applicable to actual Ollama usage

### Commands

- `help` - Show available commands
- `status` - View your progress and active sidekick
- `tips` - See all unlocked knowledge tips
- `east/west` - Navigate between rooms
- Type scroll text exactly to summon sidekicks
- Follow room-specific prompts for puzzles and challenges

### Educational Design

The Ground Level is designed with pedagogical principles:

- **Learn by Doing**: Interactive commands reinforce muscle memory
- **Progressive Complexity**: Start simple, gradually increase difficulty
- **Immediate Feedback**: See the results of your actions right away
- **Failure as Learning**: Small models fail intentionally to teach trade-offs
- **Real-World Analogies**: Game mechanics mirror actual Ollama workflows

### After Completion

Once you've mastered the Ground Level, you'll understand:

- How to pull, run, and remove models with Ollama
- The relationship between model size and capability
- When to use small vs. large models
- How to manage system memory effectively
- The basics of prompt engineering

Ready to start your adventure? Run `python3 ground_level_cli.py` and begin your journey!

---

## 🚪 Other Levels

### Entrance: Tokenizer Tomb

The **Entrance** level teaches you about tokenization and the basics of LLM processing
