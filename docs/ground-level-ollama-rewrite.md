# Ground Level: Ollama Educational Rewrite

## Overview

This document describes the educational rewrite of the Ground Level tutorial in AI-LLM-Dungeon. The goal is to teach players real Ollama commands (`ollama pull`, `ollama list`, `ollama run`, `ollama show`, `ollama rm`) through an engaging dungeon narrative while they progress through five acts.

## Design Principles

### Pedagogical Approach

1. **Learn by Doing**: Players execute real commands, not simulations
2. **Progressive Difficulty**: Start with simple commands, build to complex workflows
3. **Immediate Feedback**: Verification after each command with helpful error messages
4. **Contextual Learning**: Commands taught within story context
5. **Real-World Application**: All commands directly applicable to actual Ollama usage

### Narrative Integration

The Ground Level maintains its dungeon atmosphere while teaching practical skills. Each act takes place in a distinct chamber with unique challenges that require specific Ollama commands to progress.

## Five Act Structure

### Act I: Summoner's Vestibule
**Objective**: Learn to download and verify model installation

**Skills Taught**:
- `ollama pull llama3` - Download a model
- `ollama list` - Verify installation

**Narrative Context**: 
The player enters a mystical vestibule where they must summon their first AI companion. An ancient scroll teaches the summoning incantation (the pull command).

**Verification**:
- Check that `ollama list` output contains the pulled model
- Confirm model appears in installed models list

### Act II: Hall of Mirrors
**Objective**: Learn to list and identify models

**Skills Taught**:
- `ollama list` - List all installed models
- Reading model tags and sizes

**Narrative Context**:
A hall of mirrors shows reflections of available companions. The player must identify the correct reflection by reading the model list and finding specific tags.

**Verification**:
- Parse `ollama list` output
- Identify model name and tag from output
- Answer a question about model size or modified date

### Act III: Oracle's Bench
**Objective**: Learn to run models with prompts

**Skills Taught**:
- `ollama run llama3 "prompt"` - Execute model with a query
- Understanding prompt formatting

**Narrative Context**:
The Oracle's Bench is where the companion demonstrates its wisdom. Players must pose a riddle or question to their AI companion and receive an answer.

**Verification**:
- Command executed successfully
- Output received from model
- (Optional) Check that answer contains expected keywords

### Act IV: Archivist's Sanctum
**Objective**: Learn to inspect model details

**Skills Taught**:
- `ollama show llama3` - Display model information
- Reading modelfile and parameters

**Narrative Context**:
The Archivist requires documentation of the companion's capabilities. Players must consult the model's tome (show command) to report specific parameters.

**Verification**:
- Regex match on `ollama show` output
- Extract parameter value (e.g., temperature, num_ctx)
- Report correct value to progress

### Act V: Purge Chamber
**Objective**: Learn to remove models

**Skills Taught**:
- `ollama rm llama3` - Remove a model
- Understanding memory management

**Narrative Context**:
To complete the journey, the player must release their companion back to the void, freeing system resources. This teaches responsible model management.

**Verification**:
- Check that model no longer appears in `ollama list`
- Confirm successful removal

## Verification Modes

The system supports three verification modes to accommodate different environments:

### Mode A: Direct Shell Execution (Preferred)
- System executes `ollama` commands via subprocess
- Captures stdout/stderr
- Timeout protection (30 seconds default)
- Most authentic learning experience
- **Requirement**: Ollama installed on system

### Mode B: Paste-Output Verification
- Player executes commands in their terminal
- Copies output and pastes into game interface
- Game validates output format and content
- Good for restricted environments
- **Advantage**: Works without system access

### Mode C: Simulated Fallback
- Shows real commands but doesn't execute
- Player acknowledges seeing command
- Progress marked without verification
- Least authentic but most accessible
- **Use case**: Learning syntax before installation

## Command Reference Cheat Sheet

### Basic Commands

```bash
# Pull (download) a model
ollama pull llama3

# List installed models
ollama list

# Run a model with a prompt
ollama run llama3 "What is the capital of France?"

# Show model details
ollama show llama3

# Remove a model
ollama rm llama3
```

### Command Parameters

#### ollama pull
```bash
ollama pull <model>[:<tag>]

# Examples:
ollama pull llama3          # Latest version
ollama pull llama3:8b       # Specific tag
ollama pull mistral:7b-instruct
```

#### ollama list
```bash
ollama list

# Output format:
# NAME                ID              SIZE      MODIFIED
# llama3:latest       abc123...       4.7 GB    2 days ago
```

#### ollama run
```bash
ollama run <model> [prompt]

# Examples:
ollama run llama3 "Hello!"              # One-shot
ollama run llama3                       # Interactive mode
```

#### ollama show
```bash
ollama show <model>

# Shows:
# - Modelfile
# - Parameters
# - Template
# - System message
```

#### ollama rm
```bash
ollama rm <model>

# Examples:
ollama rm llama3
ollama rm llama3:8b
```

## Implementation Architecture

### Module Structure

```
game/
├── education/
│   ├── __init__.py
│   ├── ollama_commands.py    # Safe subprocess wrappers
│   └── verification.py        # Verification helpers
└── scenes/
    ├── __init__.py
    └── ground_level.py        # Scene controller

content/
├── quests/
│   └── ground_level.json      # Quest definitions
└── dialogue/
    └── ground_level_script.md # Narrative text
```

### OllamaOps Class (ollama_commands.py)

Provides safe wrappers for Ollama CLI:

```python
class OllamaOps:
    @staticmethod
    def pull_model(model_name: str, timeout: int = 300) -> CommandResult
    
    @staticmethod
    def list_models(timeout: int = 30) -> CommandResult
    
    @staticmethod
    def run_model(model_name: str, prompt: str, timeout: int = 60) -> CommandResult
    
    @staticmethod
    def show_model(model_name: str, timeout: int = 30) -> CommandResult
    
    @staticmethod
    def remove_model(model_name: str, timeout: int = 30) -> CommandResult
```

**CommandResult Structure**:
```python
@dataclass
class CommandResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    error_message: Optional[str] = None
```

### Verification Helpers (verification.py)

```python
class VerificationHelper:
    @staticmethod
    def model_exists_in_list(model_name: str, list_output: str) -> bool
    
    @staticmethod
    def model_absent_from_list(model_name: str, list_output: str) -> bool
    
    @staticmethod
    def extract_parameter(show_output: str, param_name: str) -> Optional[str]
    
    @staticmethod
    def validate_paste_output(output: str, expected_pattern: str) -> bool
```

### Ground Level Controller (ground_level.py)

Orchestrates the five acts:

```python
class GroundLevelController:
    def __init__(self, verification_mode: str = "shell")
    
    def start_act(self, act_number: int) -> ActPayload
    
    def verify_act(self, act_number: int, user_input: Optional[str] = None) -> VerificationResult
    
    def get_act_status(self) -> dict
```

**ActPayload Structure**:
```python
@dataclass
class ActPayload:
    act_number: int
    title: str
    narrative: str
    teaching_text: str
    command_hint: str
    verification_mode: str
    status: str  # "not_started", "in_progress", "completed", "failed"
```

**VerificationResult Structure**:
```python
@dataclass
class VerificationResult:
    success: bool
    message: str
    shell_output: Optional[str] = None
    next_step: Optional[str] = None
```

## Quest Content Format (JSON)

```json
{
  "quest_id": "ground_level_ollama",
  "title": "Ground Level: Ollama Mastery",
  "description": "Learn real Ollama commands through dungeon exploration",
  "acts": [
    {
      "act_number": 1,
      "title": "Summoner's Vestibule",
      "objective": "Learn to pull and verify models",
      "commands": ["ollama pull llama3", "ollama list"],
      "verification": {
        "type": "model_present",
        "model_name": "llama3"
      }
    }
    // ... more acts
  ]
}
```

## Error Handling

### Common Errors and Solutions

1. **Ollama Not Installed**
   - Error: `command not found: ollama`
   - Solution: Suggest installation instructions or switch to Mode B/C

2. **Model Already Exists**
   - Error: Already pulled model
   - Solution: Skip or acknowledge and continue

3. **Insufficient Disk Space**
   - Error: Not enough space to pull model
   - Solution: Educate about model sizes, suggest cleanup

4. **Timeout**
   - Error: Command exceeded timeout
   - Solution: Inform about long download times, suggest retry

5. **Model Not Found**
   - Error: Model name not recognized
   - Solution: Show available models, correct typos

## UI Integration Guidelines

### Display Requirements

1. **Teaching Text Area**: Clear instructions for each act
2. **Command Display**: Show exact command to execute
3. **Output Area**: Display shell output or paste area
4. **Status Indicator**: Show current act progress
5. **Help Section**: Quick reference for commands

### Interactive Elements

1. **Execute Button** (Mode A): Run command directly
2. **Paste Input** (Mode B): Text area for pasted output
3. **Acknowledge Button** (Mode C): Confirm viewing command
4. **Hint Toggle**: Show/hide detailed help
5. **Skip Option**: Move forward without verification (optional)

## Testing Strategy

### Unit Tests

1. **Command Wrappers**: Test subprocess execution
   - Mock subprocess calls
   - Test timeout behavior
   - Validate error handling

2. **Verification Helpers**: Test parsing logic
   - Test regex patterns
   - Test model presence/absence checks
   - Test parameter extraction

3. **Controller**: Test act orchestration
   - Test state transitions
   - Test payload generation
   - Test verification flow

### Integration Tests

1. **End-to-End**: Full act completion
2. **Mode Switching**: Test all three modes
3. **Error Scenarios**: Test failure paths

### Manual Testing

1. **With Ollama Installed**: Full Mode A workflow
2. **Without Ollama**: Mode B and C workflows
3. **Various Models**: Test with llama3, mistral, qwen

## Future Enhancements

1. **Model Selection**: Allow player to choose preferred model
2. **Advanced Commands**: Teach `ollama cp`, `ollama create`
3. **Batch Operations**: Multiple model management
4. **Performance Testing**: Teach benchmarking commands
5. **Custom Modelfiles**: Teach modelfile creation
6. **API Integration**: Introduce Ollama REST API

## Configuration Options

```json
{
  "default_model": "llama3",
  "verification_mode": "shell",
  "timeout_seconds": 60,
  "allow_mode_switch": true,
  "skip_verification": false
}
```

## Accessibility Considerations

1. **Color-Blind Friendly**: Use symbols not just colors
2. **Screen Reader Compatible**: Descriptive text for all elements
3. **Keyboard Navigation**: Full keyboard support
4. **Clear Instructions**: Plain language, no jargon
5. **Multiple Learning Styles**: Visual, textual, and kinesthetic

## Success Metrics

Players should be able to:
- ✓ Pull a model independently
- ✓ List and identify installed models
- ✓ Run a model with a prompt
- ✓ Inspect model details
- ✓ Remove a model to free resources
- ✓ Understand when to use each command
- ✓ Apply commands in real-world scenarios

## Conclusion

This educational rewrite transforms the Ground Level from a simulated experience into a practical tutorial using real Ollama commands. Players learn authentic skills while enjoying an engaging narrative, preparing them for actual LLM development work.
