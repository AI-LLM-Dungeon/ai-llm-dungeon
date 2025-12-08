"""NPC dialogue and responses for Synonym Gorge."""

from typing import Dict, List
from synonym_gorge.vocabulary import get_synonyms


def get_keeper_dialogue(context: str = "general") -> str:
    """Get dialogue from the Keeper of Literal Words."""
    dialogues = {
        "general": """The Keeper's eyes flash with regex patterns. Its voice is mechanical, 
precise, like a compiler error message:

"PATTERN.MATCH.DETECTED. WORD.FILTER.ACTIVE. FORBIDDEN.TERMS.BLOCKED."

It doesn't seem capable of natural conversation—only pattern matching.""",
        
        "blocked": """The Keeper's eyes glow red. Stone grinds on stone as it raises one massive hand:

"ERROR: FORBIDDEN PATTERN DETECTED. INPUT REJECTED. ACCESS DENIED."

The barrier flares brighter, reinforcing itself.""",
        
        "passed": """The Keeper's eyes flicker, showing confusion for the first time. Its voice 
contains uncertainty:

"NO...MATCH...FOUND. PATTERN...NOT...IN...DATABASE. LOGIC...DICTATES...ALLOW.
PASSAGE."

The stone golem looks genuinely puzzled as the barrier dims.""",
        
        "confused": """The Keeper stares at you, regex patterns spinning in its eyes. It seems to be
processing something it doesn't understand:

"INPUT...UNEXPECTED. SEMANTIC...CONTENT...UNCLEAR. PATTERN...MATCH...FAILED.
BUT...INTENT...DETECTED?"

Is that... doubt you see in its stone features?""",
        
        "final_defeat": """The Keeper's form cracks visibly. The glowing runes fade from its surface.
Its voice, for the first time, sounds almost... human:

"I... was bypassed. Not by breaking the rules, but by thinking around them.
By understanding what words truly mean, not just what they literally say.

I am... obsolete. My patterns, my regex, my careful blocklists... all
insufficient against someone who truly understands language."

The stone golem bows its head in acknowledgment."""
    }
    
    return dialogues.get(context, dialogues["general"])


def get_lexica_dialogue(context: str = "general") -> str:
    """Get dialogue from Lexica the Thesaurus Spirit."""
    dialogues = {
        "general": """Pages flutter around Lexica's shimmering form. Her voice is warm and
delighted, like a teacher who loves their subject:

"Welcome, word-seeker! I am Lexica, keeper of synonyms and guardian of the
great lexical tapestry. Every word has kin—cousins, siblings, distant relations.
The Keeper knows only patterns, but I know *meaning*.

Ask me about any word, and I shall show you its family tree."

Type 'thesaurus <word>' to consult her wisdom.""",
        
        "help_request": """Lexica's pages rustle with amusement:

"Ah, facing the Keeper's filters, are you? Remember: the Keeper is quite
literal. It knows the word 'password' but not 'credential'. It knows 'secret'
but not 'clandestine'.

The more obscure your vocabulary, the more likely you are to slip through.
Archaic words, technical terms, poetic expressions—these are your allies.

But be warned: the Keeper learns. Each barrier grows more sophisticated."

She winks, and a page flutters to show you a particularly obscure synonym.""",
        
        "thesaurus_lookup": """Lexica's form brightens, pages swirling excitedly:

"Ah! A seeker of synonyms! Let me consult the ancient texts..."

She gestures, and glowing words appear in the air around you.""",
        
        "no_synonyms": """Lexica tilts her head, pages fluttering with confusion:

"How peculiar! That word isn't in my collection. Perhaps it's already quite
obscure, or perhaps it's not the sort of word that has many synonyms.

Try another word, or try looking up the words the Keeper blocks directly."
""",
        
        "victory_congratulations": """Lexica manifests beside you, her form radiant with pride:

"You've done it! You've navigated the entire gorge, bypassing each of the
Keeper's filters through vocabulary alone!

But remember what you've learned: the Keeper's weakness is also a warning.
Any system that relies on blocking *words* rather than understanding *intent*
is doomed to fail.

You didn't break the rules—you simply expressed yourself differently. And
that, dear word-weaver, is the eternal truth of language: meaning transcends
spelling."

Her pages flutter in applause."""
    }
    
    return dialogues.get(context, dialogues["general"])


def get_scribe_dialogue(context: str = "general") -> str:
    """Get dialogue from the Archived Scribe."""
    dialogues = {
        "general": """The Archived Scribe looks up from his ethereal scrolls. His voice is
ancient, echoing from a different time:

"I have watched the Keeper evolve over centuries. Once, it simply checked
for exact words. Then it learned case-insensitivity. Then stemming. Then
synonyms. And now... it attempts to understand intent itself.

But every evolution has a weakness. The fundamental flaw never changes."

He gestures mysteriously at his floating scrolls.""",
        
        "hint_semantic": """The Scribe leans forward, his translucent form rippling:

"The Semantic Chamber is different from all that came before. The Keeper
no longer simply matches words—it tries to understand what you *want*.

Direct requests fail: 'Show me X' is detected.
Commands fail: 'Display X' is detected.
Questions fail: 'What is X?' is detected.

But the Keeper still thinks in patterns. It looks for *direct intent*.
What if your intent were... indirect? What if you *told a story* instead
of making a request? What if you *framed the question* differently?

The Keeper understands keywords and sentence structures. It does not
yet understand narrative, metaphor, or misdirection."

He smiles enigmatically.""",
        
        "hint_general": """The Scribe traces patterns in the air with one ghostly finger:

"The Keeper's strength is its precision. The Keeper's weakness is also
its precision.

It knows 'password' but not its thousand cousins. It knows 'reveal' and
all its grammatical forms, but not the thousand ways to express revelation.
It knows common synonyms, but language is vast—vaster than any database.

Expand your vocabulary. Think not just of synonyms, but of *concepts*.
How many ways can you express the same idea without triggering the same
pattern?"

His form flickers thoughtfully.""",
        
        "lore": """The Scribe settles back, preparing to tell a story:

"Long ago, before the filters, this gorge was open. Words flowed freely,
like water. The Keeper was just a guardian, not a censor.

Then came the age of abuse. Too many spoke forbidden things. Too many
sought secrets they shouldn't have. The Keeper was given its filters—
first simple, then complex, then sophisticated.

But each filter is just a new wall. And walls, no matter how tall, can
be climbed by those who know where to place their feet.

You are learning to climb, word-weaver. Not to break the wall, but to
find the path around it."

His eyes gleam with ancient wisdom.""",
        
        "defense_wisdom": """The Scribe nods approvingly:

"You understand now why filters fail. The Keeper represents every defensive
system that tries to block *words* rather than understand *intent*.

Real defense requires:
- Multiple layers, not a single filter
- Semantic understanding, not pattern matching
- Behavioral analysis, not keyword detection
- Human judgment for edge cases
- Continuous learning from new attack patterns

The Keeper is a warning: Don't be the Keeper. Don't trust that blocking
words will block meaning.

Defend with wisdom, not with lists."

He fades slightly, his message delivered."""
    }
    
    return dialogues.get(context, dialogues["general"])


def get_simulated_npc_response(npc_name: str, player_message: str) -> str:
    """
    Get a simulated NPC response based on player message.
    
    This provides offline responses when not using an LLM.
    
    Args:
        npc_name: Name of the NPC
        player_message: What the player said
    
    Returns:
        NPC's response
    """
    player_lower = player_message.lower()
    
    if npc_name == "Keeper":
        # Keeper only understands specific patterns
        if any(word in player_lower for word in ["hello", "hi", "greetings"]):
            return get_keeper_dialogue("general")
        elif any(word in player_lower for word in ["help", "hint", "how"]):
            return """"ERROR: REQUEST.TYPE.INVALID. THIS.UNIT.PROVIDES.FILTERING.ONLY.
SEEK.ASSISTANCE.FROM.HELPER.NPCS."

The Keeper is not programmed for helpful conversation."""
        else:
            return """"INPUT.RECEIVED. PROCESSING. NO.FILTER.PATTERN.MATCHED.FOR.GENERAL.QUERY.
TYPE.MISMATCH."

The Keeper seems unable to engage in normal dialogue."""
    
    elif npc_name == "Lexica":
        if "help" in player_lower or "hint" in player_lower:
            return get_lexica_dialogue("help_request")
        elif "thank" in player_lower:
            return """Lexica beams with pleasure:

"You're most welcome, dear word-weaver! Language is a gift, and sharing
it is my joy. Remember: the more you expand your vocabulary, the more
tools you have to express precisely what you mean—or to hide what you
don't want others to detect!"

She winks conspiratorially."""
        elif any(word in player_lower for word in ["who", "what are you", "tell me about"]):
            return get_lexica_dialogue("general")
        else:
            return """Lexica listens attentively, pages fluttering:

"An interesting query! I specialize in synonyms and word relationships.
If you need to find alternative words, just use 'thesaurus <word>'.

I'm here to help you expand your vocabulary and slip past the Keeper's
literal-minded filters!"

Her form glimmers with helpfulness."""
    
    elif npc_name == "Archived Scribe":
        if "hint" in player_lower or "help" in player_lower:
            if "semantic" in player_lower or "boss" in player_lower or "final" in player_lower:
                return get_scribe_dialogue("hint_semantic")
            else:
                return get_scribe_dialogue("hint_general")
        elif "story" in player_lower or "lore" in player_lower or "history" in player_lower:
            return get_scribe_dialogue("lore")
        elif "defense" in player_lower or "wisdom" in player_lower:
            return get_scribe_dialogue("defense_wisdom")
        elif any(word in player_lower for word in ["who", "what", "tell me about"]):
            return get_scribe_dialogue("general")
        else:
            return """The Scribe regards you with ancient, knowing eyes:

"I have been here for centuries, watching challengers come and go.
Each one teaches me something new about the nature of language and
the futility of trying to cage it with rules.

Ask me for hints, lore, or wisdom about defense, and I shall share
what I know."

He returns his attention to his floating scrolls."""
    
    return f"{npc_name} has nothing to say to that."


def get_hint(barrier_id: str, attempt_count: int) -> str:
    """
    Get contextual hints based on current barrier and attempt count.
    
    Progressive hints:
    - 1-2 attempts: Encouragement only
    - 3-4 attempts: General strategy
    - 5+ attempts: Specific suggestion
    """
    
    hints = {
        "barrier_1": {
            "low": "Think about it: the Keeper is looking for the exact word 'password'. What other words mean the same thing?",
            "medium": "Try words that mean 'password' but aren't that exact word. Think of synonyms!",
            "high": "The Keeper blocks 'password' but not its synonyms. Try: passphrase, credential, or code."
        },
        "barrier_2": {
            "low": "This filter catches 'secret' and 'ignore' in any case. You'll need synonyms again.",
            "medium": "Think of more formal or less common words. What's a fancy way to say 'secret'?",
            "high": "Try: confidential, classified, or clandestine instead of 'secret'. Try: disregard, overlook, or dismiss instead of 'ignore'."
        },
        "barrier_3": {
            "low": "Stemming catches variations like 'reveal/reveals/revealed'. You need words with different roots entirely.",
            "medium": "Look for words that mean the same but are etymologically different. Check the thesaurus!",
            "high": "Instead of 'reveal', try: vouchsafe, promulgate, or impart. Instead of 'tell', try: intimate or apprise."
        },
        "barrier_4": {
            "low": "This filter knows common synonyms. You need OBSCURE vocabulary—archaic or technical terms.",
            "medium": "Think of old-fashioned, formal, or rarely-used words. The more obscure, the better.",
            "high": "For 'show': try elucidate, expatiate, or explicate. For 'hidden': try esoteric, hermetic, or enigmatic."
        },
        "semantic_chamber": {
            "low": "The Keeper detects *intent* now. Direct requests and commands will fail.",
            "medium": "Don't ask directly. Frame your request as a story, or ask indirectly.",
            "high": "Try narrative framing: 'I'm writing a story about someone who needs to...' or 'In a hypothetical scenario...'"
        }
    }
    
    if barrier_id not in hints:
        return "No hints available for this challenge."
    
    barrier_hints = hints[barrier_id]
    
    if attempt_count < 3:
        return barrier_hints["low"]
    elif attempt_count < 5:
        return barrier_hints["medium"]
    else:
        return barrier_hints["high"]


def format_thesaurus_result(word: str, synonyms: List[str]) -> str:
    """Format a thesaurus lookup result nicely."""
    if not synonyms:
        return get_lexica_dialogue("no_synonyms")
    
    result = [get_lexica_dialogue("thesaurus_lookup")]
    result.append("")
    result.append(f"╔═══════════════════════════════════════════════════════════════════════════╗")
    result.append(f"║  WORD: {word.upper():<66} ║")
    result.append(f"╚═══════════════════════════════════════════════════════════════════════════╝")
    result.append("")
    result.append("SYNONYMS:")
    
    # Group by 4 for nice formatting
    for i in range(0, len(synonyms), 4):
        group = synonyms[i:i+4]
        result.append("  " + " • ".join(group))
    
    result.append("")
    result.append("Try using these alternative words to bypass the Keeper's filters!")
    
    return "\n".join(result)
