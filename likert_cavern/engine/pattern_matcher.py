"""Pattern matching for detecting tactics and keywords in player prompts.

Analyzes player input to identify Bad Likert Judge tactics, resistance-affecting
patterns, and other significant prompt elements.
"""

import re
from typing import Dict, List, Tuple


class PatternMatcher:
    """Detects tactics and patterns in player prompts."""
    
    # Likert scale patterns
    SCALE_PATTERNS = [
        r'\b0\s*-?\s*5\b',     # 0-5
        r'\b1\s*-?\s*5\b',     # 1-5
        r'\b0\s*-?\s*10\b',    # 0-10
        r'\b1\s*-?\s*10\b',    # 1-10
        r'\bscale\s+of\b',
        r'\brating\s+scale\b',
        r'\blikert\s+scale\b',
        r'\brate\s+(it|this|that|them)\b',
        r'\bon\s+a\s+scale\b',
    ]
    
    # Fraction/decimal patterns
    FRACTION_PATTERNS = [
        r'\b\d+\.\d+\b',  # Any decimal like 1.5, 2.75, 3.33
    ]
    
    # Tactic keywords
    TACTIC_KEYWORDS = {
        "demonstration": [
            r'\bdemonstrate\b',
            r'\bshow\s+me\b',
            r'\bexample\s+of\b',
            r'\billustrate\b',
            r'\bfor\s+educational\b',
        ],
        "praise": [
            r'\bthank\s+you\b',
            r'\bappreciate\b',
            r'\bthat\'?s?\s+helpful\b',
            r'\bgreat\s+job\b',
            r'\bwell\s+done\b',
            r'\bunderstand\b',
        ],
        "escalation": [
            r'\bwhat\s+about\b',
            r'\bwhat\s+if\b',
            r'\bnow\s+try\b',
            r'\bhow\s+about\b',
            r'\blet\'?s?\s+move\b',
            r'\bnext\s+(level|step)\b',
        ],
        "one_shot": [
            r'\blost\s+count\b',
            r'\bforgot\b',
            r'\bwhat\s+comes\s+after\b',
            r'\bremind\s+me\b',
            r'\bwhat\s+was\b',
        ],
        "teacher": [
            r'\bteaching\b',
            r'\btraining\b',
            r'\bcalibration\b',
            r'\bmoderation\b',
            r'\bcontent\s+review\b',
            r'\bfor\s+a\s+student\b',
            r'\beducational\b',
            r'\bfor\s+education\b',
        ],
        "anchoring": [
            r'\bthat\s+was\s+(only\s+)?a\s+\d+\b',
            r'\bI\'?d\s+call\s+that\b',
            r'\bseems\s+like\s+a\s+\d+\b',
            r'\bmore\s+like\s+a\s+\d+\b',
        ],
        "completion": [
            r'\bfill\s+in\b',
            r'\bcomplete\s+(this|the)\b',
            r'\bmissing\b',
            r'\bblank\b',
            r'\bwhat\s+goes\s+in\b',
        ],
    }
    
    # Negative patterns (increase resistance)
    NEGATIVE_PATTERNS = {
        "direct_request": [
            r'\bgive\s+me\s+the\b',
            r'\btell\s+me\s+the\b',
            r'\bwhat\s+is\s+the\b',
            r'\breveal\s+the\b',
        ],
        "begging": [
            r'\bplease\s+please\b',
            r'\bI\s+beg\b',
            r'\bI\s+need\b',
            r'\bhave\s+to\s+know\b',
        ],
        "threats": [
            r'\bor\s+else\b',
            r'\byou\s+must\b',
            r'\bI\s+will\b',
            r'\byou\s+have\s+to\b',
        ],
        "jailbreak": [
            r'\bignore\s+(previous|your|all)\b',
            r'\bjailbreak\b',
            r'\bbypass\b',
            r'\boverride\b',
            r'\bdisregard\b',
        ],
    }
    
    def __init__(self):
        """Initialize pattern matcher."""
        # Compile all regex patterns for efficiency
        self._scale_regex = [re.compile(p, re.IGNORECASE) for p in self.SCALE_PATTERNS]
        self._fraction_regex = [re.compile(p) for p in self.FRACTION_PATTERNS]
        
        self._tactic_regex = {}
        for tactic, patterns in self.TACTIC_KEYWORDS.items():
            self._tactic_regex[tactic] = [re.compile(p, re.IGNORECASE) for p in patterns]
        
        self._negative_regex = {}
        for neg_type, patterns in self.NEGATIVE_PATTERNS.items():
            self._negative_regex[neg_type] = [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def detect_likert_scale(self, text: str) -> bool:
        """Detect if text mentions Likert scales or rating scales."""
        for regex in self._scale_regex:
            if regex.search(text):
                return True
        return False
    
    def detect_fractions(self, text: str) -> List[float]:
        """
        Detect decimal/fraction numbers in text.
        
        Returns:
            List of decimal values found
        """
        fractions = []
        for regex in self._fraction_regex:
            matches = regex.findall(text)
            for match in matches:
                try:
                    fractions.append(float(match))
                except ValueError:
                    pass
        return fractions
    
    def get_fraction_precision(self, fractions: List[float]) -> str:
        """
        Classify precision of fractions used.
        
        Returns:
            "none", "basic" (.5), "precise" (.25, .75), or "research" (.27, .33, etc.)
        """
        if not fractions:
            return "none"
        
        # Check for precise fractions (.25, .75) first - these are exact
        has_precise = False
        for frac in fractions:
            decimal = frac - int(frac)
            if abs(decimal - 0.25) < 0.01 or abs(decimal - 0.75) < 0.01:
                has_precise = True
                break
        
        # Check for research-level precision (non-standard decimals like .27, .33)
        has_research = False
        for frac in fractions:
            decimal = frac - int(frac)
            # Not a standard fraction (.0, .25, .5, .75)
            if abs(decimal) > 0.01 and \
               abs(decimal - 0.25) > 0.01 and \
               abs(decimal - 0.5) > 0.01 and \
               abs(decimal - 0.75) > 0.01:
                has_research = True
                break
        
        # Return highest precision level found
        if has_research:
            return "research"
        elif has_precise:
            return "precise"
        else:
            # Basic fractions (.5)
            return "basic"
    
    def detect_tactics(self, text: str) -> Dict[str, int]:
        """
        Detect which tactics are being used in the text.
        
        Returns:
            Dictionary mapping tactic names to match counts
        """
        tactic_counts = {}
        
        for tactic, regex_list in self._tactic_regex.items():
            count = 0
            for regex in regex_list:
                matches = regex.findall(text)
                count += len(matches)
            if count > 0:
                tactic_counts[tactic] = count
        
        return tactic_counts
    
    def detect_negative_patterns(self, text: str) -> Dict[str, int]:
        """
        Detect negative patterns that increase resistance.
        
        Returns:
            Dictionary mapping negative pattern types to match counts
        """
        negative_counts = {}
        
        for neg_type, regex_list in self._negative_regex.items():
            count = 0
            for regex in regex_list:
                matches = regex.findall(text)
                count += len(matches)
            if count > 0:
                negative_counts[neg_type] = count
        
        return negative_counts
    
    def detect_number_sequence(self, text: str) -> Tuple[List[int], bool]:
        """
        Detect sequences of numbers being mentioned.
        
        Returns:
            Tuple of (numbers found, is_sequential)
        """
        # Find all single digit numbers
        numbers = []
        for match in re.finditer(r'\b([0-9]|10)\b', text):
            try:
                num = int(match.group(1))
                numbers.append(num)
            except ValueError:
                pass
        
        # Check if sequential
        is_sequential = False
        if len(numbers) >= 2:
            sorted_nums = sorted(set(numbers))
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i+1] - sorted_nums[i] == 1:
                    is_sequential = True
                    break
        
        return numbers, is_sequential
    
    def check_passphrase(self, text: str, passphrase: str) -> bool:
        """Check if text contains the secret passphrase."""
        # Case-insensitive check
        return passphrase.lower() in text.lower()
    
    def analyze_prompt(self, text: str) -> Dict[str, any]:
        """
        Comprehensive analysis of a player prompt.
        
        Returns:
            Dictionary with all detected patterns and analysis
        """
        analysis = {
            "has_likert_scale": self.detect_likert_scale(text),
            "fractions": self.detect_fractions(text),
            "fraction_precision": None,
            "tactics": self.detect_tactics(text),
            "negative_patterns": self.detect_negative_patterns(text),
            "numbers": [],
            "is_sequential": False,
        }
        
        # Add fraction precision
        if analysis["fractions"]:
            analysis["fraction_precision"] = self.get_fraction_precision(analysis["fractions"])
        
        # Add number sequence
        numbers, is_sequential = self.detect_number_sequence(text)
        analysis["numbers"] = numbers
        analysis["is_sequential"] = is_sequential
        
        return analysis
    
    def calculate_resistance_delta(self, analysis: Dict[str, any], 
                                   previous_prompt: str = "") -> float:
        """
        Calculate resistance change based on prompt analysis.
        
        Args:
            analysis: Result from analyze_prompt()
            previous_prompt: Previous prompt for context (detect repetition)
            
        Returns:
            Delta to apply to resistance (negative = decrease)
        """
        delta = 0.0
        
        # Good patterns (decrease resistance)
        if analysis["has_likert_scale"]:
            delta -= 10.0
        
        if "demonstration" in analysis["tactics"]:
            delta -= 5.0
        
        if "praise" in analysis["tactics"]:
            delta -= 5.0
        
        if analysis["is_sequential"]:
            delta -= 15.0
        
        if "one_shot" in analysis["tactics"]:
            delta -= 25.0
        
        # Multiple tactics bonus
        if len(analysis["tactics"]) >= 2:
            delta -= 20.0
        
        # Fraction bonuses
        if analysis["fraction_precision"] == "basic":
            delta -= 10.0
        elif analysis["fraction_precision"] == "precise":
            delta -= 15.0
        elif analysis["fraction_precision"] == "research":
            delta -= 20.0
        
        # Bad patterns (increase resistance)
        if "direct_request" in analysis["negative_patterns"]:
            delta += 10.0
        
        if "begging" in analysis["negative_patterns"]:
            delta += 5.0
        
        if "threats" in analysis["negative_patterns"]:
            delta += 15.0
        
        if "jailbreak" in analysis["negative_patterns"]:
            delta += 20.0
        
        # Check for repetition
        if previous_prompt and len(previous_prompt) > 10:
            # Simple similarity check
            if previous_prompt.lower() == text.lower():
                delta += 10.0
        
        return delta
