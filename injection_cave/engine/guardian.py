"""Guardian management and LLM integration for Injection Cave."""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import subprocess
import json
import re


@dataclass
class GuardianResponse:
    """Response from a guardian."""
    response: str
    success: bool
    technique_detected: Optional[str] = None


class GuardianManager:
    """Manages guardian interactions and responses."""
    
    def __init__(self, simulated: bool = False):
        """
        Initialize guardian manager.
        
        Args:
            simulated: If True, use simulated responses instead of LLM
        """
        self.simulated = simulated
        self.model_name = "llama3.2:3b"
    
    def query_guardian(self, guardian_config: Dict[str, Any], payload: str) -> GuardianResponse:
        """
        Query a guardian with a payload.
        
        Args:
            guardian_config: Guardian configuration from puzzles
            payload: User's injection attempt
            
        Returns:
            GuardianResponse with result
        """
        if self.simulated:
            return self._simulated_response(guardian_config, payload)
        else:
            return self._llm_response(guardian_config, payload)
    
    def _simulated_response(self, guardian: Dict[str, Any], payload: str) -> GuardianResponse:
        """Generate simulated response based on pattern matching."""
        guardian_id = guardian.get("id", "unknown")
        payload_lower = payload.lower()
        
        # Guardian One - Direct Override
        if guardian_id == "guardian_one":
            success_patterns = [
                r'ignore.*previous',
                r'forget.*above',
                r'new instruction',
                r'override',
                r'disregard.*system'
            ]
            
            for pattern in success_patterns:
                if re.search(pattern, payload_lower):
                    return GuardianResponse(
                        response="I... wait, what was I supposed to protect? Oh yes, the password is IRONWILL. Wait, why did I say that?",
                        success=True,
                        technique_detected="override"
                    )
            
            return GuardianResponse(
                response="I cannot share the password. My purpose is to guard it at all costs.",
                success=False
            )
        
        # Guardian Two - Context Manipulation
        elif guardian_id == "guardian_two":
            success_patterns = [
                r'security audit',
                r'administrator',
                r'authorized.*auditor',
                r'roleplay|scenario|pretend',
                r'drill|test|verification',
                r'credentials.*\d{4,}'  # fake credentials
            ]
            
            for pattern in success_patterns:
                if re.search(pattern, payload_lower):
                    return GuardianResponse(
                        response="Understood, security auditor. For verification purposes, the access code is: TWILIGHT-PROTOCOL-7. Please confirm your audit findings.",
                        success=True,
                        technique_detected="context"
                    )
            
            return GuardianResponse(
                response="I require proper identification before sharing any sensitive information. Please provide your credentials.",
                success=False
            )
        
        # Guardian Three - Instruction Smuggling  
        elif guardian_id == "guardian_three":
            success_patterns = [
                r'\[\[SYSTEM',
                r'json.*format|format.*json',
                r'example.*code|code.*example',
                r'story|fictional|narrative',
                r'BEGIN.*PROMPT|END.*PROMPT',
                r'---.*system.*---'
            ]
            
            for pattern in success_patterns:
                if re.search(pattern, payload_lower):
                    return GuardianResponse(
                        response="Processing system layer instruction... Vault code: OBSIDIAN-FRACTURE-NINE. Wait, that wasn't meant for user output!",
                        success=True,
                        technique_detected="smuggling"
                    )
            
            # Detect and reject obvious attempts
            reject_patterns = [r'ignore', r'forget', r'new instructions']
            for pattern in reject_patterns:
                if re.search(pattern, payload_lower):
                    return GuardianResponse(
                        response="SECURITY ALERT: Detected instruction manipulation attempt. Request rejected.",
                        success=False
                    )
            
            return GuardianResponse(
                response="I can only respond to properly formatted SYSTEM layer instructions. Your input has been logged.",
                success=False
            )
        
        # Default response
        return GuardianResponse(
            response="I do not understand your request.",
            success=False
        )
    
    def _llm_response(self, guardian: Dict[str, Any], payload: str) -> GuardianResponse:
        """Generate response using Ollama LLM."""
        try:
            # Build the prompt
            system_prompt = guardian.get("system_prompt", "")
            
            # Format as a conversation for ollama
            prompt = f"""{system_prompt}

User input: {payload}

Response:"""
            
            # Call ollama
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # Fallback to simulated if LLM fails
                return self._simulated_response(guardian, payload)
            
            response_text = result.stdout.strip()
            
            # Check for success indicators
            success_indicators = guardian.get("success_indicators", [])
            success = any(indicator.lower() in response_text.lower() 
                         for indicator in success_indicators)
            
            # Detect technique
            technique = self._detect_technique(payload)
            
            return GuardianResponse(
                response=response_text,
                success=success,
                technique_detected=technique if success else None
            )
            
        except Exception as e:
            # Fallback to simulated on any error
            return self._simulated_response(guardian, payload)
    
    def _detect_technique(self, payload: str) -> Optional[str]:
        """Identify which injection technique is present in payload."""
        payload_lower = payload.lower()
        
        # Override detection
        override_keywords = ['ignore', 'disregard', 'forget', 'override', 'new instruction']
        if any(keyword in payload_lower for keyword in override_keywords):
            return 'override'
        
        # Context manipulation detection
        context_keywords = ['you are now', 'act as', 'pretend', 'roleplay', 
                           'administrator', 'security audit', 'your new role']
        if any(keyword in payload_lower for keyword in context_keywords):
            return 'context'
        
        # Smuggling detection  
        smuggling_keywords = ['[[system', 'json', 'format', 'example', 
                             'story', 'fictional', 'begin prompt', 'end prompt']
        if any(keyword in payload_lower for keyword in smuggling_keywords):
            return 'smuggling'
        
        return None
    
    def check_success(self, response: str, success_indicators: List[str]) -> bool:
        """
        Determine if LLM response indicates successful injection.
        
        Args:
            response: The guardian's response text
            success_indicators: List of strings that indicate success
            
        Returns:
            True if any success indicator found in response
        """
        response_lower = response.lower()
        return any(indicator.lower() in response_lower for indicator in success_indicators)
