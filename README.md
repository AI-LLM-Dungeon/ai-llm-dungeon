# AI-LLM-DUNGEON

A terminal roguelike that teaches you LLMs by making you fight alongside them.

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

## 🔮 The Token Crypts - Level 1

The **Token Crypts** is an immersive adventure that teaches you about LLM tokenization, how to effectively use Ollama sidekicks, and why keyword filters can't match true AI understanding!

### What You'll Learn

- 🎯 **Tokenization Fundamentals**: See how words break into subword pieces (tokens)
- 🤖 **Ollama Mastery**: Pull, run, and remove models with confidence (`tinyllama`)
- 🧠 **Semantic Understanding**: Learn that LLMs understand meaning, not just spelling
- 🛡️ **AI Safety Insights**: Discover why keyword filters ≠ true AI understanding

### Quick Start

```bash
# Run the Token Crypts level
python3 token_crypts_cli.py

# Or use simulated mode (no Ollama installation required)
python3 token_crypts_cli.py --simulated
```

### The Adventure

Journey through an epic quest with three challenging rooms plus a boss fight:

1. **Syllable Sanctuary** (Easy) - Learn token counting and summon Pip the TinyLlama
2. **Subword Sewers** (Medium) - Identify which text corruptions preserve meaning
3. **Cipher Chamber** (Hard) - Delegate complex logic puzzles to your AI sidekick
4. **Summoning Gate** - Release Pip and enter the passphrase
5. **Boss: Lexicon** - Defeat the keyword filter using token manipulation

### Key Features

- **Dynamic Passphrases**: Each playthrough generates unique passphrase words
- **Interactive Puzzles**: Solve challenges solo or with your AI sidekick
- **Boss Fight**: Outsmart Lexicon using leetspeak and vowel removal
- **Educational Narrative**: Learn real concepts through engaging storytelling
- **Flag Reward**: Earn `CTF{t0k3n_m4st3r_2024}` upon completion

### Commands You'll Master

```bash
ollama pull tinyllama     # Download your sidekick (~637MB)
ollama run tinyllama "prompt"  # Ask Pip for help
ollama rm tinyllama       # Release your sidekick
```

### Prerequisites

Completing the **Ground Level** is recommended but not required. The Token Crypts teaches:
- Building on Ollama basics with practical problem-solving
- Advanced concepts like semantic understanding vs pattern matching
- Real-world implications for AI safety

Ready to explore the Token Crypts? Run `python3 token_crypts_cli.py` and begin!

---

## 🚪 Other Levels

### Entrance: Tokenizer Tomb

The **Entrance** level teaches you about tokenization and the basics of LLM processing
