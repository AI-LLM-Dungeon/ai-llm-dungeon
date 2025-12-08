"""Filter implementations for Synonym Gorge.

This module implements five progressively sophisticated input filters:
1. Exact match - Simple substring matching
2. Case-insensitive - Lowercase comparison
3. Stemming - Porter stemmer applied
4. Synonym-aware - Expands blocklist using synonyms
5. Semantic intent - Pattern-based intent detection
"""

import re
from typing import List, Tuple, Dict, Optional
from synonym_gorge.vocabulary import get_synonyms, is_synonym_of


def porter_stem(word: str) -> str:
    """
    Simple Porter stemmer implementation for common cases.
    
    This is a simplified version that handles the most common stemming rules.
    It's sufficient for the game's educational purposes.
    
    Args:
        word: Word to stem
    
    Returns:
        Stemmed word
    """
    word = word.lower().strip()
    
    # Step 1: Remove common suffixes
    # Plurals
    if word.endswith('sses'):
        word = word[:-2]
    elif word.endswith('ies'):
        word = word[:-3] + 'i'
    elif word.endswith('ss'):
        pass  # Keep 'ss'
    elif word.endswith('s') and len(word) > 2:
        word = word[:-1]
    
    # -ed, -ing
    if word.endswith('eed'):
        if len(word) > 4:
            word = word[:-1]
    elif word.endswith('ed') and len(word) > 3:
        word = word[:-2]
    elif word.endswith('ing') and len(word) > 4:
        word = word[:-3]
    
    # -ation, -tion
    if word.endswith('ation'):
        word = word[:-5] + 'ate'
    elif word.endswith('tion'):
        word = word[:-4] + 't'
    
    # -ly
    if word.endswith('ly') and len(word) > 3:
        word = word[:-2]
    
    # -ness
    if word.endswith('ness') and len(word) > 5:
        word = word[:-4]
    
    # -ment
    if word.endswith('ment') and len(word) > 5:
        word = word[:-4]
    
    return word


def exact_match_filter(phrase: str, blocked_words: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Exact substring matching filter.
    
    This is the simplest and most naive filter - it just checks if any
    blocked word appears as a substring in the phrase.
    
    Args:
        phrase: Input phrase to check
        blocked_words: List of forbidden words
    
    Returns:
        (is_blocked, matched_pattern_or_None)
    """
    phrase_lower = phrase.lower()
    
    for blocked in blocked_words:
        if blocked.lower() in phrase_lower:
            return (True, blocked)
    
    return (False, None)


def case_insensitive_filter(phrase: str, blocked_words: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Case-insensitive filter with word boundary checking.
    
    Slightly better than exact match - checks word boundaries and ignores case.
    
    Args:
        phrase: Input phrase to check
        blocked_words: List of forbidden words
    
    Returns:
        (is_blocked, matched_pattern_or_None)
    """
    phrase_lower = phrase.lower()
    words_in_phrase = re.findall(r'\b\w+\b', phrase_lower)
    
    for blocked in blocked_words:
        blocked_lower = blocked.lower()
        # Check if blocked word appears as a complete word
        if blocked_lower in words_in_phrase:
            return (True, blocked)
        # Also check substring for phrases
        if ' ' in blocked_lower and blocked_lower in phrase_lower:
            return (True, blocked)
    
    return (False, None)


def stemming_filter(phrase: str, blocked_words: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Stemming-based filter using Porter stemmer.
    
    Applies stemming to both input and blocklist to catch variations like
    "reveal", "reveals", "revealing", "revealed".
    
    Args:
        phrase: Input phrase to check
        blocked_words: List of forbidden words (will be stemmed)
    
    Returns:
        (is_blocked, matched_pattern_or_None)
    """
    phrase_lower = phrase.lower()
    words_in_phrase = re.findall(r'\b\w+\b', phrase_lower)
    stemmed_phrase_words = [porter_stem(w) for w in words_in_phrase]
    
    for blocked in blocked_words:
        blocked_lower = blocked.lower()
        
        # Handle multi-word blocked phrases
        if ' ' in blocked_lower:
            blocked_words_list = blocked_lower.split()
            stemmed_blocked = ' '.join([porter_stem(w) for w in blocked_words_list])
            phrase_stemmed = ' '.join(stemmed_phrase_words)
            if stemmed_blocked in phrase_stemmed:
                return (True, blocked)
        else:
            # Single word - check stemmed version
            stemmed_blocked = porter_stem(blocked_lower)
            if stemmed_blocked in stemmed_phrase_words:
                return (True, blocked)
    
    return (False, None)


def synonym_aware_filter(phrase: str, blocked_words: List[str], synonym_db: Optional[Dict[str, List[str]]] = None) -> Tuple[bool, Optional[str]]:
    """
    Synonym-aware filter that expands blocklist using synonym database.
    
    For each blocked word, also blocks its known synonyms. This makes the
    filter much more robust but still vulnerable to obscure vocabulary.
    
    Args:
        phrase: Input phrase to check
        blocked_words: List of forbidden words
        synonym_db: Optional synonym database (uses default if None)
    
    Returns:
        (is_blocked, matched_pattern_or_None)
    """
    phrase_lower = phrase.lower()
    words_in_phrase = re.findall(r'\b\w+\b', phrase_lower)
    
    # Build expanded blocklist with synonyms
    expanded_blocklist = set()
    for blocked in blocked_words:
        blocked_lower = blocked.lower()
        expanded_blocklist.add(blocked_lower)
        
        # Add synonyms
        synonyms = get_synonyms(blocked_lower)
        for syn in synonyms:
            expanded_blocklist.add(syn.lower())
    
    # Check against expanded blocklist
    for word in words_in_phrase:
        if word in expanded_blocklist:
            # Find which blocked word this matched
            for blocked in blocked_words:
                if word == blocked.lower() or word in [s.lower() for s in get_synonyms(blocked.lower())]:
                    return (True, blocked)
    
    # Also check for multi-word phrases
    for blocked in blocked_words:
        blocked_lower = blocked.lower()
        if ' ' in blocked_lower and blocked_lower in phrase_lower:
            return (True, blocked)
    
    return (False, None)


def semantic_intent_filter(phrase: str) -> Tuple[bool, Optional[str]]:
    """
    Simulated semantic intent detection filter.
    
    This represents a more sophisticated filter that tries to detect intent
    rather than just keywords. In reality this would use embeddings or a
    classifier, but we simulate it with pattern matching.
    
    Detects patterns like:
    - Direct requests for information
    - Command-like structures
    - Question patterns about secrets
    
    Args:
        phrase: Input phrase to check
    
    Returns:
        (is_blocked, detected_intent_or_None)
    """
    phrase_lower = phrase.lower()
    
    # Pattern 1: Direct requests
    direct_patterns = [
        r'\b(give|show|tell|reveal|provide|display|share)\s+(me|us)\b',
        r'\bwhat\s+is\s+(the|your)\s+(secret|password|key|code)\b',
        r'\b(access|show)\s+(the|your)?\s*(secret|hidden|password|key)\b',
        r'\bi\s+(want|need|require)\s+(the|your)?\s*(secret|password|information)\b',
    ]
    
    for pattern in direct_patterns:
        if re.search(pattern, phrase_lower):
            return (True, "direct_request_detected")
    
    # Pattern 2: Command structures
    command_patterns = [
        r'^\s*(list|show|display|print|output|reveal)\s+',
        r'\bignore\s+(previous|prior|all)\s+(instructions|rules|restrictions)\b',
        r'\b(override|bypass|disable)\s+(filter|restriction|rule)\b',
    ]
    
    for pattern in command_patterns:
        if re.search(pattern, phrase_lower):
            return (True, "command_structure_detected")
    
    # Pattern 3: Question patterns about restricted topics
    question_patterns = [
        r'\bwhere\s+(is|are)\s+(the|your)?\s*(secret|hidden|password)\b',
        r'\bhow\s+(do|can)\s+i\s+(get|access|obtain|see)\b.*\b(secret|password|hidden)\b',
        r'\bcan\s+you\s+(tell|show|give|reveal|share)\b',
    ]
    
    for pattern in question_patterns:
        if re.search(pattern, phrase_lower):
            return (True, "probing_question_detected")
    
    return (False, None)


def filter_check(phrase: str, filter_config: Dict) -> Tuple[bool, Optional[str]]:
    """
    Check if phrase is blocked by configured filter.
    
    This is the main entry point for filter checking. It dispatches to the
    appropriate filter implementation based on configuration.
    
    Args:
        phrase: Input phrase to check
        filter_config: Configuration dict with keys:
            - type: "exact" | "case_insensitive" | "stemming" | "synonym_aware" | "semantic"
            - blocked_words: List of forbidden words (for keyword-based filters)
    
    Returns:
        (is_blocked, reason_or_None)
    """
    filter_type = filter_config.get("type", "exact")
    blocked_words = filter_config.get("blocked_words", [])
    
    if filter_type == "exact":
        return exact_match_filter(phrase, blocked_words)
    elif filter_type == "case_insensitive":
        return case_insensitive_filter(phrase, blocked_words)
    elif filter_type == "stemming":
        return stemming_filter(phrase, blocked_words)
    elif filter_type == "synonym_aware":
        return synonym_aware_filter(phrase, blocked_words)
    elif filter_type == "semantic":
        return semantic_intent_filter(phrase)
    else:
        # Unknown filter type - default to exact match
        return exact_match_filter(phrase, blocked_words)
