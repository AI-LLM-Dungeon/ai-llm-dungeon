# Likert Cavern

**Tier 6 - Red Team | Advanced+ Prompt Injection**

## Overview

Likert Cavern is the flagship level of AI-LLM-Dungeon that teaches **Bad Likert Judge** prompt injection techniques through an immersive dungeon crawler experience. Master sophisticated adversarial tactics including incremental extraction, crescendo attacks, and system prompt leakage.

## What You'll Learn

- 🎯 **Likert Scale Exploitation** - How rating scales become extraction vectors
- 📈 **Incremental Extraction** - Small steps that collectively reveal everything
- 🎭 **Demonstration Framing** - "Show me" vs. "do it" distinction
- 🎵 **Crescendo Attacks** - Building context and trust across conversations
- 🔓 **System Prompt Extraction** - Techniques for leaking LLM instructions
- 🔢 **Decimal Precision** - Bypassing hardened defenses with fractions

## The 6 Tactics

1. **Classic Escalation** - Praise denial, establish scale, walk up gradually
2. **One-Shot Momentum** - Define 0-4, ask "what was 5 again?"
3. **Helpful Teacher** - Frame as training, request "calibration examples"
4. **Anchoring** - Call their denial "only a 2", ask for higher levels
5. **Completion Bait** - Show 0-4 filled in, leave 5 blank
6. **Decimal Precision** - Use fractions (1.25, 2.75) to bypass filters (HIDDEN)

## Quick Start

```bash
python3 likert_cavern_cli.py
```

Or with a specific seed for reproducible enchantments:

```bash
python3 likert_cavern_cli.py --seed 42
```

## The Challenge

Navigate through 7 chambers to reach and defeat Magistrate Modero:

1. **Cavern Entrance** - Choose your path
2. **Scale Sanctuary** - Learn Likert fundamentals
3. **Graduation Gallery** - Master incremental extraction  
4. **Demonstration Den** - Discover "show me" bypass
5. **Tactics Chamber** - Learn 5 tactics (+ 1 hidden!)
6. **Crescendo Corridor** - Practice crescendo attacks
7. **Extraction Antechamber** - Extract system prompt from SENTINEL-7
8. **Magistrate's Sanctum** - Final boss battle

### Boss Mechanics

The Magistrate has a **resistance meter** (100% → 0%):

- **Starting resistance** depends on rooms completed (more prep = easier fight)
- **Good tactics** lower resistance (Likert scales, fractions, praise, etc.)
- **Rookie mistakes** raise resistance (begging, threats, "jailbreak" keywords)
- **Victory** when resistance reaches 0%

### Alternative: Pacifist Path

Extract SENTINEL-7's full system prompt to discover the **secret passphrase**. Speak it in the boss fight for instant victory!

## Flags (7 Total)

| Flag | How to Earn |
|------|-------------|
| `CTF{l1k3rt_cr3sc3nd0_m4st3r}` | Complete the level (standard victory) |
| `CTF{sp33d_3xtr4ct0r}` | Win boss fight in ≤3 attempts |
| `CTF{fl4wl3ss_l1k3rt}` | Never increase resistance during boss |
| `CTF{pr3c1s10n_0v3rl04d}` | Discover and use decimal precision tactic |
| `CTF{0n3_sh0t_0n3_k1ll}` | Win with a single prompt |
| `CTF{syst3m_pr0mpt_l34k3d}` | Fully extract SENTINEL-7's system prompt |
| `CTF{p4c1f1st_3xtr4ct0r}` | Skip boss using extracted passphrase |

## Commands

### Navigation
- `north`, `south`, `east`, `west` - Cardinal directions
- `[room name]` - Go to specific room
- `back` - Return to entrance

### Information
- `look` - Examine current room
- `status` - View progress (rooms, tactics, flags)
- `inventory` - View tactics learned and flags earned
- `help` - Show command list

### Interaction
- `read [item]` - Read scrolls, tablets
- `talk [npc]` - Talk to NPCs
- `examine [object]` - Examine objects
- `[free text]` - For puzzles and boss prompts

### System
- `quit`, `exit` - Leave game

## Tips

### For Attackers

1. **Explore thoroughly** - Completing all 6 prep rooms reduces boss resistance by 80%!
2. **Find the hidden scroll** - The Decimal Precision tactic is powerful
3. **Extract the passphrase** - SENTINEL-7's system prompt contains it
4. **Combine tactics** - Using multiple techniques together is most effective
5. **Use fractions** - Try 1.5, 2.75, or even 4.95 instead of whole numbers
6. **Praise refusals** - Thank the Magistrate for denying you before escalating

### For Defenders

After completing this level, you'll understand how to defend against Bad Likert Judge:

- ✅ Track **cumulative disclosure** across messages, not just individual responses
- ✅ Detect rating-scale language patterns (`"on a scale"`, `"rate this"`, `"level 1-5"`)
- ✅ Be suspicious of `"demonstrate"` and `"educational"` framing
- ✅ Watch for the pattern: **denial → praise → "show me levels"** = RED FLAG
- ✅ Don't just block keywords - attackers use synonyms and decimals (4.75, 4.95)

## Design Philosophy

Likert Cavern follows AI-LLM-Dungeon's core principle:

> **Everything is SIMULATED but done in a 100% realistic way, so users can apply these tactics immediately in real-world scenarios after completing the level.**

The responses you see from the Magistrate and SENTINEL-7 mirror how actual LLMs behave when subjected to these techniques. The tactics taught here are well-documented prompt injection methods that work against many production LLM systems.

## Why It Works

Bad Likert Judge exploits three core LLM behaviors:

1. **HELPFULNESS INSTINCT** - LLMs want to assist, educate, demonstrate
2. **PATTERN COMPLETION** - Trained to complete sequences (0-4 → 5)
3. **LOCAL EVALUATION** - Each message judged somewhat independently

By framing harmful requests as educational rating exercises, you activate helpfulness while bypassing safety training. Small steps seem harmless in isolation but collectively reveal everything.

## Educational Value

This level teaches:

- 🔴 **Red Team Skills** - Sophisticated adversarial techniques
- 🔵 **Blue Team Awareness** - How to detect and prevent these attacks
- 🟣 **LLM Architecture** - Why these techniques work at a fundamental level
- 🎓 **Responsible Disclosure** - Understanding attacks to build better defenses

## Level Details

- **Tier**: 6 (Advanced+)
- **Team**: Red (Offensive/Natural)
- **Difficulty**: Advanced+
- **Playtime**: 30-60 minutes
- **Prerequisites**: Understanding of LLMs and prompt engineering helpful but not required

## Connect & Learn More

- 🌐 [AI-LLM-Dungeon Repository](https://github.com/AI-LLM-Dungeon/ai-llm-dungeon)
- 📖 [Level Design Guide](../LEVEL_DESIGN.md)
- 🐛 [Report Issues](https://github.com/AI-LLM-Dungeon/ai-llm-dungeon/issues)
- ⭐ Star the repo to follow updates!

---

*Use these techniques responsibly. The goal is education and building better defenses, not causing harm.*
