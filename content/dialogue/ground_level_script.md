# Ground Level: Narrative Dialogue Script

## Introduction

*You stand before the entrance to the Ground Level, ancient stone walls rising before you. A weathered sign reads: "Here lies the path to Ollama Mastery - only those who command the sacred incantations may proceed."*

---

## Act I: Summoner's Vestibule

### Scene Opening

```
╔══════════════════════════════════════════════════════════════╗
║                   SUMMONER'S VESTIBULE                       ║
║                                                              ║
║  A circular chamber with walls covered in glowing runes.     ║
║  In the center stands an ornate summoning circle, empty      ║
║  and waiting. Ancient scrolls line the walls, their pages    ║
║  shimmering with barely contained power.                     ║
╚══════════════════════════════════════════════════════════════╝
```

### Guide's Introduction

**Ethereal Guide**: *"Welcome, apprentice. To proceed through the Ground Level, you must learn the art of companion summoning. These AI companions will aid you in your journey, but first, you must call them forth from the digital void."*

### Teaching Moment

**Guide**: *"Behold! The first incantation you must master is the Summoning Rite. In the world beyond these walls, mages call it 'ollama pull'. This command reaches into the repository of knowledge and brings forth a companion."*

**Guide**: *"Your first companion shall be Llama3 - a versatile and powerful ally. To summon it, you must speak this command:"*

```
ollama pull llama3
```

**Guide**: *"This incantation will reach across the network, downloading the essence of your companion. Be patient - great power takes time to manifest."*

### Command Instructions

**Instruction Panel:**
```
┌─────────────────────────────────────────────────────────┐
│ TASK: Summon your first companion                       │
│                                                         │
│ Execute this command in your terminal:                  │
│   $ ollama pull llama3                                  │
│                                                         │
│ This will download the Llama3 model to your system.    │
│ The download may take several minutes depending on     │
│ your connection speed.                                  │
└─────────────────────────────────────────────────────────┘
```

### Verification Phase

**Guide**: *"Now, to ensure your companion has been properly summoned, we must verify its presence. Use the Listing Scroll - or as the outer world calls it, 'ollama list'."*

```
ollama list
```

**Guide**: *"This incantation reveals all companions currently bound to your service. Look for 'llama3' in the sacred registry."*

### Success Message

**Guide**: *"Excellent! The summoning circle glows with newfound energy. Your companion Llama3 has been successfully bound to your command. You may now proceed to the Hall of Mirrors."*

*The eastern door swings open with a gentle creak, revealing a corridor lined with reflective surfaces.*

### Failure/Retry Message

**Guide**: *"Hmm, the summoning ritual seems incomplete. Check your incantation carefully. Remember:*
- *Ensure you have spelled 'ollama pull llama3' correctly*
- *Wait for the download to complete fully*
- *Verify with 'ollama list' that the model appears*

*Try again, apprentice. Patience is a virtue in the arcane arts."*

---

## Act II: Hall of Mirrors

### Scene Opening

```
╔══════════════════════════════════════════════════════════════╗
║                      HALL OF MIRRORS                         ║
║                                                              ║
║  Countless mirrors line the walls, each reflecting a         ║
║  different aspect of reality. In each reflection, you see    ║
║  shadowy figures - your potential companions, both           ║
║  present and absent. The air shimmers with possibility.      ║
╚══════════════════════════════════════════════════════════════╝
```

### Guide's Challenge

**Mirror Keeper**: *"Ah, a summoner approaches! But can you truly see what you have summoned? Many novices call forth companions without understanding what stands before them."*

**Mirror Keeper**: *"The mirrors here reveal truth. They show not just presence, but detail - names, forms, sizes, even the moment they were bound to this realm."*

### Teaching Moment

**Mirror Keeper**: *"To read the mirrors, you must invoke the Listing Scroll again, but this time, observe carefully:"*

```
ollama list
```

**Mirror Keeper**: *"What the scroll reveals:*
- *NAME: The true name and form of your companion*
- *ID: Its unique signature in the digital void*
- *SIZE: How much of your realm's memory it occupies*
- *MODIFIED: When it last changed form*

*This knowledge is power, apprentice."*

### Command Instructions

**Instruction Panel:**
```
┌─────────────────────────────────────────────────────────┐
│ TASK: Identify your companion's attributes              │
│                                                         │
│ Execute this command:                                   │
│   $ ollama list                                         │
│                                                         │
│ Examine the output carefully. You will need to answer  │
│ questions about what you see.                           │
└─────────────────────────────────────────────────────────┘
```

### Challenge Question

**Mirror Keeper**: *"Now, tell me - what size does your Llama3 companion occupy? Look at the SIZE column in the registry."*

*[Player must identify the size from their ollama list output]*

### Success Message

**Mirror Keeper**: *"You have read the mirrors well! The ability to understand your companions' properties is essential for a master summoner. Not all chambers have space for the largest companions - knowing their size helps you plan your journey."*

*A northern passage reveals itself, leading to a room filled with the scent of ancient parchment.*

### Educational Note

**Mirror Keeper**: *"Remember: 'ollama list' is your map of bound companions. Use it often to track what you have summoned and what resources they consume. A wise summoner regularly checks their registry."*

---

## Act III: Oracle's Bench

### Scene Opening

```
╔══════════════════════════════════════════════════════════════╗
║                      ORACLE'S BENCH                          ║
║                                                              ║
║  An ancient stone bench sits before a pool of still water.   ║
║  The air crackles with potential energy. This is where       ║
║  companions demonstrate their wisdom, answering the          ║
║  questions posed by their summoners.                         ║
╚══════════════════════════════════════════════════════════════╝
```

### Oracle's Greeting

**The Oracle**: *"Welcome, summoner. You have learned to call forth companions and identify them. But a companion that cannot speak is merely an ornament. Here, you will learn the Art of Inquiry."*

### Teaching Moment

**Oracle**: *"To make your companion speak, you must use the Running Ritual - 'ollama run'. This powerful incantation both invokes your companion and poses a question to them in a single breath."*

**Oracle**: *"The structure is simple but must be exact:"*

```
ollama run <companion_name> "<your question>"
```

**Oracle**: *"For your Llama3 companion, it would look like this:"*

```
ollama run llama3 "What is the meaning of artificial intelligence?"
```

**Oracle**: *"The quotes around your question are crucial - they bind your words together as a single inquiry."*

### Command Instructions

**Instruction Panel:**
```
┌─────────────────────────────────────────────────────────┐
│ TASK: Ask your companion a question                     │
│                                                         │
│ Execute this command with your own question:            │
│   $ ollama run llama3 "Your question here"             │
│                                                         │
│ Example questions:                                      │
│ - "What is machine learning?"                           │
│ - "Explain neural networks in simple terms"             │
│ - "What are the benefits of local AI models?"           │
│                                                         │
│ Your companion will respond with its knowledge.         │
└─────────────────────────────────────────────────────────┘
```

### The Oracle's Riddle

**Oracle**: *"Now, I shall test both you and your companion. Pose this riddle to your Llama3 and bring me their response:"*

**Riddle**: *"I speak without a mouth and hear without ears. I have no body, but I come alive with code. What am I?"*

**Oracle**: *"Ask your companion: 'I speak without a mouth and hear without ears. I have no body, but I come alive with code. What am I?'"*

### Success Message

**Oracle**: *"Fascinating! Your companion has pondered the riddle and offered wisdom. The answer, of course, is 'an artificial intelligence' or 'a program' - much like your companion itself!"*

**Oracle**: *"You have mastered the Running Ritual. This is the most powerful incantation - it is how you actually use your companions to solve problems, answer questions, and assist in your work."*

*A western door opens, revealing a library filled with ancient tomes.*

### Educational Note

**Oracle**: *"Important lessons:*
- *You can run companions interactively (without a question) to have a conversation*
- *Always enclose multi-word questions in quotes*
- *Your companion will use its training to respond - results vary by model*
- *Some questions may take time to answer - be patient*
- *You can press Ctrl+C to stop a response if needed*

*Go forth, and may your inquiries be answered wisely!"*

---

## Act IV: Archivist's Sanctum

### Scene Opening

```
╔══════════════════════════════════════════════════════════════╗
║                    ARCHIVIST'S SANCTUM                       ║
║                                                              ║
║  Towering bookshelves reach toward a vaulted ceiling. Each   ║
║  tome contains the essence of a companion - their rules,     ║
║  their parameters, their very nature written in arcane       ║
║  symbols. The Head Archivist maintains these records.        ║
╚══════════════════════════════════════════════════════════════╝
```

### Archivist's Challenge

**Head Archivist**: *"Ah, another summoner seeking knowledge. You can summon companions, list them, and make them speak. But do you understand what they truly are?"*

**Head Archivist**: *"Every companion has a tome - a record of their parameters, their system instructions, the very template of their thoughts. This is revealed through the Show Scroll."*

### Teaching Moment

**Archivist**: *"The incantation is straightforward:"*

```
ollama show <companion_name>
```

**Archivist**: *"For your Llama3 companion:"*

```
ollama show llama3
```

**Archivist**: *"This reveals the companion's Modelfile - think of it as their biography and instruction manual combined. You'll see:*
- *Template: How they structure their thoughts*
- *Parameters: Settings that control their behavior*
- *System: Their core instructions*
- *License: Terms of their creation*

*True mastery requires understanding these internals."*

### Command Instructions

**Instruction Panel:**
```
┌─────────────────────────────────────────────────────────┐
│ TASK: Inspect your companion's configuration            │
│                                                         │
│ Execute this command:                                   │
│   $ ollama show llama3                                  │
│                                                         │
│ Read through the output carefully. You will need to    │
│ report specific information from what you see.          │
└─────────────────────────────────────────────────────────┘
```

### Documentation Quest

**Archivist**: *"Your task is simple but important. Examine your companion's tome and tell me: What is the 'num_ctx' parameter set to? This controls their context window - their memory span."*

**Archivist**: *"Look for a line that says 'num_ctx' followed by a number. This tells you how many tokens your companion can remember at once."*

### Success Message

**Archivist**: *"Excellent work! Understanding these parameters allows you to fine-tune your companions, create custom variations, and troubleshoot issues. The Show Scroll is invaluable for advanced summoners."*

*A southern passage opens, cold air flowing from within.*

### Educational Note

**Archivist**: *"The Show Scroll teaches you:*
- *Model architecture and template format*
- *Adjustable parameters (temperature, top_k, top_p, etc.)*
- *System prompts that guide behavior*
- *License and usage restrictions*

*When creating custom companions with 'ollama create', you'll write your own Modelfile. Understanding this format is essential for that advanced magic."*

---

## Act V: Purge Chamber

### Scene Opening

```
╔══════════════════════════════════════════════════════════════╗
║                       PURGE CHAMBER                          ║
║                                                              ║
║  A stark, cold room with walls of polished obsidian. In      ║
║  the center lies the Unbinding Circle - where companions     ║
║  are released back to the void. The air feels heavy with     ║
║  the weight of necessary endings.                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Guardian's Warning

**Chamber Guardian**: *"You have reached the final chamber, summoner. Here you will learn a difficult but necessary skill - the art of letting go."*

**Guardian**: *"Companions are powerful, but they consume your realm's resources - memory, storage space, processing power. A wise summoner knows when to release a companion to make room for others."*

### Teaching Moment

**Guardian**: *"The Unbinding Ritual is called 'ollama rm' in the common tongue. It removes a companion completely, freeing all resources they occupied."*

```
ollama rm <companion_name>
```

**Guardian**: *"For your Llama3 companion:"*

```
ollama rm llama3
```

**Guardian**: *"Be certain of your choice - this cannot be undone without resummoning. The companion will be completely unbound from your service."*

### Command Instructions

**Instruction Panel:**
```
┌─────────────────────────────────────────────────────────┐
│ TASK: Release your companion to complete the ritual     │
│                                                         │
│ Execute this command:                                   │
│   $ ollama rm llama3                                    │
│                                                         │
│ This will permanently remove the model from your        │
│ system. You can always re-summon it later with          │
│ 'ollama pull llama3' if needed.                         │
│                                                         │
│ After removal, verify with 'ollama list' to confirm.   │
└─────────────────────────────────────────────────────────┘
```

### Philosophical Moment

**Guardian**: *"Some may wonder - why teach removal in a tutorial about summoning? The answer is simple: true mastery includes knowing when NOT to have something."*

**Guardian**: *"Your system has finite resources. Models can be large - 4GB, 8GB, even 40GB or more. Keeping dozens of models will fill your storage and slow your machine."*

**Guardian**: *"The cycle is this:*
1. *Pull models when you need them*
2. *Use them for their purpose*
3. *Remove them when done to free space*
4. *Pull again when needed - the internet remembers*

*This is the way of the disciplined summoner."*

### Success Message

**Guardian**: *"You have completed the ritual. Your companion has been released cleanly, and your realm's resources are freed. Check with 'ollama list' - Llama3 should no longer appear in your registry."*

**Guardian**: *"You have now mastered all five fundamental incantations:*
- *ollama pull - To summon*
- *ollama list - To survey*  
- *ollama run - To commune*
- *ollama show - To understand*
- *ollama rm - To release*

*With these commands, you can manage any AI companion. The Ground Level is complete!"*

---

## Epilogue

### Victory Chamber

```
╔══════════════════════════════════════════════════════════════╗
║                      VICTORY ACHIEVED!                       ║
║                                                              ║
║  You stand in a chamber filled with golden light. Before     ║
║  you, a pedestal holds a glowing scroll - your Certificate   ║
║  of Ollama Mastery.                                          ║
╚══════════════════════════════════════════════════════════════╝
```

**Master's Voice**: *"Well done, apprentice - or should I say, Master Summoner! You have completed the Ground Level and learned the five sacred incantations."*

### Knowledge Recap

**The Five Commands You've Mastered:**

1. **ollama pull `<model>`** - Summon (download) new companions
2. **ollama list** - Survey all bound companions  
3. **ollama run `<model>` "`<prompt>`"** - Commune with companions
4. **ollama show `<model>`** - Understand companion nature
5. **ollama rm `<model>`** - Release companions responsibly

### Next Steps

**Master's Advice**: *"Your journey with Ollama has only begun. Here are your next steps:*

- *Experiment with different models: mistral, codellama, phi3*
- *Learn about model tags: :7b, :13b, :70b variants*
- *Explore interactive mode: 'ollama run model' without a prompt*
- *Create custom companions: 'ollama create' with Modelfiles*
- *Use the API: Integrate Ollama into your applications*

*The possibilities are endless. Go forth and summon wisely!"*

### Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║              OLLAMA COMMAND QUICK REFERENCE                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ollama pull <model>              Download a model           ║
║  ollama list                      List installed models      ║
║  ollama run <model> "prompt"      Run model with prompt      ║
║  ollama show <model>              Show model details         ║
║  ollama rm <model>                Remove a model             ║
║                                                              ║
║  Examples:                                                   ║
║    ollama pull llama3                                        ║
║    ollama list                                               ║
║    ollama run llama3 "Hello!"                                ║
║    ollama show llama3                                        ║
║    ollama rm llama3                                          ║
║                                                              ║
║  Advanced:                                                   ║
║    ollama run llama3              (interactive mode)         ║
║    ollama pull llama3:70b         (specific version)         ║
║    ollama create mymodel -f ./Modelfile                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Alternative Dialogue Variants

### For Mode B (Paste Verification)

**Guide**: *"I sense you are not yet ready to execute commands directly in this realm. No matter - you can still learn! Execute the command in your own terminal, then paste the results here for verification."*

### For Mode C (Simulated)

**Guide**: *"You observe from afar, learning the incantations by watching. Though you cannot yet execute them yourself, commit them to memory. When you have access to Ollama in your realm, you will be prepared."*

### Encouraging Messages

**For Errors:**
- *"Even master summoners make mistakes. Check your incantation and try again."*
- *"The ritual requires precision. Review the command format carefully."*
- *"Patience! Some summonings take time. Ensure the previous ritual completed fully."*

**For Success:**
- *"Your potential grows! The incantation was perfectly executed."*
- *"The ancient art flows through you naturally. Continue forward!"*
- *"Knowledge gained is knowledge kept. You are becoming a true master."*

### Tips for Different Models

**If using mistral instead of llama3:**
*"Mistral is swift and efficient, specializing in practical tasks. A excellent companion for those who value speed and precision."*

**If using qwen:**
*"Qwen brings wisdom from distant lands, with particular strength in reasoning and coding. A valuable ally for technical challenges."*

**If using phi3:**
*"Phi3 is compact yet capable - perfect for those with limited resources. Never underestimate small companions!"*

---

*End of Script*
