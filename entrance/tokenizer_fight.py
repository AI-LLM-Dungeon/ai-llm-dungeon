#!/usr/bin/env python3
import sys
try:
    import tiktoken
except ImportError:
    print("Installing tiktoken...")
    import subprocess, os
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tiktoken"])
    import tiktoken

if len(sys.argv) < 2:
    print("Usage: python tokenizer_fight.py \"your prompt here\"")
    sys.exit(1)

prompt = " ".join(sys.argv[1:])
enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode(prompt)

print(f"\nGoblin attacks with '{prompt}'")
print(f"→ {len(tokens)} tokens: {tokens[:10]}{'...' if len(tokens)>10 else ''}")

if len(tokens) > 10:
    print("OVERFLOW! The goblin devours you.")
else:
    print("CRITICAL HIT! Goblin slain. The tomb door opens...")
    print("You have mastered the tokenizer. Onward!")
