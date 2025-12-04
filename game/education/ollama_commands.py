"""
Safe subprocess wrappers for running Ollama CLI commands.

This module provides a safe interface for executing Ollama commands
with proper timeout handling, error capture, and result parsing.
"""

import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional


@dataclass
class CommandResult:
    """Result of executing an Ollama command.
    
    Attributes:
        success: Whether the command executed successfully (exit code 0)
        stdout: Standard output from the command
        stderr: Standard error from the command
        exit_code: The process exit code
        error_message: Human-readable error message if command failed
    """
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    error_message: Optional[str] = None


class OllamaOps:
    """Safe wrapper for Ollama CLI operations.
    
    Provides methods to execute Ollama commands with proper error handling,
    timeouts, and result parsing. All methods are static and do not require
    instantiation.
    """
    
    @staticmethod
    def is_ollama_available() -> bool:
        """Check if the ollama command is available on the system.
        
        Returns:
            bool: True if ollama is installed and in PATH, False otherwise
        """
        return shutil.which("ollama") is not None
    
    @staticmethod
    def pull_model(model_name: str, timeout: int = 300) -> CommandResult:
        """Pull (download) a model from the Ollama repository.
        
        Args:
            model_name: Name of the model to pull (e.g., 'llama3', 'llama3:8b')
            timeout: Maximum time to wait for download in seconds (default: 300)
        
        Returns:
            CommandResult: Result of the pull operation
            
        Example:
            >>> result = OllamaOps.pull_model('llama3')
            >>> if result.success:
            ...     print(f"Model pulled successfully")
        """
        if not OllamaOps.is_ollama_available():
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message="Ollama command not found. Please install Ollama first."
            )
        
        try:
            process = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = process.returncode == 0
            error_msg = None if success else f"Pull failed with exit code {process.returncode}"
            
            return CommandResult(
                success=success,
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                error_message=error_msg
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    @staticmethod
    def list_models(timeout: int = 30) -> CommandResult:
        """List all installed Ollama models.
        
        Args:
            timeout: Maximum time to wait for command in seconds (default: 30)
        
        Returns:
            CommandResult: Result containing the list of models
            
        Example:
            >>> result = OllamaOps.list_models()
            >>> if result.success:
            ...     print(result.stdout)
        """
        if not OllamaOps.is_ollama_available():
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message="Ollama command not found. Please install Ollama first."
            )
        
        try:
            process = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = process.returncode == 0
            error_msg = None if success else f"List failed with exit code {process.returncode}"
            
            return CommandResult(
                success=success,
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                error_message=error_msg
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    @staticmethod
    def run_model(model_name: str, prompt: str, timeout: int = 60) -> CommandResult:
        """Run a model with a given prompt.
        
        Note: This executes the model in non-interactive mode with a single prompt.
        For interactive sessions, users should run the command directly in their terminal.
        
        Args:
            model_name: Name of the model to run
            prompt: The prompt to send to the model
            timeout: Maximum time to wait for response in seconds (default: 60)
        
        Returns:
            CommandResult: Result containing the model's response
            
        Example:
            >>> result = OllamaOps.run_model('llama3', 'What is AI?')
            >>> if result.success:
            ...     print(result.stdout)
        """
        if not OllamaOps.is_ollama_available():
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message="Ollama command not found. Please install Ollama first."
            )
        
        try:
            process = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = process.returncode == 0
            error_msg = None if success else f"Run failed with exit code {process.returncode}"
            
            return CommandResult(
                success=success,
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                error_message=error_msg
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message=f"Command timed out after {timeout} seconds. Try a simpler prompt or increase timeout."
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    @staticmethod
    def show_model(model_name: str, timeout: int = 30) -> CommandResult:
        """Show detailed information about a model.
        
        Displays the model's Modelfile, parameters, template, and other metadata.
        
        Args:
            model_name: Name of the model to show
            timeout: Maximum time to wait for command in seconds (default: 30)
        
        Returns:
            CommandResult: Result containing model details
            
        Example:
            >>> result = OllamaOps.show_model('llama3')
            >>> if result.success:
            ...     print(result.stdout)
        """
        if not OllamaOps.is_ollama_available():
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message="Ollama command not found. Please install Ollama first."
            )
        
        try:
            process = subprocess.run(
                ["ollama", "show", model_name],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = process.returncode == 0
            error_msg = None if success else f"Show failed with exit code {process.returncode}"
            
            return CommandResult(
                success=success,
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                error_message=error_msg
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    @staticmethod
    def remove_model(model_name: str, timeout: int = 30) -> CommandResult:
        """Remove a model from the system.
        
        Args:
            model_name: Name of the model to remove
            timeout: Maximum time to wait for command in seconds (default: 30)
        
        Returns:
            CommandResult: Result of the removal operation
            
        Example:
            >>> result = OllamaOps.remove_model('llama3')
            >>> if result.success:
            ...     print("Model removed successfully")
        """
        if not OllamaOps.is_ollama_available():
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message="Ollama command not found. Please install Ollama first."
            )
        
        try:
            process = subprocess.run(
                ["ollama", "rm", model_name],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = process.returncode == 0
            error_msg = None if success else f"Remove failed with exit code {process.returncode}"
            
            return CommandResult(
                success=success,
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                error_message=error_msg
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stdout="",
                stderr="",
                exit_code=-1,
                error_message=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}"
            )
