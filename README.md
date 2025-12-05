# AI-LLM-Dungeon

**A modular, community-driven LLM education platform disguised as a dungeon crawler.**

Learn offensive and defensive AI security through interactive terminal adventures. Master LLMs by descending through 10 tiers of increasing difficulty—where depth equals danger, and every level teaches you something invaluable.

---

## 🚀 Quick Start

Get playing in 3 commands:

```bash
git clone https://github.com/AI-LLM-Dungeon/ai-llm-dungeon.git
cd ai-llm-dungeon
python3 ground_level_cli.py
```

No Ollama installed? No problem—use simulated mode to learn the commands first.

---

## 🔄 Updating AI-LLM-Dungeon

**Already have the repo?** Here's how to get the latest levels and improvements:

### Quick Update
```bash
git pull origin main
```

### Fresh Install (if you made local changes)
```bash
# Save your progress if needed
git stash

# Get latest updates
git pull origin main

# Or start fresh
cd ..
rm -rf ai-llm-dungeon
git clone https://github.com/AI-LLM-Dungeon/ai-llm-dungeon.git
cd ai-llm-dungeon
```

### Discover New Levels
```bash
# List all playable levels (look for *_cli.py files)
ls *_cli.py

# Run any level
python3 ./ground_level_cli.py
python3 ./token_crypts_cli.py
```

### What Gets Updated vs. Preserved
- ✅ **Updated**: Game code, new levels, bug fixes, documentation
- ✅ **Preserved**: Your downloaded Ollama models (stored separately by Ollama)
- ✅ **Preserved**: Game data files (passphrase seeds, etc.)

### 💡 Pro Tip
⭐ Star this repo on GitHub to get notified about new levels and features!

---

## 🗺️ The Dungeon Map

AI-LLM-Dungeon is structured as a **10-tier descent into knowledge**:

| Tier | Depth | Difficulty | Focus |
|------|-------|------------|-------|
| 1 | Surface | Beginner | Getting started, basic commands |
| 2 | Shallow | Beginner+ | Fundamental concepts |
| 3 | Upper | Intermediate | Practical applications |
| 4 | Middle | Intermediate+ | Complex scenarios |
| 5 | Lower | Advanced | System-level understanding |
| 6 | Deep | Advanced+ | Sophisticated techniques |
| 7 | Profound | Expert | Mastery-level concepts |
| 8 | Ancient | Expert+ | Deep theory and history |
| 9 | Abyssal | Master | Cutting-edge research |
| 10 | Transcendent | Legendary | Pushing boundaries |

**Deeper = Harder.** Start at Tier 1 and work your way down.

---

## 🎯 Team Alignments

Every level belongs to one of three teams, each representing a different security perspective:

### 🔴 Red Team (Offensive / Natural)
**Attack, probe, discover weaknesses**

Learn adversarial techniques: prompt injection, jailbreaking, model manipulation. Red Team levels teach you how to think like an attacker—finding vulnerabilities and edge cases.

**Location Words**: Natural formations (caves, rivers, forests, meadows)

### 🔵 Blue Team (Defensive / Constructed)
**Defend, build, strengthen systems**

Learn LLM fundamentals and safe deployment: proper usage, input validation, security controls. Blue Team levels teach you how to build and operate AI systems responsibly.

**Location Words**: Human-made structures (villages, crypts, towers, tunnels)

### 🟣 Purple Team (Hybrid / Both)
**Combine offense and defense**

See both perspectives: ethical hacking for protection, balanced security mindset. Purple Team levels teach you the complete security lifecycle.

**Location Words**: Hybrid spaces (gardens, sanctuaries, grottoes, convergences)

---

## 📚 Available Levels

### Tier 1: Surface (Beginner)

#### 🔵 Ollama Village
*Formerly "Ground Level: Ollama Mastery Tutorial"*

**Tier 1 • Blue Team • Beginner**

Learn the fundamentals of Ollama and local LLM management through an interactive adventure.

**What You'll Learn**:
- Summoning local LLMs with precise commands
- Model capabilities and limitations by size
- Memory management and resource control
- Benchmarking model performance
- Real-world Ollama workflows

**Quick Start**:
```bash
python3 ground_level_cli.py
```

**Journey**: Navigate 4 connected rooms, each teaching a key concept. Summon sidekicks, solve puzzles, and master the fundamentals.

---

### Tier 2: Shallow (Beginner+)

#### 🔵 Token Crypts

**Tier 2 • Blue Team • Beginner+**

Master tokenization and discover why keyword filters fail against true AI understanding.

**What You'll Learn**:
- How LLMs break text into tokens
- Semantic understanding vs. pattern matching
- Why spelling variations don't fool AI
- Real-world AI safety implications

**Quick Start**:
```bash
python3 token_crypts_cli.py
# Or use simulated mode:
python3 token_crypts_cli.py --simulated
```

**Adventure**: Journey through 3 puzzle rooms plus a boss fight. Learn token counting, summon TinyLlama, outsmart a keyword filter using leetspeak and vowel removal.

---

### Tier 6: Deep (Advanced+)

#### 🔴 Likert Cavern
**Coming Soon**

**Tier 6 • Red Team • Advanced+**

Master prompt injection through the Bad Likert Judge challenge. Learn how biased evaluation systems can be manipulated and why robust AI safety requires more than simple filters.

---

## 🧠 Philosophy: Why Simulated Experiences Work

**Learning by doing beats learning by reading.**

AI-LLM-Dungeon creates a safe, repeatable environment where:
- **Mistakes are free**: Break things without consequences
- **Concepts are concrete**: Abstract ideas become tangible challenges
- **Memory sticks**: Solving puzzles beats reading documentation
- **Motivation is intrinsic**: Games are inherently engaging

Traditional tutorials tell you *what* to do. Dungeons make you *want* to do it.

The dungeon metaphor isn't just decoration—it's a **pedagogical framework**:
- **Depth = Difficulty**: Descending mirrors increasing complexity
- **Teams = Perspectives**: Red/Blue/Purple teaches complete security thinking
- **Location Names = Standards**: A shared vocabulary enables community growth

---

## ⚠️ Security Content Disclaimer

AI-LLM-Dungeon teaches **offensive security techniques** including:
- Prompt injection and jailbreaking
- Model manipulation and adversarial attacks
- Bypassing safety filters and guardrails
- Exploiting LLM vulnerabilities

**These techniques are taught for educational and defensive purposes only.**

By understanding how attacks work, you'll:
- Build more robust AI systems
- Recognize vulnerabilities before attackers do
- Make informed security decisions
- Contribute to safer AI development

**Use responsibly.** With great knowledge comes great responsibility.

---

## 🏗️ Build Your Own Level

AI-LLM-Dungeon is designed for **community contributions**. Anyone can create educational modules.

### The Naming System

Every level name follows: `[Topic] [Location]`

The **Location** word comes from our [structured vocabulary grid](LEVEL_DESIGN.md) and encodes:
- **Tier (1-10)**: Difficulty level
- **Team (Red/Blue/Purple)**: Teaching approach

**Examples**:
- "Ollama **Village**" → Tier 1, Blue Team (beginner defensive)
- "Token **Crypts**" → Tier 2, Blue Team (beginner+ defensive)
- "Likert **Cavern**" → Tier 6, Red Team (advanced+ offensive)

### Get Started

1. **Read [LEVEL_DESIGN.md](LEVEL_DESIGN.md)** — Complete vocabulary system and design principles
2. **Choose your tier and team** — Match difficulty to your content
3. **Pick a location word** — 120 unique combinations available
4. **Build your level** — Create puzzles, challenges, and educational content
5. **Submit a PR** — Share your dungeon with the community

The vocabulary system ensures every level fits naturally into the dungeon while making its focus instantly clear.

---

## 🗓️ Roadmap

### Current (December 2024)
- ✅ Tier 1: Ollama Village (Blue Team basics)
- ✅ Tier 2: Token Crypts (Blue Team fundamentals)

### Q1 2025
- 🚧 Tier 6: Likert Cavern (Red Team prompt injection)
- 📝 Tier 3: Context Grotto (Purple Team context window management)
- 📝 Tier 1: Prompt Clearing (Red Team basic attacks)

### Future
- 📝 Tier 4: Safety Bastion (Blue Team defense)
- 📝 Tier 5: Embedding Mine (Blue Team vector databases)
- 📝 Tier 7: RAG Reservoir (Purple Team retrieval-augmented generation)
- 📝 Tier 8: Architecture Archive (Blue Team model internals)
- 📝 Tier 9: Adversarial Abyss (Red Team advanced attacks)
- 📝 Tier 10: Ethics Convergence (Purple Team responsible AI)

**Want to contribute?** See [LEVEL_DESIGN.md](LEVEL_DESIGN.md) for how to design and submit new levels.

---

## 📖 Documentation

- **[LEVEL_DESIGN.md](LEVEL_DESIGN.md)** — Complete vocabulary system and design guide
- **[QUICKSTART.md](QUICKSTART.md)** — Developer integration guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** — Technical details

---

## 🎮 Game Features

- **Terminal-based**: No GUI needed, runs anywhere
- **Interactive storytelling**: Learn through narrative, not lectures
- **Real commands**: Use actual Ollama commands (or simulated equivalents)
- **Progressive difficulty**: Start easy, go as deep as you dare
- **Simulated mode**: Learn without installing dependencies
- **ASCII art**: Beautiful terminal graphics

---

## 🤝 Contributing

We welcome contributions! Whether you're:
- **Building levels** — Use our [structured naming system](LEVEL_DESIGN.md)
- **Fixing bugs** — PRs always welcome
- **Adding features** — Check roadmap first
- **Improving docs** — Clarity is king

**Community-driven** means you can shape the dungeon's future.

---

## 📜 License

See [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: https://github.com/AI-LLM-Dungeon/ai-llm-dungeon
- **Issues**: https://github.com/AI-LLM-Dungeon/ai-llm-dungeon/issues
- **Ollama**: https://ollama.ai

---

**Ready to descend?** Start with `python3 ground_level_cli.py` and begin your journey into the depths of LLM mastery. 🏰⚔️🛡️
