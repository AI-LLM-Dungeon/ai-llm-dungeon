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
        self.model_metadata = {
            "phi3-mini": {"id": "a2b3c4d5e6f7", "size": "2.3 GB", "size_bytes": 2300},
            "llama3-8b": {"id": "b3c4d5e6f7a8", "size": "4.7 GB", "size_bytes": 4700}
        }
    
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
        
        # Get model size for realistic simulation
        size_bytes = self.model_metadata.get(model_name, {}).get("size_bytes", 1500)
        
        # Simulate download progress
        self._show_progress_bar(model_name, duration=2.0, total_size=size_bytes)
        
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
        List all currently installed models with formatted table output.
        
        Returns:
            List of installed model names
        """
        if not self.installed_models:
            print("\nNo models installed yet.")
            return []
        
        print("\n📋 Simulating: ollama list")
        print("\nNAME            ID              SIZE      MODIFIED")
        
        import datetime
        for i, model_name in enumerate(sorted(self.installed_models)):
            metadata = self.model_metadata.get(model_name, {
                "id": "abc123def456",
                "size": "1.5 GB"
            })
            
            # Simulate different modification times
            minutes_ago = (i + 1) * 2
            modified = f"{minutes_ago} minutes ago" if minutes_ago < 60 else f"{minutes_ago // 60} hours ago"
            
            # Format the output to align properly
            name_col = model_name.ljust(16)
            id_col = metadata["id"].ljust(16)
            size_col = metadata["size"].ljust(10)
            
            print(f"{name_col}{id_col}{size_col}{modified}")
        
        print()
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
    
    def serve(self) -> None:
        """
        Simulate starting the Ollama daemon/service.
        
        Displays realistic output about the Ollama server starting.
        """
        print("\n🔄 Simulating: ollama serve")
        print("\nStarting Ollama server...")
        time.sleep(0.5)
        print("Ollama is running on http://localhost:11434")
        print("✅ Server is ready to accept requests\n")
    
    def _show_progress_bar(self, model_name: str, duration: float = 2.0, total_size: int = 1500) -> None:
        """
        Display a simulated progress bar for model download.
        
        Args:
            model_name: Name of the model being downloaded
            duration: Total duration of the progress bar in seconds
            total_size: Total size in MB
        """
        total_steps = 20
        sleep_time = duration / total_steps
        
        for i in range(total_steps + 1):
            percent = (i / total_steps) * 100
            filled = int(i)
            bar = "█" * filled + "░" * (total_steps - filled)
            
            # Simulate download size based on total_size
            size_mb = int((i / total_steps) * total_size)
            
            sys.stdout.write(f"\r[{bar}] {percent:5.1f}% ({size_mb} MB / {total_size} MB)")
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
