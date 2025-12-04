# Quick Start Guide: Ground Level Ollama Tutorial

## For Players

### Try the Tutorial Now

```bash
# Clone the repository
git clone https://github.com/AI-LLM-Dungeon/ai-llm-dungeon.git
cd ai-llm-dungeon

# Run the demo to see all modes
python3 demo_ground_level.py

# Run tests to verify everything works
python3 test_ground_level_modules.py
```

### Choose Your Mode

**Have Ollama Installed?**
- Use **Shell Mode** for automatic execution and verification
- Most authentic learning experience

**Don't Have Ollama?**
- Use **Paste Mode** to run commands yourself and paste results
- Or use **Simulated Mode** to learn syntax first

## For Developers

### Integrate Into Your Game

```python
from game.scenes.ground_level import GroundLevelController

# 1. Initialize controller
controller = GroundLevelController(
    verification_mode="shell",  # "shell", "paste", or "simulated"
    quest_json_path="content/quests/ground_level.json"
)

# 2. Start Act 1
act = controller.start_act(1)

# 3. Display to player
print(f"=== {act.title} ===")
print(act.narrative)
print(f"\nObjective: {act.objective}")
print(f"\nCommand to run:\n  {act.command_hint}")
print(f"\n{act.teaching_text}")

# 4. Verify completion
result = controller.verify_act(1)

# 5. Show result
if result.success:
    print(f"✅ {result.message}")
    print(f"Next: {result.next_step}")
else:
    print(f"❌ {result.message}")

# 6. Check overall progress
status = controller.get_act_status()
print(f"Progress: {status['completed_count']}/{status['total_acts']} complete")
```

### Use Individual Modules

**Execute Ollama Commands:**
```python
from game.education.ollama_commands import OllamaOps

# Check if available
if OllamaOps.is_ollama_available():
    # Pull a model
    result = OllamaOps.pull_model("llama3")
    print(result.stdout)
    
    # List models
    result = OllamaOps.list_models()
    print(result.stdout)
```

**Validate Output:**
```python
from game.education.verification import VerificationHelper

# Check if model exists
output = "llama3:latest    abc123    4.7 GB"
exists = VerificationHelper.model_exists_in_list("llama3", output)

# Extract information
size = VerificationHelper.extract_model_size(output, "llama3")
print(f"Model size: {size}")
```

## Example: Complete Act Flow

```python
from game.scenes.ground_level import GroundLevelController

def play_act(controller, act_number):
    """Play through a single act."""
    # Start the act
    act = controller.start_act(act_number)
    
    print(f"\n{'='*60}")
    print(f"ACT {act_number}: {act.title}")
    print('='*60)
    print(f"\n{act.narrative}\n")
    print(f"Objective: {act.objective}\n")
    print(f"Command:\n  {act.command_hint}\n")
    
    # For paste mode, get user input
    if controller.verification_mode.value == "paste":
        user_input = input("Paste output here: ")
        result = controller.verify_act(act_number, user_input)
    else:
        result = controller.verify_act(act_number)
    
    # Show result
    print(f"\n{'✅' if result.success else '❌'} {result.message}")
    if result.next_step:
        print(f"→ {result.next_step}")
    
    return result.success

# Play through all acts
controller = GroundLevelController(verification_mode="simulated")

for i in range(1, 6):
    if not play_act(controller, i):
        print("Failed! Try again.")
        break
    input("\nPress Enter to continue...")

print("\n🎉 Quest Complete! You've mastered Ollama commands!")
```

## Testing Your Integration

```python
# Run validation tests
python3 test_ground_level_modules.py

# Run demo to see examples
python3 demo_ground_level.py
```

## Customization

### Use a Different Model

```python
controller = GroundLevelController(verification_mode="shell")
controller.model_name = "mistral"  # or "qwen", "phi3", etc.
```

### Adjust Timeouts

```python
from game.education.ollama_commands import OllamaOps

# Longer timeout for slow connections
result = OllamaOps.pull_model("llama3", timeout=600)  # 10 minutes
```

### Load Custom Quest Data

```python
controller = GroundLevelController(
    verification_mode="paste",
    quest_json_path="/path/to/your/custom_quest.json"
)
```

## Troubleshooting

**"Ollama command not found"**
- Install Ollama from https://ollama.ai
- Or switch to paste/simulated mode

**"Command timed out"**
- Increase timeout value
- Check internet connection (for pull command)

**"Model not found in output"**
- Check spelling of model name
- Ensure command completed successfully
- Verify output format matches expected pattern

## Documentation

- **Full Design**: `docs/ground-level-ollama-rewrite.md`
- **Integration Guide**: `game/README.md`
- **Quest Definition**: `content/quests/ground_level.json`
- **Narrative Script**: `content/dialogue/ground_level_script.md`
- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`

## Commands Reference

```bash
# Download a model
ollama pull llama3

# List installed models
ollama list

# Run a model with a prompt
ollama run llama3 "What is AI?"

# Show model details
ollama show llama3

# Remove a model
ollama rm llama3
```

## Support

- **Issues**: https://github.com/AI-LLM-Dungeon/ai-llm-dungeon/issues
- **Ollama Docs**: https://ollama.ai/docs

## License

Part of the AI-LLM-Dungeon project. See LICENSE file.
