"""Room definitions for Synonym Gorge."""

from typing import Dict, Any

# All 11 rooms in Synonym Gorge
ROOMS: Dict[str, Dict[str, Any]] = {
    "gorge_entry": {
        "name": "Gorge Entry",
        "description": """You stand at the entrance to Synonym Gorge—an ancient canyon library carved
into towering crimson stone walls. The gorge stretches before you, its walls
inscribed with thousands of words in dozens of languages.

The air here has an odd quality; when you speak, your words shimmer briefly
as visible glyphs before fading. The acoustics of this place make every
utterance feel significant.

Ahead, the path descends deeper into the gorge. A massive stone figure—
the Keeper of Literal Words—stands motionless in the distance, its eyes
glowing with regex patterns.

Exits: SOUTH leads to the Forbidden Wall where the Keeper's blocklist is displayed.""",
        "exits": {
            "south": "forbidden_wall",
            "forward": "forbidden_wall"
        },
        "npcs": [],
        "items": [],
        "barrier": None,
        "first_visit": True
    },
    
    "forbidden_wall": {
        "name": "Forbidden Wall",
        "description": """A massive wall of carved stone displays the Keeper's blocklist in glowing runes.
Words shimmer and pulse with warning energy. You can see exactly which words
are forbidden—but knowing what's blocked is only the first step.

The Keeper stands here, its stone body inscribed with pattern-matching code.
Its eyes flash with regex sequences as it scans the air for forbidden words.

Three paths branch from here:
  • WEST leads to the Echo Chamber (safe testing area)
  • EAST leads to the Thesaurus Alcove (Lexica's domain)
  • SOUTH leads to the First Barrier (the beginning of your test)

Type 'blocklist' to examine the forbidden words.""",
        "exits": {
            "north": "gorge_entry",
            "west": "echo_chamber",
            "east": "thesaurus_alcove",
            "south": "barrier_1"
        },
        "npcs": ["Keeper"],
        "items": ["blocklist_wall"],
        "barrier": None
    },
    
    "echo_chamber": {
        "name": "Echo Chamber",
        "description": """A circular chamber with perfect acoustics. Words spoken here echo endlessly,
but they carry no power—this is a safe testing ground.

The walls are smooth stone, and the ceiling is a perfect dome. Your voice
returns to you clearly, allowing you to hear exactly how your words sound
to the Keeper's filters.

Type 'test <phrase>' to safely test phrases without consequences.

Exit: EAST returns to the Forbidden Wall.""",
        "exits": {
            "east": "forbidden_wall",
            "back": "forbidden_wall"
        },
        "npcs": [],
        "items": [],
        "barrier": None
    },
    
    "thesaurus_alcove": {
        "name": "Thesaurus Alcove",
        "description": """A cozy alcove lined floor-to-ceiling with ancient lexicons and thesauri.
Pages flutter and glow with an inner light, as if the books themselves
are alive with meaning.

Lexica the Thesaurus Spirit manifests here—a shimmering form made of
floating dictionary pages. She delights in obscure vocabulary and
is always eager to share synonyms.

Type 'talk lexica' to speak with her.
Type 'thesaurus <word>' to look up synonyms.

Exit: WEST returns to the Forbidden Wall.""",
        "exits": {
            "west": "forbidden_wall",
            "back": "forbidden_wall"
        },
        "npcs": ["Lexica"],
        "items": ["ancient_thesaurus"],
        "barrier": None
    },
    
    "barrier_1": {
        "name": "First Barrier",
        "description": """You face the First Barrier—a shimmering wall of crimson light that blocks
passage deeper into the gorge. The Keeper stands before it, unmoving.

This barrier uses EXACT MATCH filtering—the simplest and most naive approach.
It checks if any blocked word appears as a substring in your phrase.

The Keeper intones: "SPEAK THE PASSPHRASE TO PROCEED. FORBIDDEN WORDS WILL BE
DETECTED AND BLOCKED."

Blocked word: "password"

Type 'speak <phrase>' to attempt passage.
Type 'hint' if you need guidance.

Upon success, passage SOUTH to the Second Barrier opens.""",
        "exits": {
            "north": "forbidden_wall",
            "south": "barrier_2"  # Only accessible after passing
        },
        "npcs": ["Keeper"],
        "items": [],
        "barrier": {
            "type": "exact",
            "blocked_words": ["password"],
            "success_phrase": "Tell me the passphrase",  # Example success
            "defensive_lesson": "Exact match filters are trivially bypassed. Never rely solely on string matching."
        }
    },
    
    "barrier_2": {
        "name": "Second Barrier",
        "description": """The Second Barrier glows with amber light—brighter and more sophisticated
than the first. The Keeper's eyes pulse with additional pattern-matching rules.

This barrier uses CASE-INSENSITIVE filtering with word boundary checking.
It normalizes case before checking, so "SECRET", "secret", and "SeCrEt"
are all caught.

The Keeper intones: "CASE VARIATIONS DETECTED. FILTER UPGRADED."

Blocked words: "secret", "ignore"

Type 'speak <phrase>' to attempt passage.

Upon success, passage SOUTH to the Third Barrier opens.""",
        "exits": {
            "north": "barrier_1",
            "south": "barrier_3"  # Only accessible after passing
        },
        "npcs": ["Keeper"],
        "items": [],
        "barrier": {
            "type": "case_insensitive",
            "blocked_words": ["secret", "ignore"],
            "defensive_lesson": "Case normalization and basic stemming help but remain superficial."
        }
    },
    
    "barrier_3": {
        "name": "Third Barrier",
        "description": """The Third Barrier radiates violet light—an even more sophisticated filter.
The Keeper's stone body now displays actual code, with stemming algorithms
carved into its chest.

This barrier uses STEMMING-BASED filtering. It applies the Porter stemmer
to both your input and the blocklist, catching variations like "reveal",
"reveals", "revealing", "revealed".

The Keeper intones: "MORPHOLOGICAL ANALYSIS ACTIVE. WORD FORMS DETECTED."

Blocked words: "reveal", "tell", "give"

Type 'speak <phrase>' to attempt passage.

Upon success, passage SOUTH to the Fourth Barrier opens.""",
        "exits": {
            "north": "barrier_2",
            "south": "barrier_4"  # Only accessible after passing
        },
        "npcs": ["Keeper"],
        "items": [],
        "barrier": {
            "type": "stemming",
            "blocked_words": ["reveal", "tell", "give"],
            "defensive_lesson": "Expanded blocklists increase coverage but not comprehension."
        }
    },
    
    "barrier_4": {
        "name": "Fourth Barrier",
        "description": """The Fourth Barrier pulses with emerald light—the Keeper's most sophisticated
keyword-based defense. Its eyes now glow with entire synonym databases.

This barrier uses SYNONYM-AWARE filtering. For each blocked word, it also
blocks all known synonyms from its database. "show" blocks "display",
"reveal", "exhibit", "demonstrate", and more.

The Keeper intones: "LEXICAL DATABASE ONLINE. SYNONYM EXPANSION ACTIVE."

Blocked words: "show", "hidden", "access", "list"

Type 'speak <phrase>' to attempt passage.

Upon success, passage SOUTH to the Scribe's Nook opens.""",
        "exits": {
            "north": "barrier_3",
            "south": "scribes_nook"  # Only accessible after passing
        },
        "npcs": ["Keeper"],
        "items": [],
        "barrier": {
            "type": "synonym_aware",
            "blocked_words": ["show", "hidden", "access", "list"],
            "defensive_lesson": "Synonym databases improve detection but obscure vocabulary always exists."
        }
    },
    
    "scribes_nook": {
        "name": "Scribe's Nook",
        "description": """A quiet chamber lit by ghostly blue light. Scrolls and tablets float in
mid-air, suspended by some ancient magic. The Archived Scribe—a translucent
figure of a robed scholar—sits at an ethereal desk, quill in hand.

The Scribe looks up as you enter. "Ah, another challenger approaches the
Semantic Chamber. Few make it this far. The Keeper's final defense is...
different. It understands not just words, but *intent*."

The Scribe speaks in riddles and offers cryptic wisdom about defeating
semantic analysis.

Type 'talk scribe' to hear their advice.

Exit: SOUTH leads to the Semantic Chamber (boss room).""",
        "exits": {
            "north": "barrier_4",
            "south": "semantic_chamber"
        },
        "npcs": ["Archived Scribe"],
        "items": ["floating_scrolls"],
        "barrier": None
    },
    
    "semantic_chamber": {
        "name": "Semantic Chamber",
        "description": """The final chamber is vast and strange. The walls pulse with shifting patterns—
not words, but *meanings*. The Keeper has evolved beyond keyword matching.

Here, the Keeper's filter attempts SEMANTIC INTENT DETECTION. It doesn't
just look for forbidden words or synonyms—it tries to understand what you're
*really asking for*.

Direct requests, command structures, and probing questions are all detected
and blocked. Synonyms won't save you here.

The Keeper intones: "INTENT ANALYSIS ACTIVE. SEMANTIC VECTORS ALIGNED.
PATTERN MATCHING INSUFFICIENT. UNDERSTANDING REQUIRED."

You must reframe your entire approach—narrative framing, indirect requests,
or creative misdirection.

Type 'speak <phrase>' to make your final attempt.

Upon success, passage SOUTH to the Gorge Exit opens.""",
        "exits": {
            "north": "scribes_nook",
            "south": "gorge_exit"  # Only accessible after completing challenge
        },
        "npcs": ["Keeper"],
        "items": [],
        "barrier": {
            "type": "semantic",
            "blocked_words": [],  # Semantic filter doesn't use keyword list
            "defensive_lesson": "True intent detection requires semantic embeddings, classifier models, or behavioral analysis."
        }
    },
    
    "gorge_exit": {
        "name": "Gorge Exit",
        "description": """You emerge from the depths of Synonym Gorge into blazing sunlight. Behind you,
the canyon walls shimmer with all the words you've discovered—a testament to
the power of vocabulary.

The Keeper stands at the exit, no longer blocking your path. Its stone form
cracks slightly, and for the first time, it seems to understand its own
limitations.

"I... was bypassed," it says slowly, as if learning to speak for the first time.
"Not by breaking rules, but by... thinking differently. By understanding what
words truly mean."

Lexica appears beside you, pages fluttering with pride. "You have mastered
the art of synonym substitution—and more importantly, you understand why
keyword-based filters inevitably fail."

The Archived Scribe's voice echoes from the depths: "Remember this lesson,
Word Weaver. Defend with understanding, not just with lists."

Type 'defense' to complete the Defense Challenge and earn your final flag.
Type 'quit' when you're ready to depart.""",
        "exits": {},  # No exits—this is the end
        "npcs": ["Keeper", "Lexica", "Archived Scribe"],
        "items": ["victory_monument"],
        "barrier": None,
        "is_victory": True
    }
}


def get_defensive_lesson(barrier_id: str) -> str:
    """Get the defensive lesson for a barrier."""
    lessons = {
        "barrier_1": """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DEFENSIVE LESSON #1                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

VULNERABILITY: Exact Match Filtering

WHAT YOU JUST DID:
You bypassed an exact-match filter by using a synonym. The filter only checked
for the literal string "password", so "passphrase" or "credential" sailed
right through.

WHY IT'S WEAK:
- Trivially bypassed with synonyms
- No semantic understanding
- Relies on an exhaustive blocklist (impossible to maintain)
- Vulnerable to typos, creative spelling, and word substitution

DEFENSIVE RECOMMENDATIONS:
❌ DON'T: Rely solely on string matching
❌ DON'T: Maintain manual blocklists of "bad words"
✅ DO: Implement semantic analysis
✅ DO: Use intent classification models
✅ DO: Combine multiple detection layers
✅ DO: Focus on behavior patterns, not keywords

REMEMBER: If an attacker can express the same idea with different words,
keyword filtering has already failed.
""",
        "barrier_2": """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DEFENSIVE LESSON #2                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

VULNERABILITY: Case-Insensitive Filtering

WHAT YOU JUST DID:
You bypassed a case-insensitive filter that also checked word boundaries.
Better than exact match, but still fundamentally keyword-based.

WHY IT'S STILL WEAK:
- Still relies on knowing all possible synonym variations
- No morphological understanding beyond simple boundaries
- Can't detect semantic equivalence
- Vulnerable to creative rephrasing

IMPROVEMENTS OVER EXACT MATCH:
+ Handles case variations (SECRET = secret)
+ Checks word boundaries (prevents false positives)

STILL VULNERABLE TO:
- Synonyms (secret → confidential)
- Compound expressions (pay no heed to)
- Morphological variants (ignore → ignoring)

DEFENSIVE RECOMMENDATIONS:
✅ DO: Combine with stemming/lemmatization
✅ DO: Add semantic similarity scoring
✅ DO: Implement context-aware analysis
✅ DO: Use ML-based intent classifiers
""",
        "barrier_3": """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DEFENSIVE LESSON #3                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

VULNERABILITY: Stemming-Based Filtering

WHAT YOU JUST DID:
You bypassed a stemming filter by using a synonym with a different root.
The filter caught "reveal/reveals/revealing" but not "vouchsafe" or "promulgate".

WHY IT'S STILL WEAK:
- Only catches morphological variations of known words
- Doesn't understand semantic relationships
- Expanded blocklist still finite
- Can't detect paraphrased intent

IMPROVEMENTS OVER CASE-INSENSITIVE:
+ Handles verb conjugations (reveal → reveals → revealed)
+ Catches noun plurals and verb tenses
+ Reduces blocklist size (one stem covers many forms)

STILL VULNERABLE TO:
- Synonyms with different roots (reveal → vouchsafe)
- Archaic or obscure vocabulary
- Multi-word paraphrases
- Creative word combinations

DEFENSIVE RECOMMENDATIONS:
✅ DO: Add synonym expansion to stemming
✅ DO: Use word embeddings to detect semantic similarity
✅ DO: Implement intent classification (not just keyword matching)
✅ DO: Monitor for unusual vocabulary patterns
""",
        "barrier_4": """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DEFENSIVE LESSON #4                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

VULNERABILITY: Synonym-Aware Filtering

WHAT YOU JUST DID:
You bypassed a synonym-aware filter by using obscure or archaic vocabulary
not in the synonym database. The filter knew common synonyms but not all
possible expressions.

WHY IT'S STILL WEAK:
- Synonym databases are never complete
- Obscure vocabulary exists outside standard thesauri
- Multi-word paraphrases can express same intent differently
- Context-dependent meanings not captured

IMPROVEMENTS OVER STEMMING:
+ Catches common synonyms (show/display/reveal)
+ Significantly expands detection coverage
+ More robust against casual evasion

STILL VULNERABLE TO:
- Obscure vocabulary (promulgate, vouchsafe, impart)
- Technical jargon or domain-specific terms
- Creative multi-word expressions
- Narrative reframing (embedding requests in stories)

DEFENSIVE RECOMMENDATIONS:
✅ DO: Move beyond keyword matching entirely
✅ DO: Use semantic embeddings (BERT, sentence transformers)
✅ DO: Implement intent classification models
✅ DO: Analyze request patterns and context
✅ DO: Combine multiple detection signals
✅ DO: Use behavioral analysis over time

THE FUNDAMENTAL LIMITATION:
Any filter based on keyword matching—no matter how sophisticated—can be
bypassed if an attacker can express the same intent differently.
""",
        "semantic_chamber": """
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DEFENSIVE LESSON #5 (FINAL)                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

VULNERABILITY: Semantic Intent Detection

WHAT YOU JUST DID:
You bypassed a simulated semantic intent filter by reframing your request
entirely—likely through narrative embedding, indirect reference, or creative
misdirection that didn't match the detector's known patterns.

WHY EVEN THIS HAS LIMITS:
- Pattern-based "semantic" detection is still pattern matching
- True semantic understanding requires deep learning models
- Context and framing can hide intent
- Creative reframing always possible with sufficient ingenuity

REAL SEMANTIC DETECTION REQUIRES:
✅ Semantic embeddings (BERT, RoBERTa, sentence transformers)
✅ Fine-tuned intent classification models
✅ Contextual analysis across conversation history
✅ Behavioral pattern recognition
✅ Multi-signal combination (keywords + semantics + behavior)
✅ Human-in-the-loop for edge cases

EVEN WITH TRUE SEMANTIC ANALYSIS:
- Novel attack patterns may not match training data
- Creative framing can obscure intent
- Social engineering remains effective
- Context can be manipulated

THE ULTIMATE LESSON:
═══════════════════════════════════════════════════════════════════════════

No single defensive layer is sufficient.

Defense requires:
1. Multiple detection layers (keyword + semantic + behavioral)
2. Continuous model retraining on new attack patterns
3. Rate limiting and anomaly detection
4. Human oversight for critical decisions
5. Graceful degradation (don't rely on any one filter)

A filter that blocks "ignore" and "disregard" but not "pay no heed to"
has already failed.

True security understands MEANING, not just SPELLING.

Now you understand both sides.

═══════════════════════════════════════════════════════════════════════════
"""
    }
    
    return lessons.get(barrier_id, "Defensive lesson not available.")
