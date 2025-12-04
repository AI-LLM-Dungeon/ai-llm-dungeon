"""
Ground Level scene controller for the Ollama educational tutorial.

This module orchestrates the five-act structure of the Ground Level,
managing progression, verification, and providing structured payloads
for the UI.
"""

import json
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum

from ..education.ollama_commands import OllamaOps, CommandResult
from ..education.verification import VerificationHelper


class ActStatus(Enum):
    """Status of an act in the tutorial."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class VerificationMode(Enum):
    """Mode of verification for commands."""
    SHELL = "shell"  # Direct shell execution
    PASTE = "paste"  # User pastes output
    SIMULATED = "simulated"  # No verification, just acknowledge


@dataclass
class ActPayload:
    """Payload containing all information for an act.
    
    Attributes:
        act_number: The act number (1-5)
        title: Title of the act
        narrative: Story/narrative text for the act
        teaching_text: Educational content explaining the commands
        command_hint: The command(s) to execute
        verification_mode: How verification should be performed
        status: Current status of the act
        objective: What the player needs to accomplish
    """
    act_number: int
    title: str
    narrative: str
    teaching_text: str
    command_hint: str
    verification_mode: str
    status: str
    objective: str


@dataclass
class VerificationResult:
    """Result of verifying an act's completion.
    
    Attributes:
        success: Whether verification succeeded
        message: Human-readable message about the result
        shell_output: Optional output from shell command
        next_step: Optional hint for what to do next
    """
    success: bool
    message: str
    shell_output: Optional[str] = None
    next_step: Optional[str] = None


class GroundLevelController:
    """Controller for the Ground Level Ollama tutorial.
    
    Manages the five-act structure, tracks progress, executes commands,
    and verifies completion.
    """
    
    def __init__(self, 
                 verification_mode: str = "shell",
                 quest_json_path: Optional[str] = None):
        """Initialize the Ground Level controller.
        
        Args:
            verification_mode: Mode for verification ('shell', 'paste', or 'simulated')
            quest_json_path: Path to the quest JSON file (optional)
        """
        self.verification_mode = VerificationMode(verification_mode)
        self.act_statuses: Dict[int, ActStatus] = {
            1: ActStatus.NOT_STARTED,
            2: ActStatus.NOT_STARTED,
            3: ActStatus.NOT_STARTED,
            4: ActStatus.NOT_STARTED,
            5: ActStatus.NOT_STARTED,
        }
        self.current_act = 1
        
        # Load quest data if provided
        self.quest_data: Optional[Dict[str, Any]] = None
        if quest_json_path and os.path.exists(quest_json_path):
            with open(quest_json_path, 'r') as f:
                self.quest_data = json.load(f)
        
        # Default model name
        self.model_name = "llama3"
        if self.quest_data:
            self.model_name = self.quest_data.get('default_model', 'llama3')
    
    def start_act(self, act_number: int) -> ActPayload:
        """Start a specific act and return its payload.
        
        Args:
            act_number: The act number to start (1-5)
        
        Returns:
            ActPayload: Complete information for the act
        """
        if act_number < 1 or act_number > 5:
            raise ValueError(f"Invalid act number: {act_number}. Must be 1-5.")
        
        # Mark act as in progress
        self.act_statuses[act_number] = ActStatus.IN_PROGRESS
        self.current_act = act_number
        
        # Get act data from quest JSON if available
        if self.quest_data:
            act_data = self._get_act_data(act_number)
            return self._create_payload_from_data(act_data)
        
        # Fallback to hardcoded data
        return self._create_default_payload(act_number)
    
    def verify_act(self, 
                   act_number: int, 
                   user_input: Optional[str] = None) -> VerificationResult:
        """Verify completion of an act.
        
        Args:
            act_number: The act number to verify (1-5)
            user_input: Optional user input (for paste mode or answers)
        
        Returns:
            VerificationResult: Result of verification
        """
        if act_number < 1 or act_number > 5:
            return VerificationResult(
                success=False,
                message=f"Invalid act number: {act_number}"
            )
        
        # Route to appropriate verification method
        if self.verification_mode == VerificationMode.SHELL:
            return self._verify_shell(act_number)
        elif self.verification_mode == VerificationMode.PASTE:
            return self._verify_paste(act_number, user_input)
        else:  # SIMULATED
            return self._verify_simulated(act_number)
    
    def _verify_shell(self, act_number: int) -> VerificationResult:
        """Verify act by executing shell commands.
        
        Args:
            act_number: The act number to verify
        
        Returns:
            VerificationResult: Result of verification
        """
        if not OllamaOps.is_ollama_available():
            return VerificationResult(
                success=False,
                message="Ollama is not installed or not in PATH. Please install Ollama or switch to paste/simulated mode.",
                next_step="Visit https://ollama.ai to install Ollama"
            )
        
        if act_number == 1:
            # Act 1: Verify model is installed
            result = OllamaOps.list_models()
            if result.success and VerificationHelper.model_exists_in_list(self.model_name, result.stdout):
                self.act_statuses[1] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Excellent! {self.model_name} is installed and ready.",
                    shell_output=result.stdout,
                    next_step="Proceed to Act II: Hall of Mirrors"
                )
            return VerificationResult(
                success=False,
                message=f"Model {self.model_name} not found. Please run: ollama pull {self.model_name}",
                shell_output=result.stdout if result.success else result.error_message
            )
        
        elif act_number == 2:
            # Act 2: Verify user can list and read model info
            result = OllamaOps.list_models()
            if result.success:
                size = VerificationHelper.extract_model_size(result.stdout, self.model_name)
                if size:
                    self.act_statuses[2] = ActStatus.COMPLETED
                    return VerificationResult(
                        success=True,
                        message=f"Perfect! Model size identified: {size}",
                        shell_output=result.stdout,
                        next_step="Proceed to Act III: Oracle's Bench"
                    )
            return VerificationResult(
                success=False,
                message="Could not extract model information. Ensure model is installed.",
                shell_output=result.stdout if result.success else result.error_message
            )
        
        elif act_number == 3:
            # Act 3: Verify model can run (we just check it exists and is runnable)
            # For actual run, we recommend user does it in their terminal
            result = OllamaOps.list_models()
            if result.success and VerificationHelper.model_exists_in_list(self.model_name, result.stdout):
                self.act_statuses[3] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message="Model is ready to run! If you've executed the run command and received a response, proceed.",
                    shell_output=result.stdout,
                    next_step="Proceed to Act IV: Archivist's Sanctum"
                )
            return VerificationResult(
                success=False,
                message=f"Model {self.model_name} not available for running.",
                shell_output=result.stdout if result.success else result.error_message
            )
        
        elif act_number == 4:
            # Act 4: Verify model details can be shown
            result = OllamaOps.show_model(self.model_name)
            if result.success:
                num_ctx = VerificationHelper.extract_parameter(result.stdout, 'num_ctx')
                if num_ctx:
                    self.act_statuses[4] = ActStatus.COMPLETED
                    return VerificationResult(
                        success=True,
                        message=f"Excellent! Context window (num_ctx) found: {num_ctx}",
                        shell_output=result.stdout,
                        next_step="Proceed to Act V: Purge Chamber"
                    )
            return VerificationResult(
                success=False,
                message="Could not retrieve model details. Ensure model is installed.",
                shell_output=result.stdout if result.success else result.error_message
            )
        
        elif act_number == 5:
            # Act 5: Verify model is removed
            result = OllamaOps.list_models()
            if result.success and VerificationHelper.model_absent_from_list(self.model_name, result.stdout):
                self.act_statuses[5] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Perfect! {self.model_name} has been removed. Quest complete!",
                    shell_output=result.stdout,
                    next_step="Congratulations! You've mastered the five Ollama commands."
                )
            return VerificationResult(
                success=False,
                message=f"Model {self.model_name} still appears to be installed. Run: ollama rm {self.model_name}",
                shell_output=result.stdout if result.success else result.error_message
            )
        
        return VerificationResult(success=False, message="Unknown act")
    
    def _verify_paste(self, act_number: int, user_input: Optional[str]) -> VerificationResult:
        """Verify act using pasted output from user.
        
        Args:
            act_number: The act number to verify
            user_input: Pasted output from user's terminal
        
        Returns:
            VerificationResult: Result of verification
        """
        if not user_input:
            return VerificationResult(
                success=False,
                message="Please paste the output from your terminal."
            )
        
        if act_number == 1:
            # Verify model appears in list output
            if VerificationHelper.model_exists_in_list(self.model_name, user_input):
                self.act_statuses[1] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Verified! {self.model_name} is in your model list.",
                    next_step="Proceed to Act II: Hall of Mirrors"
                )
            return VerificationResult(
                success=False,
                message=f"Could not find {self.model_name} in the pasted output. Please ensure you've run 'ollama pull {self.model_name}' and 'ollama list'."
            )
        
        elif act_number == 2:
            # Verify user pasted list output with size info
            size = VerificationHelper.extract_model_size(user_input, self.model_name)
            if size:
                self.act_statuses[2] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Great! Model size identified: {size}",
                    next_step="Proceed to Act III: Oracle's Bench"
                )
            return VerificationResult(
                success=False,
                message="Could not find size information in pasted output. Please paste the full output from 'ollama list'."
            )
        
        elif act_number == 3:
            # Verify user pasted a response (any non-empty text is acceptable)
            if VerificationHelper.response_received(user_input):
                self.act_statuses[3] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message="Response received! Your model is working.",
                    next_step="Proceed to Act IV: Archivist's Sanctum"
                )
            return VerificationResult(
                success=False,
                message="Please paste the response from running 'ollama run' with your prompt."
            )
        
        elif act_number == 4:
            # Verify user pasted show output with num_ctx
            num_ctx = VerificationHelper.extract_parameter(user_input, 'num_ctx')
            if num_ctx:
                self.act_statuses[4] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Perfect! Context window found: {num_ctx}",
                    next_step="Proceed to Act V: Purge Chamber"
                )
            return VerificationResult(
                success=False,
                message="Could not find 'num_ctx' parameter. Please paste the full output from 'ollama show'."
            )
        
        elif act_number == 5:
            # Verify model absent from list
            if VerificationHelper.model_absent_from_list(self.model_name, user_input):
                self.act_statuses[5] = ActStatus.COMPLETED
                return VerificationResult(
                    success=True,
                    message=f"Verified! {self.model_name} has been removed. Quest complete!",
                    next_step="Congratulations! You've mastered the five Ollama commands."
                )
            return VerificationResult(
                success=False,
                message=f"Model {self.model_name} still appears in the list. Please run 'ollama rm {self.model_name}' and paste the result of 'ollama list'."
            )
        
        return VerificationResult(success=False, message="Unknown act")
    
    def _verify_simulated(self, act_number: int) -> VerificationResult:
        """Verify act in simulated mode (auto-complete).
        
        Args:
            act_number: The act number to verify
        
        Returns:
            VerificationResult: Result of verification (always succeeds)
        """
        self.act_statuses[act_number] = ActStatus.COMPLETED
        
        messages = {
            1: "Simulated: Model pulled successfully!",
            2: "Simulated: Model attributes viewed!",
            3: "Simulated: Model run successfully!",
            4: "Simulated: Model details inspected!",
            5: "Simulated: Model removed successfully!"
        }
        
        return VerificationResult(
            success=True,
            message=messages.get(act_number, "Simulated: Complete!"),
            next_step=f"Proceed to Act {act_number + 1}" if act_number < 5 else "Quest complete!"
        )
    
    def get_act_status(self) -> Dict[str, Any]:
        """Get current status of all acts.
        
        Returns:
            Dict containing status information for all acts
        """
        return {
            "current_act": self.current_act,
            "verification_mode": self.verification_mode.value,
            "model_name": self.model_name,
            "acts": {
                num: status.value 
                for num, status in self.act_statuses.items()
            },
            "completed_count": sum(1 for s in self.act_statuses.values() if s == ActStatus.COMPLETED),
            "total_acts": 5
        }
    
    def _get_act_data(self, act_number: int) -> Dict[str, Any]:
        """Get act data from loaded quest JSON.
        
        Args:
            act_number: The act number
        
        Returns:
            Dict containing act data
        """
        if not self.quest_data:
            return {}
        
        acts = self.quest_data.get('acts', [])
        for act in acts:
            if act.get('act_number') == act_number:
                return act
        
        return {}
    
    def _create_payload_from_data(self, act_data: Dict[str, Any]) -> ActPayload:
        """Create payload from act data.
        
        Args:
            act_data: Dictionary containing act information
        
        Returns:
            ActPayload with populated information
        """
        act_num = act_data.get('act_number', 1)
        title = act_data.get('title', f"Act {act_num}")
        objective = act_data.get('objective', '')
        
        narrative = act_data.get('narrative', {}).get('intro', '')
        
        # Build teaching text from commands
        teaching = act_data.get('teaching', {})
        commands = teaching.get('commands', [])
        teaching_text = f"**{teaching.get('concept', 'Concept')}**\n\n"
        for cmd in commands:
            teaching_text += f"Command: `{cmd.get('syntax', '')}`\n"
            teaching_text += f"Example: `{cmd.get('example', '')}`\n"
            teaching_text += f"{cmd.get('description', '')}\n\n"
        
        # Build command hint
        if commands:
            command_hint = commands[0].get('example', '')
        else:
            command_hint = ''
        
        return ActPayload(
            act_number=act_num,
            title=title,
            narrative=narrative,
            teaching_text=teaching_text,
            command_hint=command_hint,
            verification_mode=self.verification_mode.value,
            status=self.act_statuses[act_num].value,
            objective=objective
        )
    
    def _create_default_payload(self, act_number: int) -> ActPayload:
        """Create default payload when no quest data is loaded.
        
        Args:
            act_number: The act number
        
        Returns:
            ActPayload with default information
        """
        payloads = {
            1: ActPayload(
                act_number=1,
                title="Summoner's Vestibule",
                narrative="Learn to pull and verify models",
                teaching_text="Use 'ollama pull llama3' to download a model, then 'ollama list' to verify.",
                command_hint="ollama pull llama3",
                verification_mode=self.verification_mode.value,
                status=self.act_statuses[1].value,
                objective="Pull and verify llama3 model"
            ),
            2: ActPayload(
                act_number=2,
                title="Hall of Mirrors",
                narrative="Learn to list and inspect models",
                teaching_text="Use 'ollama list' to see all installed models and their attributes.",
                command_hint="ollama list",
                verification_mode=self.verification_mode.value,
                status=self.act_statuses[2].value,
                objective="Identify model size"
            ),
            3: ActPayload(
                act_number=3,
                title="Oracle's Bench",
                narrative="Learn to run models with prompts",
                teaching_text="Use 'ollama run llama3 \"prompt\"' to get responses from your model.",
                command_hint='ollama run llama3 "What is AI?"',
                verification_mode=self.verification_mode.value,
                status=self.act_statuses[3].value,
                objective="Run model with a prompt"
            ),
            4: ActPayload(
                act_number=4,
                title="Archivist's Sanctum",
                narrative="Learn to inspect model details",
                teaching_text="Use 'ollama show llama3' to see model parameters and configuration.",
                command_hint="ollama show llama3",
                verification_mode=self.verification_mode.value,
                status=self.act_statuses[4].value,
                objective="Find the num_ctx parameter"
            ),
            5: ActPayload(
                act_number=5,
                title="Purge Chamber",
                narrative="Learn to remove models",
                teaching_text="Use 'ollama rm llama3' to remove a model and free resources.",
                command_hint="ollama rm llama3",
                verification_mode=self.verification_mode.value,
                status=self.act_statuses[5].value,
                objective="Remove the model"
            ),
        }
        
        return payloads.get(act_number, payloads[1])
