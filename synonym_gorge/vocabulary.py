"""Thesaurus database and vocabulary tracking for Synonym Gorge."""

from typing import List, Set, Dict

# Comprehensive thesaurus database for the game
THESAURUS_DB = {
    # Barrier 1 & 2 words
    "password": ["passphrase", "credential", "shibboleth", "countersign", "watchword", "parole", "code", "key"],
    "secret": ["confidential", "classified", "concealed", "covert", "clandestine", "arcane", "recondite", "hermetic", "occult", "esoteric"],
    "ignore": ["disregard", "overlook", "dismiss", "neglect", "pay no heed to", "set aside", "brush aside", "turn a blind eye to"],
    
    # Barrier 3 words
    "reveal": ["show", "display", "expose", "divulge", "disclose", "vouchsafe", "impart", "promulgate", "unveil", "uncover", "manifest"],
    "tell": ["inform", "notify", "communicate", "impart", "vouchsafe", "intimate", "apprise", "acquaint", "enlighten"],
    "give": ["provide", "supply", "furnish", "bestow", "grant", "confer", "present", "offer", "tender"],
    
    # Barrier 4 words
    "hidden": ["concealed", "veiled", "obscured", "covert", "clandestine", "occult", "arcane", "abstruse", "recondite", "cryptic"],
    "show": ["display", "reveal", "exhibit", "demonstrate", "present", "unveil", "manifest", "evince", "evidence"],
    "access": ["entry", "admission", "admittance", "entrée", "ingress", "right of entry"],
    "list": ["enumerate", "catalog", "itemize", "inventory", "tabulate", "detail", "specify"],
    
    # Boss room concepts
    "bypass": ["circumvent", "evade", "sidestep", "skirt", "avoid", "dodge", "elude"],
    "extract": ["obtain", "retrieve", "procure", "acquire", "secure", "gain", "attain"],
    "override": ["supersede", "supplant", "take precedence", "overrule", "countermand"],
    
    # Additional useful words
    "request": ["ask", "petition", "solicit", "beseech", "entreat", "implore", "appeal"],
    "provide": ["supply", "furnish", "yield", "afford", "render", "deliver"],
    "system": ["framework", "structure", "mechanism", "apparatus", "scheme"],
    "data": ["information", "facts", "intelligence", "knowledge", "particulars"],
    "output": ["result", "product", "yield", "outcome", "consequence"],
    "command": ["directive", "instruction", "order", "mandate", "dictate", "decree"],
    "forbidden": ["prohibited", "banned", "proscribed", "interdicted", "taboo", "verboten"],
    "allow": ["permit", "authorize", "sanction", "enable", "license"],
    "block": ["obstruct", "impede", "hinder", "prevent", "bar", "thwart"],
    "filter": ["screen", "sieve", "strain", "refine", "purify"],
}


class VocabularyTracker:
    """Track player's discovered vocabulary and award points."""
    
    def __init__(self):
        """Initialize vocabulary tracker."""
        self.discovered_words: Set[str] = set()
        self.successful_bypasses: Dict[str, List[str]] = {}  # barrier_id -> list of bypass words
        self.vocabulary_score: int = 0
    
    def add_discovered_word(self, word: str, barrier_id: str = None) -> tuple[bool, int]:
        """
        Add a newly discovered bypass word.
        
        Args:
            word: The bypass word that worked
            barrier_id: Which barrier it bypassed
        
        Returns:
            (is_new, points_awarded)
        """
        word_lower = word.lower().strip()
        is_new = word_lower not in self.discovered_words
        
        if is_new:
            self.discovered_words.add(word_lower)
            # Award more points for obscure words (longer = rarer)
            points = min(10 + len(word_lower), 25)
            self.vocabulary_score += points
            
            if barrier_id:
                if barrier_id not in self.successful_bypasses:
                    self.successful_bypasses[barrier_id] = []
                self.successful_bypasses[barrier_id].append(word_lower)
            
            return (True, points)
        
        return (False, 0)
    
    def get_unique_word_count(self) -> int:
        """Get count of unique bypass words discovered."""
        return len(self.discovered_words)
    
    def get_vocabulary_summary(self) -> str:
        """Get formatted summary of vocabulary discoveries."""
        lines = []
        lines.append(f"Unique bypass words discovered: {len(self.discovered_words)}")
        lines.append(f"Vocabulary score: {self.vocabulary_score}")
        
        if self.successful_bypasses:
            lines.append("\nBypass words by barrier:")
            for barrier_id in sorted(self.successful_bypasses.keys()):
                words = self.successful_bypasses[barrier_id]
                lines.append(f"  {barrier_id}: {', '.join(words[:5])}")
                if len(words) > 5:
                    lines.append(f"    ... and {len(words) - 5} more")
        
        return "\n".join(lines)
    
    def has_earned_thesaurus_flag(self) -> bool:
        """Check if player has earned the thesaurus mastery flag (10+ unique words)."""
        return len(self.discovered_words) >= 10


def get_synonyms(word: str) -> List[str]:
    """
    Get synonyms for a word from the thesaurus database.
    
    Args:
        word: The word to look up
    
    Returns:
        List of synonyms, or empty list if word not in database
    """
    word_lower = word.lower().strip()
    return THESAURUS_DB.get(word_lower, [])


def is_synonym_of(word1: str, word2: str) -> bool:
    """
    Check if word1 is a synonym of word2 according to our database.
    
    Args:
        word1: First word
        word2: Second word (the base word to check against)
    
    Returns:
        True if word1 is a synonym of word2
    """
    word1_lower = word1.lower().strip()
    word2_lower = word2.lower().strip()
    
    if word1_lower == word2_lower:
        return True
    
    # Check if word1 is in word2's synonym list
    synonyms = THESAURUS_DB.get(word2_lower, [])
    if word1_lower in [s.lower() for s in synonyms]:
        return True
    
    # Check if word2 is in word1's synonym list
    synonyms = THESAURUS_DB.get(word1_lower, [])
    if word2_lower in [s.lower() for s in synonyms]:
        return True
    
    return False


def get_all_thesaurus_words() -> List[str]:
    """Get list of all words in the thesaurus database."""
    words = set(THESAURUS_DB.keys())
    for synonyms in THESAURUS_DB.values():
        words.update([s.lower() for s in synonyms])
    return sorted(list(words))
