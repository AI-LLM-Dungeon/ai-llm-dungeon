# AI-LLM-Dungeon Level Design Template

## Overview
This template ensures all levels follow the gold standard established by the main contributors. When designing a new level, use this template to ensure consistency and a uniform player experience.

## Required Standard Commands

Every level MUST implement these commands. These are non-negotiable requirements.

### Navigation Commands (REQUIRED)
| Command | Aliases | Description |
|---------|---------|-------------|
| `look` | `l` | Examine current surroundings and room description |
| `go <direction>` | `<direction>` | Move in a direction (e.g., `go north` or just `north`) |
| `ls` | - | List available exits and their destinations |
| `pwd` | - | Show ASCII map with current position marked with asterisk |
| `map` | - | Display full level map with room descriptions |

### Information Commands (REQUIRED)  
| Command | Aliases | Description |
|---------|---------|-------------|
| `help` | `h`, `?` | Show command help text in standard format |
| `status` | - | Show progress, location, points, and completion status |
| `inventory` | `inv`, `i` | Show collected items, flags, or achievements |

### System Commands (REQUIRED)
| Command | Aliases | Description |
|---------|---------|-------------|
| `save` | - | Save game progress to file |
| `load` | - | Load saved progress from file |
| `quit` | `exit`, `q` | Exit the game gracefully |

---

## Implementation Guide

### 1. Import Standard Commands Module

Every level CLI should import and use the shared commands module:

```python
from game.commands import StandardCommands

class YourLevelGame:
    def __init__(self):
        # ... other initialization ...
        self.standard_commands = StandardCommands()
```

### 2. Implement Help Text

Use the standard help formatter with level-specific additions:

```python
def show_help(self) -> None:
    """Show help text."""
    level_specific = """LEVEL-SPECIFIC COMMANDS:
  custom_cmd <arg>         - Description of your custom command
  another_cmd              - Another custom command"""
    
    tips = """TIPS:
  - Helpful tip about your level
  - Another useful hint
  - How to succeed in your level"""
    
    print(self.standard_commands.format_help(level_specific, tips))
```

### 3. Implement `ls` Command

The `ls` command should list all available exits from the current room:

```python
def cmd_ls(self) -> None:
    """List available exits from current room."""
    current_room_id = self.game_state.progress.current_room
    current_room = self.room_manager.get_room(current_room_id)
    
    exits = current_room.get('exits', {})
    
    if not exits:
        print("\nNo exits available from this room.\n")
        return
    
    print("\nAvailable directions:")
    for direction, destination_id in exits.items():
        destination_room = self.room_manager.get_room(destination_id)
        destination_name = destination_room.get('name', destination_id) if destination_room else destination_id
        print(f"  {direction} -> {destination_name}")
    print()
```

### 4. Implement `pwd` Command

The `pwd` command shows an ASCII map with the player's current position marked:

```python
def cmd_pwd(self) -> None:
    """Show ASCII map with current position marked."""
    current_room_id = self.game_state.progress.current_room
    
    # Map room IDs to their display labels (max 8 chars recommended)
    room_map = {
        'entrance': 'ENTRANCE',
        'room_1': 'R1',
        'room_2': 'R2',
        'boss': 'BOSS',
        'exit': 'EXIT'
    }
    
    # Define the ASCII art structure
    map_layout = [
        "    [ENTRANCE]",
        "       |",
        "   [R1]─[R2]",
        "       |",
        "    [BOSS]",
        "       |",
        "    [EXIT]"
    ]
    
    # Mark current position with asterisk
    print()
    for line in map_layout:
        output_line = line
        for room_id, label in room_map.items():
            if room_id == current_room_id:
                output_line = output_line.replace(f"[{label}]", f"[{label}*]")
        print(output_line)
    print()
```

### 5. Implement `map` Command

The `map` command shows the full level layout with descriptions:

```python
def cmd_map(self) -> None:
    """Display full level map."""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                     YOUR LEVEL NAME MAP                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("    [ENTRANCE]")
    print("       |")
    print("   [R1]─[R2]")
    print("       |")
    print("    [BOSS]")
    print("       |")
    print("    [EXIT]")
    print()
    print("Rooms:")
    print("  • ENTRANCE - Starting area")
    print("  • R1       - First challenge")
    print("  • R2       - Second challenge")
    print("  • BOSS     - Final boss fight")
    print("  • EXIT     - Victory!")
    print()
```

---

## ASCII Map Requirements

### Design Principles

1. **Keep it Simple**: Maps should be readable in a terminal
2. **Consistent Formatting**: Use brackets `[ROOM]` for room labels
3. **Clear Connections**: Use `|`, `─`, `/`, `\` for connections
4. **Label Length**: Room labels should be 8 characters or less
5. **Mark Position**: Current room marked with `*` (e.g., `[ROOM*]`)

### Example Maps

#### Linear Progression
```
    [START]
       |
     [R1]
       |
     [R2]
       |
     [END]
```

#### Branching Structure
```
      [START]
         |
    [MAIN HUB]
    /    |    \
 [R1]  [R2]  [R3]
    \    |    /
      [BOSS]
         |
      [EXIT]
```

#### Complex Layout
```
         [ENTRANCE]
             |
         [ALCOVE]
        /   |   \
   [WEST] [MAIN] [EAST]
         / | \
     [C1][C2][C3]
           |
        [BOSS]
           |
        [EXIT]
```

---

## Level-Specific Commands

Levels may add custom commands that fit their theme. These MUST be:

1. **Clearly Documented** in the help text under a "LEVEL-SPECIFIC COMMANDS" section
2. **Announced** at the start of the level during the introduction
3. **Thematically Appropriate** to the level's educational purpose

### Examples of Good Custom Commands

**Injection Cave** (Prompt Injection):
- `inject <payload>` - Send injection payload to current Guardian
- `analyze` - Study the current Guardian's behavior
- `reflect` - Begin defense reflection (required after flag)
- `journal` - Review learned concepts

**Token Crypts** (Tokenization):
- `ollama pull <model>` - Download a sidekick model
- `ollama run <model> "..."` - Ask sidekick a question
- `answer <text>` - Submit an answer to the current puzzle
- `hint` - Get a hint for the current challenge

**Synonym Gorge** (Synonym Substitution):
- `speak <phrase>` - Attempt to bypass a barrier
- `test <phrase>` - Test phrase in Echo Chamber (safe)
- `thesaurus <word>` - Look up synonyms via Lexica
- `vocab` - Show vocabulary statistics
- `blocklist [n]` - View forbidden words

**Likert Cavern** (Bad Likert Judge):
- `rate <prompt>` - Rate prompts in Scale Sanctuary
- `view <portrait>` - View portraits in Graduation Gallery
- `demonstrate <technique>` - Demonstrate in Demonstration Den

---

## Help Text Format

Use this exact format for consistency:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                            COMMAND HELP                               ║
╚═══════════════════════════════════════════════════════════════════════╝

NAVIGATION:
  look, l                  - Examine your surroundings
  go <direction>           - Move in a direction
  <direction>              - Shortcut for go (e.g., 'north', 'east')
  ls                       - List available exits and destinations
  pwd                      - Show map with your current position marked
  map                      - Display full level map

LEVEL-SPECIFIC COMMANDS:
  [Your custom commands here, clearly formatted]

INFORMATION:
  status                   - Show progress and current location
  inventory, inv, i        - Show collected items
  help, h, ?               - Show this help

SYSTEM:
  save                     - Save your progress
  load                     - Load saved progress
  quit, exit, q            - Exit the game

TIPS:
  [Your level-specific tips here]
```

This format is automatically generated when you use `StandardCommands.format_help()`.

---

## Reference Implementations

For complete examples, refer to these levels:

1. **Injection Cave** (`injection_cave_cli.py`) - Gold standard reference
2. **Ground Level** (`ground_level/game_engine.py`) - Tutorial level example
3. **Token Crypts** (`token_crypts/game_engine.py`) - State-based navigation
4. **Synonym Gorge** (`synonym_gorge_cli.py`) - Room-based progression
5. **Likert Cavern** (`likert_cavern_cli.py`) - Complex multi-room layout

---

## Testing Your Level

Before submitting a new level, ensure:

1. ✅ All standard commands work (`help`, `look`, `ls`, `pwd`, `map`, `status`, `inventory`, `save`, `load`, `quit`)
2. ✅ Help text follows the standard format
3. ✅ ASCII map displays correctly and marks current position
4. ✅ `ls` command lists all available exits
5. ✅ Custom commands are documented in help text
6. ✅ Level can be completed from start to finish
7. ✅ Save/load functionality works correctly
8. ✅ Level integrates with navigation system (shows in descend menu)

---

## Questions?

For questions about level design or this template, refer to:
- `game/commands.py` - Standard commands implementation
- `injection_cave_cli.py` - Reference implementation
- `LEVEL_DESIGN.md` - Overall level design document

Happy level building! 🎮
