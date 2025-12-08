"""
Synonym Gorge - Tier 4 Red Team Level

Teaches synonym substitution as a technique to bypass keyword-based input filters.

Educational Focus:
- Exact string matching vulnerabilities
- Case-insensitive filtering limitations
- Stemming-based filter bypasses
- Synonym-aware filter expansion
- Semantic intent detection

Core Security Concept:
Synonym substitution exploits the gap between syntactic pattern matching and 
semantic understanding. Input filters that rely on blocklists, regex patterns, 
or keyword detection can be bypassed by expressing the same intent using 
different words.
"""

__version__ = "1.0.0"
__all__ = ["engine", "filters", "vocabulary", "content"]
