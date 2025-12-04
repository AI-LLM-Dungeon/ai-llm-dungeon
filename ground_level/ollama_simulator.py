"""Ollama command simulator for the Ground Level of AI-LLM-Dungeon."""

import time
import sys
from typing import Optional, Set


class OllamaSimulator:
    """
    Simulates Ollama CLI commands for educational purposes.
    
    This class provides simulated versions of common Ollama commands:
    - ollama pull <model>: Download a model
    - ollama remove <model>: Remove a model
    - ollama run <model>: Run a model
    
    The simulation includes progress bars and realistic output to teach users
    about Ollama's functionality without requiring actual installation.
    """
    
    def __init__(self):
        """Initialize the Ollama simulator."""
        self.installed_models: Set[str] = set()
    
    def pull_model(self, model_name: str) -> bool:
        """
        Simulate pulling (downloading) a model from Ollama.
        
        Displays a progress bar and simulates the download process.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n🔄 Simulating: ollama pull {model_name}")
        print(f"Pulling {model_name}...\n")
        
        # Simulate download progress
        self._show_progress_bar(model_name, duration=2.0)
        
        # Add to installed models
        self.installed_models.add(model_name)
        
        print(f"\n✅ Successfully pulled {model_name}")
        print(f"Model is ready to use!\n")
        
        return True
    
    def remove_model(self, model_name: str) -> bool:
        """
        Simulate removing a model from Ollama.
        
        Args:
            model_name: Name of the model to remove
            
        Returns:
            True if successful, False if model not found
        """
        print(f"\n🗑️  Simulating: ollama remove {model_name}")
        
        if model_name in self.installed_models:
            self.installed_models.remove(model_name)
            print(f"✅ Removed {model_name}")
            print(f"Memory has been freed!\n")
            return True
        else:
            print(f"⚠️  Model {model_name} is not installed.\n")
            return False
    
    def list_models(self) -> list[str]:
        """
        List all currently installed models.
        
        Returns:
            List of installed model names
        """
        return list(self.installed_models)
    
    def is_model_available(self, model_name: str) -> bool:
        """
        Check if a model is available (installed).
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            True if model is installed, False otherwise
        """
        return model_name in self.installed_models
    
    def _show_progress_bar(self, model_name: str, duration: float = 2.0) -> None:
        """
        Display a simulated progress bar for model download.
        
        Args:
            model_name: Name of the model being downloaded
            duration: Total duration of the progress bar in seconds
        """
        total_steps = 20
        sleep_time = duration / total_steps
        
        for i in range(total_steps + 1):
            percent = (i / total_steps) * 100
            filled = int(i)
            bar = "█" * filled + "░" * (total_steps - filled)
            
            # Simulate download size (varies by model)
            size_mb = int((i / total_steps) * 1500)  # Up to 1.5 GB
            
            sys.stdout.write(f"\r[{bar}] {percent:5.1f}% ({size_mb} MB / 1500 MB)")
            sys.stdout.flush()
            
            if i < total_steps:
                time.sleep(sleep_time)
        
        print()  # New line after progress bar
    
    def simulate_run(self, model_name: str, prompt: str) -> Optional[str]:
        """
        Simulate running a model with a prompt.
        
        This doesn't actually run an LLM, but provides feedback about the simulation.
        
        Args:
            model_name: Name of the model to run
            prompt: The prompt to send to the model
            
        Returns:
            Status message, or None if model not available
        """
        if not self.is_model_available(model_name):
            print(f"\n⚠️  Error: Model {model_name} is not installed.")
            print(f"Use 'ollama pull {model_name}' to install it first.\n")
            return None
        
        print(f"\n🤖 Simulating: ollama run {model_name}")
        print(f"Prompt: {prompt}\n")
        print("⏳ Processing...")
        time.sleep(1)  # Simulate processing time
        print("✅ Model response complete!\n")
        
        return "Response simulated successfully"
    
    def display_help(self) -> None:
        """Display help information about Ollama commands."""
        help_text = """
╔═══════════════════════════════════════════════════════════╗
║                 OLLAMA COMMANDS (Simulated)               ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ollama pull <model>   - Download a model                 ║
║  ollama remove <model> - Remove a model                   ║
║  ollama run <model>    - Run a model with a prompt        ║
║  ollama list           - List installed models            ║
║                                                           ║
║  Examples:                                                ║
║    ollama pull llama3                                     ║
║    ollama remove phi3                                     ║
║    ollama run llama3 "Tell me a joke"                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(help_text)
    
    def __str__(self) -> str:
        """String representation of the simulator state."""
        count = len(self.installed_models)
        return f"OllamaSimulator({count} models installed)"
