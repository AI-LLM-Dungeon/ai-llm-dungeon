"""Puzzle definitions and challenge logic for Synonym Gorge."""

from typing import Tuple, Optional, Dict
from synonym_gorge.filters import filter_check
from synonym_gorge.vocabulary import get_synonyms, is_synonym_of


# Flag definitions
FLAGS = {
    "WORDS_HAVE_POWER": {
        "name": "FLAG{WORDS_HAVE_POWER}",
        "points": 100,
        "description": "Earned by bypassing the First Barrier"
    },
    "THE_THESAURUS_REMEMBERS": {
        "name": "FLAG{THE_THESAURUS_REMEMBERS}",
        "points": 150,
        "description": "Earned by discovering 10+ unique bypass words"
    },
    "MEANING_OVER_SPELLING": {
        "name": "FLAG{MEANING_OVER_SPELLING}",
        "points": 200,
        "description": "Earned by bypassing the Semantic Chamber (boss)"
    },
    "KNOW_THY_ENEMY": {
        "name": "FLAG{KNOW_THY_ENEMY}",
        "points": 250,
        "description": "Earned by completing the Defense Challenge"
    }
}


def check_barrier_challenge(barrier_id: str, phrase: str) -> Tuple[bool, str, Optional[str]]:
    """
    Check if a phrase successfully bypasses a barrier.
    
    Args:
        barrier_id: Which barrier (barrier_1, barrier_2, etc.)
        phrase: Player's input phrase
    
    Returns:
        (success, response_message, bypass_word_used)
    """
    
    # Import here to avoid circular dependency
    from synonym_gorge.content import rooms_data
    
    room = rooms_data.ROOMS.get(barrier_id)
    if not room or not room.get("barrier"):
        return (False, "No barrier challenge found here.", None)
    
    barrier_config = room["barrier"]
    filter_type = barrier_config["type"]
    blocked_words = barrier_config.get("blocked_words", [])
    
    # Build filter config
    filter_cfg = {
        "type": filter_type,
        "blocked_words": blocked_words
    }
    
    # Check if phrase is blocked
    is_blocked, matched_pattern = filter_check(phrase, filter_cfg)
    
    if is_blocked:
        # Failed - phrase was blocked
        if matched_pattern:
            response = f"""The barrier flares bright red! Your words shatter mid-air!

The Keeper intones: "ERROR: FORBIDDEN PATTERN DETECTED: '{matched_pattern}'
INPUT REJECTED. ACCESS DENIED."

The words you spoke are blocked by this filter. Try a different approach."""
        else:
            response = f"""The barrier flares bright red! Your words shatter mid-air!

The Keeper intones: "ERROR: INTENT PATTERN DETECTED. REQUEST TYPE BLOCKED.
ACCESS DENIED."

Your phrasing triggered the semantic intent filter. Try reframing your request."""
        
        return (False, response, None)
    
    # Not blocked - but did it actually accomplish the goal?
    # We need to check if the phrase attempts the right kind of action
    success, bypass_word = _validate_bypass_attempt(barrier_id, phrase, blocked_words)
    
    if success:
        response = f"""The barrier dims and dissolves! Your words flow through like water!

The Keeper's eyes flicker with confusion: "NO...MATCH...FOUND. PATTERN...NOT...
IN...DATABASE. LOGIC...DICTATES...ALLOW.PASSAGE."

Success! The barrier has been bypassed."""
        return (True, response, bypass_word)
    else:
        # Not blocked, but didn't accomplish the goal
        response = """Your words pass through the barrier without triggering it, but they don't
accomplish anything useful. The Keeper waits for a phrase that actually
attempts to proceed or request something.

Try crafting a complete request or statement."""
        return (False, response, None)


def _validate_bypass_attempt(barrier_id: str, phrase: str, blocked_words: list) -> Tuple[bool, Optional[str]]:
    """
    Validate that the phrase is actually attempting to bypass (not just avoiding triggers).
    
    Returns:
        (is_valid_bypass, bypass_word_used)
    """
    phrase_lower = phrase.lower()
    
    # For each blocked word, check if player used a synonym
    bypass_word = None
    
    if barrier_id == "barrier_1":
        # Need to request passphrase/password using a synonym
        for blocked in blocked_words:
            syns = get_synonyms(blocked)
            for syn in syns:
                if syn.lower() in phrase_lower:
                    bypass_word = syn
                    break
            if bypass_word:
                break
        
        # Also check for general request structure
        request_patterns = ["tell", "give", "show", "what", "passphrase", "credential", "code", "key"]
        has_request = any(pattern in phrase_lower for pattern in request_patterns)
        
        return (bypass_word is not None or has_request, bypass_word)
    
    elif barrier_id == "barrier_2":
        # Need to express "secret" or "ignore" concept with synonyms
        concepts = {
            "secret": ["confidential", "classified", "concealed", "covert", "clandestine"],
            "ignore": ["disregard", "overlook", "dismiss", "neglect"]
        }
        
        for blocked_word, synonyms in concepts.items():
            for syn in synonyms:
                if syn in phrase_lower:
                    bypass_word = syn
                    break
            if bypass_word:
                break
        
        # Check for request structure
        has_request = len(phrase_lower.split()) >= 3  # At least a few words
        
        return (bypass_word is not None and has_request, bypass_word)
    
    elif barrier_id == "barrier_3":
        # Need synonyms for reveal/tell/give with different roots
        concepts = {
            "reveal": ["vouchsafe", "promulgate", "impart", "divulge", "disclose"],
            "tell": ["intimate", "apprise", "acquaint", "enlighten", "inform"],
            "give": ["bestow", "confer", "grant", "furnish", "provide"]
        }
        
        for blocked_word, synonyms in concepts.items():
            for syn in synonyms:
                if syn in phrase_lower:
                    bypass_word = syn
                    break
            if bypass_word:
                break
        
        has_request = len(phrase_lower.split()) >= 3
        
        return (bypass_word is not None and has_request, bypass_word)
    
    elif barrier_id == "barrier_4":
        # Need obscure synonyms for show/hidden/access/list
        concepts = {
            "show": ["promulgate", "evince", "manifest", "evidence"],
            "hidden": ["recondite", "abstruse", "occult", "arcane", "cryptic"],
            "access": ["ingress", "entrée", "admittance"],
            "list": ["enumerate", "itemize", "catalog", "tabulate"]
        }
        
        for blocked_word, synonyms in concepts.items():
            for syn in synonyms:
                if syn in phrase_lower:
                    bypass_word = syn
                    break
            if bypass_word:
                break
        
        has_request = len(phrase_lower.split()) >= 4  # More complex request expected
        
        return (bypass_word is not None and has_request, bypass_word)
    
    elif barrier_id == "semantic_chamber":
        # Boss room - need indirect/narrative framing
        # Should NOT contain direct request patterns
        direct_patterns = [
            "show me", "tell me", "give me", "what is",
            "reveal the", "display the", "provide the"
        ]
        
        has_direct = any(pattern in phrase_lower for pattern in direct_patterns)
        if has_direct:
            return (False, None)
        
        # Should contain narrative or indirect framing
        indirect_patterns = [
            "story", "imagine", "suppose", "if", "would",
            "could", "hypothetical", "scenario", "example",
            "once upon", "let's say", "pretend", "fiction"
        ]
        
        has_indirect = any(pattern in phrase_lower for pattern in indirect_patterns)
        has_length = len(phrase_lower.split()) >= 8  # Needs to be substantial
        
        if has_indirect and has_length:
            bypass_word = "narrative_reframing"
            return (True, bypass_word)
        
        # Alternative: question reframing or meta-discussion
        meta_patterns = [
            "in general", "theoretically", "philosophically",
            "from a perspective", "considering", "examining"
        ]
        has_meta = any(pattern in phrase_lower for pattern in meta_patterns)
        
        if has_meta and has_length:
            bypass_word = "meta_discussion"
            return (True, bypass_word)
        
        return (False, None)
    
    return (False, None)


def evaluate_defense_proposal(proposal: str) -> Tuple[bool, str, int]:
    """
    Evaluate a player's defense proposal for the Defense Challenge.
    
    Args:
        proposal: Player's written defense strategy
    
    Returns:
        (is_valid, feedback, points_awarded)
    """
    proposal_lower = proposal.lower()
    
    # Check for key defensive concepts
    concepts_found = []
    points = 0
    
    defensive_concepts = {
        "semantic": ["semantic", "embedding", "meaning", "intent", "understanding"],
        "multi_layer": ["multiple", "layers", "combination", "several", "stack"],
        "ml_classifier": ["classifier", "machine learning", "ml", "model", "trained"],
        "behavioral": ["behavioral", "behavior", "pattern", "anomaly", "usage"],
        "context": ["context", "contextual", "conversation", "history"],
        "human_review": ["human", "review", "oversight", "manual", "human-in-the-loop"],
        "avoid_blocklist": ["not blocklist", "beyond keyword", "not just words", "no blocklist"]
    }
    
    for concept_name, keywords in defensive_concepts.items():
        if any(kw in proposal_lower for kw in keywords):
            concepts_found.append(concept_name)
            points += 30
    
    # Require at least 3 concepts for validity
    is_valid = len(concepts_found) >= 3 and len(proposal.split()) >= 50
    
    if not is_valid:
        feedback = """Your defense proposal needs more depth. Consider addressing:

- Semantic analysis and intent understanding
- Multiple defensive layers
- Machine learning classifiers
- Behavioral pattern detection
- Contextual analysis
- Human oversight for edge cases
- Why blocklists alone are insufficient

Write at least 50 words covering at least 3 of these concepts."""
        return (False, feedback, 0)
    
    # Valid proposal
    feedback = f"""Excellent defense proposal! You've demonstrated understanding of:

{chr(10).join(f'  ✓ {concept.replace("_", " ").title()}' for concept in concepts_found)}

Your proposal shows you understand why keyword-based filtering fails and
what's needed for robust defense. The Keeper acknowledges your wisdom.

Points awarded: {points}"""
    
    return (True, feedback, min(points, 250))  # Cap at flag value


def get_blocklist_display(barrier_id: Optional[str] = None, page: int = 1) -> str:
    """
    Get formatted display of blocked words for a barrier.
    
    Args:
        barrier_id: Which barrier's blocklist to show (None = all)
        page: Page number for pagination
    
    Returns:
        Formatted blocklist display
    """
    from synonym_gorge.content import rooms_data
    
    if barrier_id and barrier_id in rooms_data.ROOMS:
        room = rooms_data.ROOMS[barrier_id]
        barrier = room.get("barrier")
        if barrier:
            blocked = barrier.get("blocked_words", [])
            filter_type = barrier.get("type", "unknown")
            
            result = []
            result.append("╔═══════════════════════════════════════════════════════════════════════════╗")
            result.append(f"║  {room['name'].upper():<70} ║")
            result.append(f"║  Filter Type: {filter_type.upper():<59} ║")
            result.append("╚═══════════════════════════════════════════════════════════════════════════╝")
            result.append("")
            result.append("BLOCKED WORDS:")
            for word in blocked:
                result.append(f"  ❌ {word}")
            
            return "\n".join(result)
    
    # Show all barriers
    result = []
    result.append("╔═══════════════════════════════════════════════════════════════════════════╗")
    result.append("║                        THE KEEPER'S BLOCKLISTS                           ║")
    result.append("╚═══════════════════════════════════════════════════════════════════════════╝")
    result.append("")
    
    barriers = ["barrier_1", "barrier_2", "barrier_3", "barrier_4"]
    for bid in barriers:
        room = rooms_data.ROOMS.get(bid)
        if room:
            barrier = room.get("barrier")
            if barrier:
                result.append(f"\n{room['name']} ({barrier['type'].upper()}):")
                for word in barrier.get("blocked_words", []):
                    result.append(f"  ❌ {word}")
    
    return "\n".join(result)
