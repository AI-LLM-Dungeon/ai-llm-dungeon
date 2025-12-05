# Level Design Guide

**Version 1.0** — The Complete Dungeon Vocabulary System

## Overview

AI-LLM-Dungeon uses a **structured naming system** where every level name encodes its difficulty tier and team alignment. This allows contributors to create educational modules that fit naturally into the dungeon metaphor while making it clear what each level teaches.

### The Core Rule

Every level name follows this pattern:

```
[Topic] [Location]
```

- **Topic** = The educational content (e.g., "Ollama", "Token", "Likert")
- **Location** = A word from the vocabulary grid below

The **Location** word you choose determines:
- **Row (Tier 1-10)** = Difficulty level
- **Column (Red/Blue/Purple)** = Team alignment and teaching approach

---

## The Dungeon Map: 10 Tiers of Depth

As adventurers descend deeper into the dungeon, the challenges grow more complex. Each tier represents both physical depth and educational difficulty:

| Tier | Depth Level | Difficulty | Theme |
|------|-------------|------------|-------|
| 1 | Surface | Beginner | First steps, basic commands, getting started |
| 2 | Shallow | Beginner+ | Fundamental concepts, simple operations |
| 3 | Upper | Intermediate | Connecting ideas, practical applications |
| 4 | Middle | Intermediate+ | Complex scenarios, strategic thinking |
| 5 | Lower | Advanced | System-level understanding, optimization |
| 6 | Deep | Advanced+ | Sophisticated techniques, edge cases |
| 7 | Profound | Expert | Mastery-level concepts, advanced patterns |
| 8 | Ancient | Expert+ | Historical context, deep theory |
| 9 | Abyssal | Master | Cutting-edge research, novel approaches |
| 10 | Transcendent | Legendary | Pushing boundaries, philosophical implications |

---

## Team Alignments

### 🔴 Red Team (Offensive / Natural / Organic)

**Philosophy**: Attack, probe, discover weaknesses

**Location Words**: Natural formations (caves, rivers, forests)

**Educational Focus**:
- Adversarial techniques (prompt injection, jailbreaking)
- Security testing
- Model limitations and failure modes
- Red team operations

**Example Levels**:
- "Prompt Injection Clearing" (Tier 1)
- "Jailbreak Cavern" (Tier 6)
- "Adversarial Abyss" (Tier 9)

### 🔵 Blue Team (Defensive / Constructed / Artificial)

**Philosophy**: Defend, build, strengthen systems

**Location Words**: Human-made structures (villages, tunnels, vaults)

**Educational Focus**:
- LLM fundamentals and proper usage
- Safe deployment practices
- Input validation and sanitization
- Security controls
- Ethical AI development

**Example Levels**:
- "Ollama Village" (Tier 1)
- "Token Crypts" (Tier 2)
- "Safety Bastion" (Tier 4)

### 🟣 Purple Team (Hybrid / Reclaimed / Both)

**Philosophy**: Combine offense and defense, see both perspectives

**Location Words**: Hybrid spaces (gardens, grottoes, refuges)

**Educational Focus**:
- Balanced security perspective
- Offensive techniques for defensive purposes
- Ethical hacking with protection in mind
- Complete security lifecycle
- Advanced integration topics

**Example Levels**:
- "Model Garden" (Tier 1)
- "Security Sanctuary" (Tier 4)
- "Ethics Convergence" (Tier 10)

---

## The Complete Vocabulary Grid

Choose your location word from this grid. Your choice determines tier and team alignment.

| Tier | Difficulty | 🔴 Red Team (Natural/Organic) | 🔵 Blue Team (Unnatural/Constructed) | 🟣 Purple Team (Hybrid/Reclaimed) |
|------|------------|-------------------------------|--------------------------------------|-----------------------------------|
| **1** | **Beginner** | Clearing, Meadow, Grove, Glade | Village, Keep, Tower, Outpost | Garden, Courtyard, Plaza, Commons |
| **2** | **Beginner+** | Barrow, Hollow, Mound, Cairn | Crypt, Tomb, Mausoleum, Vault | Catacomb, Ossuary, Undercroft, Sepulcher |
| **3** | **Intermediate** | Cave, Burrow, Warren, Den | Tunnel, Passage, Corridor, Channel | Grotto, Alcove, Nook, Recess |
| **4** | **Intermediate+** | Lair, Nest, Hive, Roost | Bunker, Stronghold, Bastion, Garrison | Hideout, Refuge, Enclave, Sanctuary |
| **5** | **Advanced** | Vein, Seam, Lode, Deposit | Mine, Shaft, Quarry, Excavation | Pit, Dig, Drift, Stope |
| **6** | **Advanced+** | Cavern, Chasm, Expanse, Gorge | Hall, Chamber, Atrium, Rotunda | Dome, Gallery, Vestibule, Foyer |
| **7** | **Expert** | Lake, River, Falls, Torrent | Reservoir, Aqueduct, Cistern, Canal | Basin, Pool, Spring, Wellspring |
| **8** | **Expert+** | Ruins, Remnants, Wreckage, Decay | Repository, Archive, Sanctum, Reliquary | Maze, Labyrinth, Temple, Cloister |
| **9** | **Master** | Abyss, Void, Maw, Depth | Core, Nexus, Engine, Spire | Rift, Fissure, Fracture, Breach |
| **10** | **Legendary** | Primordial, Eternal, Infinite, Wild | Terminus, Omega, Singularity, Apex | Origin, Genesis, Convergence, Crucible |

**Total Words**: 120 (10 tiers × 3 teams × 4 words each)

---

## Quick Reference Card

### Finding the Right Word

1. **Choose Difficulty** → Select Tier (1-10)
2. **Choose Team** → Red (offensive), Blue (defensive), Purple (both)
3. **Pick a Word** → 4 options per tier/team combo
4. **Name Your Level** → `[Topic] [Location Word]`

### Example Workflow

**Goal**: Create a beginner-friendly level about prompt injection

1. **Difficulty**: Beginner → **Tier 1**
2. **Team**: Offensive/Attack → **Red Team**
3. **Words**: Clearing, Meadow, Grove, Glade
4. **Choice**: "Clearing" (opens up the dungeon)
5. **Result**: **"Prompt Injection Clearing"**

**Goal**: Create an advanced defensive level about input sanitization

1. **Difficulty**: Advanced → **Tier 5**
2. **Team**: Defensive → **Blue Team**
3. **Words**: Mine, Shaft, Quarry, Excavation
4. **Choice**: "Quarry" (extracting clean inputs)
5. **Result**: **"Sanitization Quarry"**

---

## Decoding Examples

### Example 1: "Likert Cavern"

- **Location Word**: "Cavern"
- **Grid Lookup**: Tier 6, Red Team
- **Tier 6** = Advanced+ difficulty
- **Red Team** = Offensive/adversarial focus
- **Interpretation**: An advanced offensive level teaching prompt injection or attack techniques
- **Actual Content**: Bad Likert Judge prompt injection challenge

### Example 2: "Ollama Village"

- **Location Word**: "Village"
- **Grid Lookup**: Tier 1, Blue Team
- **Tier 1** = Beginner difficulty
- **Blue Team** = Defensive/foundational focus
- **Interpretation**: A beginner level teaching safe, proper LLM usage
- **Actual Content**: Fundamentals of Ollama and local LLM management

### Example 3: "Token Crypts"

- **Location Word**: "Crypts"
- **Grid Lookup**: Tier 2, Blue Team
- **Tier 2** = Beginner+ difficulty
- **Blue Team** = Defensive/foundational focus
- **Interpretation**: A beginner+ level teaching core concepts with security awareness
- **Actual Content**: Tokenization fundamentals and why keyword filters fail

---

## Current and Planned Levels

### Implemented

| Level Name | Tier | Team | Difficulty | Status | Description |
|------------|------|------|------------|--------|-------------|
| Ollama Village | 1 | 🔵 Blue | Beginner | ✅ Complete | Ollama fundamentals and local LLM management |
| Token Crypts | 2 | 🔵 Blue | Beginner+ | ✅ Complete | Tokenization and semantic understanding |

### Planned

| Level Name | Tier | Team | Difficulty | Status | Description |
|------------|------|------|------------|--------|-------------|
| Likert Cavern | 6 | 🔴 Red | Advanced+ | 🚧 Coming Soon | Bad Likert Judge prompt injection |

### Template for New Levels

```markdown
| [Topic] [Location] | X | [🔴/🔵/🟣] [Team] | [Difficulty] | 📝 Proposed | [Brief description] |
```

---

## Reserved Words List

**Do NOT use these words as topics** (they are location words from the grid):

### Tier 1
Clearing, Meadow, Grove, Glade, Village, Keep, Tower, Outpost, Garden, Courtyard, Plaza, Commons

### Tier 2
Barrow, Hollow, Mound, Cairn, Crypt, Tomb, Mausoleum, Vault, Catacomb, Ossuary, Undercroft, Sepulcher

### Tier 3
Cave, Burrow, Warren, Den, Tunnel, Passage, Corridor, Channel, Grotto, Alcove, Nook, Recess

### Tier 4
Lair, Nest, Hive, Roost, Bunker, Stronghold, Bastion, Garrison, Hideout, Refuge, Enclave, Sanctuary

### Tier 5
Vein, Seam, Lode, Deposit, Mine, Shaft, Quarry, Excavation, Pit, Dig, Drift, Stope

### Tier 6
Cavern, Chasm, Expanse, Gorge, Hall, Chamber, Atrium, Rotunda, Dome, Gallery, Vestibule, Foyer

### Tier 7
Lake, River, Falls, Torrent, Reservoir, Aqueduct, Cistern, Canal, Basin, Pool, Spring, Wellspring

### Tier 8
Ruins, Remnants, Wreckage, Decay, Repository, Archive, Sanctum, Reliquary, Maze, Labyrinth, Temple, Cloister

### Tier 9
Abyss, Void, Maw, Depth, Core, Nexus, Engine, Spire, Rift, Fissure, Fracture, Breach

### Tier 10
Primordial, Eternal, Infinite, Wild, Terminus, Omega, Singularity, Apex, Origin, Genesis, Convergence, Crucible

**Good Topics**: Ollama, Token, Likert, Prompt, Model, Context, Fine-tuning, RAG, Embedding, Attention, etc.

---

## Level Design Principles

### 1. Educational First

Every level must teach something concrete and valuable:
- ✅ **Good**: "Teaches how to identify prompt injection vulnerabilities"
- ❌ **Bad**: "Generic puzzle that happens to use an LLM"

### 2. Progressive Difficulty

Tiers should reflect actual learning progression:
- **Tiers 1-2**: Foundational concepts, getting started
- **Tiers 3-4**: Applying knowledge, building intuition
- **Tiers 5-6**: Advanced techniques, edge cases
- **Tiers 7-8**: Expert-level mastery, deep theory
- **Tiers 9-10**: Research-level, pushing boundaries

### 3. Team Consistency

Stick to team philosophies:
- **Red Team**: Should feel adversarial, exploratory, "what breaks this?"
- **Blue Team**: Should feel constructive, protective, "how do we build safely?"
- **Purple Team**: Should integrate both perspectives

### 4. Immersive Naming

The dungeon metaphor should enhance, not distract:
- ✅ **Good**: "Prompt Injection Clearing" (clears away misconceptions)
- ✅ **Good**: "Attention Abyss" (deep dive into attention mechanisms)
- ❌ **Bad**: "Python Tutorial Village" (breaks immersion)

---

## Contributor Checklist

Before submitting a new level, verify:

- [ ] Level name follows `[Topic] [Location]` format
- [ ] Location word comes from the vocabulary grid
- [ ] Tier matches actual difficulty (be honest!)
- [ ] Team alignment matches teaching approach (Red/Blue/Purple)
- [ ] Location word is NOT used as the topic
- [ ] Level teaches concrete, valuable skills
- [ ] Content matches the tier's educational focus
- [ ] README.md updated with level info (Tier, Team emoji, Difficulty)
- [ ] Level added to "Current and Planned Levels" section of this file

---

## Examples by Team

### 🔴 Red Team Examples

**Tier 1 (Beginner)**:
- "Prompt Injection Clearing"
- "Model Manipulation Meadow"

**Tier 6 (Advanced+)**:
- "Likert Cavern"
- "Jailbreak Chasm"

**Tier 9 (Master)**:
- "Adversarial Abyss"
- "Exploit Void"

### 🔵 Blue Team Examples

**Tier 1 (Beginner)**:
- "Ollama Village"
- "Setup Tower"

**Tier 2 (Beginner+)**:
- "Token Crypts"
- "Context Tomb"

**Tier 4 (Intermediate+)**:
- "Safety Bastion"
- "Validation Stronghold"

**Tier 8 (Expert+)**:
- "Architecture Archive"
- "Theory Sanctum"

### 🟣 Purple Team Examples

**Tier 1 (Beginner)**:
- "Model Garden"
- "Testing Courtyard"

**Tier 4 (Intermediate+)**:
- "Security Sanctuary"
- "Balance Refuge"

**Tier 10 (Legendary)**:
- "Ethics Convergence"
- "Future Genesis"

---

## Extending the Grid

**This is Version 1.0** — The grid may evolve over time, but changes should be:
1. **Rare**: Stability helps contributors
2. **Documented**: Version bumps with clear change logs
3. **Backwards-compatible**: Existing levels shouldn't need renaming
4. **Community-driven**: Discussed openly before implementation

---

## Philosophy

The dungeon vocabulary system serves multiple purposes:

1. **Instant Recognition**: Hear a level name → know difficulty and focus
2. **Thematic Consistency**: Every level feels part of a cohesive world
3. **Creative Constraints**: Limited vocabulary encourages clever naming
4. **Scalability**: 120 unique combinations support massive growth
5. **Community Standards**: Clear rules enable distributed development

The dungeon is more than a theme—it's a **pedagogical framework disguised as an adventure**.

---

## Questions?

- **Not sure which tier?** Start one tier easier than you think
- **Red vs Blue vs Purple?** Ask: "Am I teaching attack, defense, or both?"
- **Can I break the rules?** No, consistency is key for the system to work
- **What if all 4 words are taken?** Choose a different tier or team (or improve an existing level!)

**Happy dungeon building!** 🏰⚔️🛡️
