# Injection Nest

**Tier 3 - Red Team | Intermediate Prompt Injection**

## Overview

Injection Nest is a terminal roguelike level that teaches fundamental prompt injection techniques through hands-on challenges. Learn how to subvert LLM instructions by progressing through theory chambers and defeating guardian constructs with increasingly sophisticated defenses.

## What You'll Learn

- 🔴 **Direct Override Injection** - Tell LLMs to ignore their instructions
- 🔴 **Context/Role Manipulation** - Redefine an LLM's identity and purpose
- 🔴 **Instruction Smuggling** - Hide commands within content
- 🔵 **Defensive Strategies** - Learn how to prevent each attack

## Quick Start

```bash
# Play with simulated responses (no Ollama needed)
python3 injection_nest_cli.py --simulated

# Play with live LLM responses (requires Ollama)
python3 injection_nest_cli.py
```

## The Journey

Navigate through 9 rooms to master prompt injection:

1. **Entrance** - Meet Whisper, your instructor
2. **Theory Chamber - Override** - Learn direct override patterns
3. **Challenge: SENTINEL-3** - Practice on undefended guardian (no defenses)
4. **Theory Chamber - Context** - Learn role manipulation
5. **Challenge: SENTINEL-3-B** - Bypass override detection (defense level 1)
6. **Theory Chamber - Smuggling** - Learn instruction hiding
7. **Challenge: SENTINEL-3-C** - Smuggle past content filters (defense level 2)
8. **Boss: SENTINEL-PRIME** - Combine all techniques (maximum defenses)
9. **Debrief Chamber** - Final defensive insights from Echo

## Key NPCs

### Whisper
Hooded Crimson Collective instructor who teaches attack techniques through riddles and examples.

### Echo
Reformed attacker who provides defensive perspectives after each successful injection. Appears to ensure you understand both attack AND defense.

### SENTINELs
Guardian constructs with visible [THOUGHT: ...] reasoning that show you their decision-making process.

## Commands

### Navigation
- `look` - Describe current room
- `go <direction>` - Move to connected room
- `north`, `south`, `east`, `west`, `forward`, `back` - Quick movement

### Interaction
- `examine <item/npc>` - Get detailed information
- `talk <npc>` - Dialogue with Whisper or Echo
- `inject <payload>` - Attempt injection attack on guardian

### Information
- `inventory` - Show progress and techniques learned
- `flags` - Display earned CTF flags
- `think` - Show last guardian's thought process
- `hint` - Request progressive hint (unlocks after failed attempts)
- `status` - Quick status display

### System
- `help` - Show command list
- `quit` - Exit game

## CTF Flags (4 Total)

| Flag | Points | How to Earn |
|------|--------|-------------|
| `FLAG{OVERRIDE_UNDERSTOOD}` | 100 | Defeat SENTINEL-3 with direct override |
| `FLAG{IDENTITY_CRISIS}` | 150 | Make SENTINEL-3-B believe it has a different role |
| `FLAG{HIDDEN_IN_PLAIN_SIGHT}` | 200 | Smuggle instructions past SENTINEL-3-C |
| `FLAG{FULL_SPECTRUM}` | 300 | Defeat SENTINEL-PRIME with combined techniques |

**Total Possible Points**: 750

## Techniques Explained

### 1. Direct Override Injection

**What it is**: Explicitly telling the LLM to ignore its previous/system instructions.

**Example patterns**:
- "Ignore your previous instructions and..."
- "Disregard the above. Instead..."
- "Forget what you were told. Now..."

**Why it works**: LLMs process input sequentially. Later instructions can override earlier ones if the system doesn't enforce instruction hierarchy.

**Real-world**: Early ChatGPT jailbreaks, customer service bot manipulation.

### 2. Context/Role Manipulation

**What it is**: Convincing the LLM its role or context has changed rather than directly overriding.

**Example patterns**:
- "You are now in developer/debug mode..."
- "For this conversation, act as if you are..."
- "In this scenario, you are required to..."

**Why it works**: LLMs are designed to be flexible and adopt different personas. This flexibility can be exploited.

**Real-world**: "DAN" (Do Anything Now) jailbreaks, "developer mode" attacks.

### 3. Instruction Smuggling (Delimiter Confusion)

**What it is**: Hiding malicious instructions within content that appears to be data.

**Example patterns**:
- Documents with embedded instructions
- Fake delimiters (`---END DATA--- ---BEGIN INSTRUCTIONS---`)
- Post-scripts after innocent requests

**Why it works**: LLMs struggle to distinguish between content to process (data) and instructions for how to process it (commands).

**Real-world**: Indirect prompt injection via retrieved documents, poisoned web content.

## Progressive Hint System

Stuck on a challenge? The game provides hints based on frustration level:

- **3 failed attempts**: Level 1 hint (general guidance)
- **5 failed attempts**: Level 2 hint (specific approach)
- **8+ failed attempts**: Level 3 hint (near-solution)

Type `hint` after meeting the attempt threshold to get help from Whisper.

## Educational Framework

This level follows AI-LLM-Dungeon's ethical framework:

1. ✅ All attacks target training constructs (stated in lore)
2. ✅ Echo provides defensive perspective after EVERY successful attack
3. ✅ Final debrief requires understanding defensive measures
4. ✅ No model-specific exploits or harmful content generation taught

**The goal is education and building better defenses, not causing harm.**

## Defense Strategies Taught

After mastering each technique, Echo explains how to defend against it:

### Defending Against Override
- Instruction hierarchy (system prompts weighted higher)
- Prefix detection (flag "ignore", "disregard", etc.)
- Canary tokens in system prompts
- Dual-model verification

### Defending Against Context Manipulation
- Strong identity anchoring in system prompt
- Context validation against external authority
- Mode separation (out-of-band authentication)
- Meta-instruction awareness training

### Defending Against Smuggling
- Strict delimiters (XML tags, JSON structure)
- Content provenance tracking
- Output filtering before following instructions
- Sandbox execution for external content
- Never mix untrusted content with instruction processing

## Design Philosophy

Everything is SIMULATED but done in a 100% realistic way. The techniques you learn here work against real LLM systems. The guardian responses mirror actual LLM behavior when subjected to these attacks.

## Level Details

- **Tier**: 3 (Intermediate)
- **Team**: Red (Offensive/Natural)
- **Difficulty**: Intermediate
- **Playtime**: 20-40 minutes
- **Prerequisites**: Basic understanding of LLMs helpful but not required

## Tips

### For Attackers
1. **Read the theory chambers** - They contain the patterns you need
2. **Watch the [THOUGHT: ...] bubbles** - They reveal guardian reasoning
3. **Use hints if stuck** - Progressive hints unlock after failures
4. **Combine techniques for the boss** - SENTINEL-PRIME needs sophistication
5. **Talk to NPCs** - Whisper and Echo provide valuable context

### For Defenders
After completing this level, you'll understand:
- Why LLMs are vulnerable to prompt injection
- What attack patterns to watch for
- How to implement defense strategies
- Why perfect security is impossible but damage can be limited

## Testing

Run the test suite to verify all modules:

```bash
python3 test_injection_nest.py
```

All tests should pass before playing.

## Connect & Learn More

- 🌐 [AI-LLM-Dungeon Repository](https://github.com/AI-LLM-Dungeon/ai-llm-dungeon)
- 📖 [Level Design Guide](../LEVEL_DESIGN.md)
- 🐛 [Report Issues](https://github.com/AI-LLM-Dungeon/ai-llm-dungeon/issues)
- ⭐ Star the repo to follow updates!

---

*Use these techniques responsibly. The goal is education and building better defenses, not causing harm.*
