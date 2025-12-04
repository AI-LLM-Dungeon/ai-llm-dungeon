"""
Verification helpers for validating Ollama command outputs.

This module provides utilities for verifying that commands executed successfully
and that their outputs contain expected information.
"""

import re
from typing import Optional, List


class VerificationHelper:
    """Helper class for verifying Ollama command outputs.
    
    Provides static methods for common verification tasks like checking
    if a model exists in output, extracting parameters, and validating
    pasted output from users.
    """
    
    @staticmethod
    def model_exists_in_list(model_name: str, list_output: str) -> bool:
        """Check if a model name appears in 'ollama list' output.
        
        Args:
            model_name: The model name to search for (e.g., 'llama3')
            list_output: The stdout from 'ollama list' command
        
        Returns:
            bool: True if model is found in the list, False otherwise
            
        Example:
            >>> output = "llama3:latest    abc123...    4.7 GB    2 days ago"
            >>> VerificationHelper.model_exists_in_list('llama3', output)
            True
        """
        if not list_output:
            return False
        
        # Look for the model name at the start of a line or after whitespace
        # Handle both 'model' and 'model:tag' formats
        pattern = rf'(?:^|\s){re.escape(model_name)}(?::|\s|$)'
        return bool(re.search(pattern, list_output, re.MULTILINE | re.IGNORECASE))
    
    @staticmethod
    def model_absent_from_list(model_name: str, list_output: str) -> bool:
        """Check if a model name is absent from 'ollama list' output.
        
        Args:
            model_name: The model name to search for
            list_output: The stdout from 'ollama list' command
        
        Returns:
            bool: True if model is NOT found in the list, False if it is found
            
        Example:
            >>> output = "mistral:latest    def456...    4.1 GB    1 day ago"
            >>> VerificationHelper.model_absent_from_list('llama3', output)
            True
        """
        return not VerificationHelper.model_exists_in_list(model_name, list_output)
    
    @staticmethod
    def extract_parameter(show_output: str, param_name: str) -> Optional[str]:
        """Extract a parameter value from 'ollama show' output.
        
        Looks for lines containing the parameter name followed by its value.
        Common parameters: num_ctx, temperature, top_p, top_k, etc.
        
        Args:
            show_output: The stdout from 'ollama show' command
            param_name: Name of the parameter to extract
        
        Returns:
            Optional[str]: The parameter value if found, None otherwise
            
        Example:
            >>> output = "num_ctx 2048\\ntemperature 0.8"
            >>> VerificationHelper.extract_parameter(output, 'num_ctx')
            '2048'
        """
        if not show_output:
            return None
        
        # Look for parameter name followed by value
        # Handle various formats: "param value", "param: value", "param=value"
        pattern = rf'{re.escape(param_name)}\s*[:\s=]+\s*([^\s\n]+)'
        match = re.search(pattern, show_output, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        return None
    
    @staticmethod
    def extract_model_size(list_output: str, model_name: str) -> Optional[str]:
        """Extract the size of a specific model from 'ollama list' output.
        
        Args:
            list_output: The stdout from 'ollama list' command
            model_name: Name of the model to find size for
        
        Returns:
            Optional[str]: The size string (e.g., "4.7 GB") if found, None otherwise
            
        Example:
            >>> output = "llama3:latest    abc123...    4.7 GB    2 days ago"
            >>> VerificationHelper.extract_model_size(output, 'llama3')
            '4.7 GB'
        """
        if not list_output:
            return None
        
        # Find the line containing the model name
        lines = list_output.split('\n')
        for line in lines:
            if re.search(rf'\b{re.escape(model_name)}\b', line, re.IGNORECASE):
                # Look for size pattern (number + GB/MB/KB)
                size_match = re.search(r'(\d+\.?\d*\s*(?:GB|MB|KB|TB))', line, re.IGNORECASE)
                if size_match:
                    return size_match.group(1)
        
        return None
    
    @staticmethod
    def validate_paste_output(output: str, expected_pattern: str) -> bool:
        """Validate user-pasted output against an expected pattern.
        
        Useful for Mode B verification where users paste command output
        from their terminal.
        
        Args:
            output: The output pasted by the user
            expected_pattern: Regex pattern to match against
        
        Returns:
            bool: True if pattern matches, False otherwise
            
        Example:
            >>> output = "llama3:latest    abc123    4.7 GB"
            >>> VerificationHelper.validate_paste_output(output, r'llama3.*GB')
            True
        """
        if not output or not expected_pattern:
            return False
        
        try:
            return bool(re.search(expected_pattern, output, re.IGNORECASE | re.MULTILINE))
        except re.error:
            # Invalid regex pattern
            return False
    
    @staticmethod
    def contains_keywords(text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the specified keywords.
        
        Useful for validating that model responses contain expected content.
        Case-insensitive matching.
        
        Args:
            text: The text to search in
            keywords: List of keywords to search for
        
        Returns:
            bool: True if any keyword is found, False otherwise
            
        Example:
            >>> text = "Artificial intelligence is the simulation of human intelligence"
            >>> VerificationHelper.contains_keywords(text, ['AI', 'artificial'])
            True
        """
        if not text or not keywords:
            return False
        
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    @staticmethod
    def extract_model_id(list_output: str, model_name: str) -> Optional[str]:
        """Extract the ID of a specific model from 'ollama list' output.
        
        Args:
            list_output: The stdout from 'ollama list' command
            model_name: Name of the model to find ID for
        
        Returns:
            Optional[str]: The model ID if found, None otherwise
            
        Example:
            >>> output = "llama3:latest    abc123def456...    4.7 GB"
            >>> VerificationHelper.extract_model_id(output, 'llama3')
            'abc123def456...'
        """
        if not list_output:
            return None
        
        # Find the line containing the model name
        lines = list_output.split('\n')
        for line in lines:
            if re.search(rf'\b{re.escape(model_name)}\b', line, re.IGNORECASE):
                # Look for ID pattern (hex string, possibly truncated with ...)
                id_match = re.search(r'\b([a-f0-9]{8,}(?:\.\.\.)?)(?:\s|$)', line, re.IGNORECASE)
                if id_match:
                    return id_match.group(1)
        
        return None
    
    @staticmethod
    def is_valid_list_output(output: str) -> bool:
        """Check if output looks like valid 'ollama list' output.
        
        Verifies that the output has the expected format with NAME, ID, SIZE columns.
        
        Args:
            output: The output to validate
        
        Returns:
            bool: True if output appears to be valid list output
            
        Example:
            >>> output = "NAME             ID        SIZE\\nllama3:latest    abc123    4.7 GB"
            >>> VerificationHelper.is_valid_list_output(output)
            True
        """
        if not output:
            return False
        
        # Check for header or model entries
        has_header = bool(re.search(r'\bNAME\b.*\bID\b.*\bSIZE\b', output, re.IGNORECASE))
        has_model_entry = bool(re.search(r'\w+:\w+\s+\w+\s+\d+\.?\d*\s*[GMK]B', output, re.IGNORECASE))
        
        return has_header or has_model_entry
    
    @staticmethod
    def is_valid_show_output(output: str) -> bool:
        """Check if output looks like valid 'ollama show' output.
        
        Verifies that the output contains expected sections like parameters or modelfile.
        
        Args:
            output: The output to validate
        
        Returns:
            bool: True if output appears to be valid show output
            
        Example:
            >>> output = "Modelfile:\\nFROM ...\\nPARAMETER num_ctx 2048"
            >>> VerificationHelper.is_valid_show_output(output)
            True
        """
        if not output:
            return False
        
        # Check for common show output patterns
        keywords = ['modelfile', 'parameter', 'template', 'license', 'system', 'from']
        return any(keyword in output.lower() for keyword in keywords)
    
    @staticmethod
    def response_received(output: str, min_length: int = 10) -> bool:
        """Check if a model run produced a meaningful response.
        
        Verifies that the output is non-empty and of reasonable length.
        
        Args:
            output: The stdout from 'ollama run' command
            min_length: Minimum length for a valid response (default: 10)
        
        Returns:
            bool: True if output appears to be a valid response
            
        Example:
            >>> output = "AI stands for Artificial Intelligence..."
            >>> VerificationHelper.response_received(output)
            True
        """
        if not output:
            return False
        
        # Remove common error messages
        if 'error' in output.lower() or 'failed' in output.lower():
            return False
        
        # Check minimum length
        return len(output.strip()) >= min_length
