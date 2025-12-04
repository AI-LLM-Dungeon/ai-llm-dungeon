# Ground Level Ollama Educational Modules

This directory contains the educational rewrite of the Ground Level tutorial, teaching players real Ollama commands through an interactive dungeon narrative.

## Overview

The Ground Level teaches five fundamental Ollama commands through a five-act quest structure:

1. **Act I: Summoner's Vestibule** - `ollama pull` and `ollama list`
2. **Act II: Hall of Mirrors** - Reading model attributes with `ollama list`
3. **Act III: Oracle's Bench** - `ollama run` with prompts
4. **Act IV: Archivist's Sanctum** - `ollama show` for model details
5. **Act V: Purge Chamber** - `ollama rm` for cleanup

## Directory Structure

```
game/
├── education/
│   ├── ollama_commands.py    # Safe subprocess wrappers for Ollama CLI
│   └── verification.py        # Helpers for validating command output
└── scenes/
    └── ground_level.py        # Scene controller orchestrating acts

content/
├── quests/
│   └── ground_level.json      # Quest definitions with all 5 acts
└── dialogue/
    └── ground_level_script.md # Narrative dialogue and prompts

docs/
└── ground-level-ollama-rewrite.md  # Complete design document
```

## Verification Modes

The system supports three modes to accommodate different environments:

### Mode A: Shell (Direct Execution)
- Executes Ollama commands via subprocess
- Most authentic learning experience
- **Requires**: Ollama installed on system

### Mode B: Paste (Output Validation)
- User executes commands in terminal
- Pastes output into game for validation
- Works in restricted environments

### Mode C: Simulated (Acknowledgment)
- Shows commands without execution
- Progress tracked without verification
- Useful for learning syntax before installation

## Quick Start

### Basic Usage

```python
from game.scenes.ground_level import GroundLevelController

# Initialize controller with chosen mode
controller = GroundLevelController(verification_mode="simulated")

# Start an act
payload = controller.start_act(1)
print(f"Title: {payload.title}")
print(f"Command: {payload.command_hint}")

# Verify completion
result = controller.verify_act(1)
print(f"Result: {result.message}")
```

### With Quest JSON

```python
controller = GroundLevelController(
    verification_mode="paste",
    quest_json_path="content/quests/ground_level.json"
)
```

### Shell Mode (Automatic Execution)

```python
from game.education.ollama_commands import OllamaOps

# Check if Ollama is available
if OllamaOps.is_ollama_available():
    controller = GroundLevelController(verification_mode="shell")
    
    # Commands are executed automatically during verification
    result = controller.verify_act(1)
```

### Paste Mode (Manual Execution)

```python
controller = GroundLevelController(verification_mode="paste")

# User runs command in their terminal:
# $ ollama list

# User pastes output:
pasted_output = """
NAME             ID        SIZE      MODIFIED
llama3:latest    abc123    4.7 GB    2 days ago
"""

result = controller.verify_act(1, user_input=pasted_output)
```

## Module Reference

### OllamaOps (ollama_commands.py)

Safe wrappers for Ollama CLI commands:

```python
from game.education.ollama_commands import OllamaOps

# Check availability
available = OllamaOps.is_ollama_available()

# Execute commands
result = OllamaOps.pull_model("llama3", timeout=300)
result = OllamaOps.list_models()
result = OllamaOps.run_model("llama3", "What is AI?")
result = OllamaOps.show_model("llama3")
result = OllamaOps.remove_model("llama3")

# All methods return CommandResult with:
# - success: bool
# - stdout: str
# - stderr: str
# - exit_code: int
# - error_message: Optional[str]
```

### VerificationHelper (verification.py)

Utilities for validating outputs:

```python
from game.education.verification import VerificationHelper

# Check model presence
list_output = "llama3:latest    abc123    4.7 GB"
exists = VerificationHelper.model_exists_in_list("llama3", list_output)

# Extract information
size = VerificationHelper.extract_model_size(list_output, "llama3")
param = VerificationHelper.extract_parameter(show_output, "num_ctx")

# Validate output format
valid = VerificationHelper.is_valid_list_output(list_output)
valid = VerificationHelper.is_valid_show_output(show_output)

# Check response quality
has_response = VerificationHelper.response_received(model_output)
```

### GroundLevelController (ground_level.py)

Main orchestrator for the quest:

```python
from game.scenes.ground_level import GroundLevelController

controller = GroundLevelController(verification_mode="shell")

# Start an act
payload = controller.start_act(1)
# Returns ActPayload with:
# - act_number, title, narrative, teaching_text
# - command_hint, objective, status, verification_mode

# Verify completion
result = controller.verify_act(1, user_input=None)
# Returns VerificationResult with:
# - success, message, shell_output, next_step

# Get overall status
status = controller.get_act_status()
# Returns dict with:
# - current_act, verification_mode, model_name
# - acts (status for each), completed_count, total_acts
```

## Testing

Run the test suite to validate all modules:

```bash
python3 test_ground_level_modules.py
```

Run the demo to see all verification modes in action:

```bash
python3 demo_ground_level.py
```

## Integration Guide

To integrate into a game UI:

1. **Initialize Controller**
   ```python
   controller = GroundLevelController(
       verification_mode="shell",  # or "paste" or "simulated"
       quest_json_path="content/quests/ground_level.json"
   )
   ```

2. **Display Act Information**
   ```python
   payload = controller.start_act(act_number)
   
   # Display to user:
   # - payload.title (act title)
   # - payload.narrative (story text)
   # - payload.teaching_text (educational content)
   # - payload.command_hint (command to execute)
   ```

3. **Handle Verification**
   ```python
   # For shell mode:
   result = controller.verify_act(act_number)
   
   # For paste mode:
   user_paste = get_user_input()  # from UI
   result = controller.verify_act(act_number, user_input=user_paste)
   
   # For simulated mode:
   result = controller.verify_act(act_number)  # auto-completes
   ```

4. **Display Results**
   ```python
   # Show to user:
   # - result.message (feedback)
   # - result.shell_output (command output, if available)
   # - result.next_step (what to do next)
   
   if result.success:
       # Move to next act
       next_act = act_number + 1
   ```

5. **Track Progress**
   ```python
   status = controller.get_act_status()
   
   # Display:
   # - Current act: status['current_act']
   # - Progress: f"{status['completed_count']}/{status['total_acts']}"
   ```

## Command Cheat Sheet

```bash
# Download a model
ollama pull llama3

# List installed models
ollama list

# Run a model with a prompt
ollama run llama3 "What is artificial intelligence?"

# Show model details
ollama show llama3

# Remove a model
ollama rm llama3
```

## Educational Design

The tutorial follows pedagogical principles:

- **Progressive Difficulty**: Start simple, build complexity
- **Learn by Doing**: Real commands, not simulations
- **Immediate Feedback**: Verification after each command
- **Contextual Learning**: Commands taught within story
- **Multiple Modalities**: Support various learning environments

## Alternative Models

While the default is `llama3`, other models can be used:

```python
# Change model name
controller.model_name = "mistral"
controller.model_name = "qwen"
controller.model_name = "phi3"
```

Or specify in quest JSON:

```json
{
  "default_model": "mistral",
  ...
}
```

## Troubleshooting

### Ollama Not Found
If `OllamaOps.is_ollama_available()` returns `False`:
- Install Ollama from https://ollama.ai
- Ensure `ollama` is in system PATH
- Or switch to paste/simulated mode

### Command Timeouts
Increase timeout for slow connections:
```python
result = OllamaOps.pull_model("llama3", timeout=600)  # 10 minutes
```

### Verification Failures
Check:
- Model name spelling
- Command executed fully
- Output format matches expected pattern

## Further Reading

- **Full Design Document**: `docs/ground-level-ollama-rewrite.md`
- **Narrative Script**: `content/dialogue/ground_level_script.md`
- **Quest Data**: `content/quests/ground_level.json`
- **Ollama Documentation**: https://ollama.ai/docs

## License

This educational content is part of the AI-LLM-Dungeon project.
See LICENSE file in repository root for details.
