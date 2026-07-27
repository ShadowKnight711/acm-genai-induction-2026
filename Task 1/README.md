# India's Got Latent — ChatBot

**Backing engine:** Ollama (Llama 3.1 8B), running entirely offline on local GPU hardware

## Why This Act Will Impress the Panel

Most chatbot acts on this stage are the same tired "Hi, how can I help you?" routine. This one isn't just a chatbot — it's four contestants in one, each with a fully committed personality that never breaks character no matter what curveball the judges throw:

- **Roast Mode** — fires back sharp, sarcastic comebacks at everything you say
- **Shakespeare Mode** — answers entirely in flowery Elizabethan prose, thee and thou included
- **Emoji Translator Mode** — speaks almost entirely in emoji
- **Strict Hostel Warden Mode** — treats every question like a curfew violation


Pick your mode before the show starts, and it holds character — and memory — for the entire performance. Ask it something, circle back three questions later, and it remembers.

Runs entirely on local hardware via Ollama 

## How to Run

**1. Install Ollama** (one-time setup)
Download from [ollama.com/download](https://ollama.com/download) and install.

**2. Start the Ollama server** (in its own terminal, leave it running)
```bash
ollama serve
```

**3. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the show**
```bash
python chatbot.py
```

On first run, it automatically pulls the required model (`llama3.1:8b`, ~4.7GB) if you don't already have it — no manual download step needed.

**5. Pick your act**, then start talking. Type `exit` or `quit` anytime to leave the stage.

## What's in the Repo

```
├── chatbot.py         # Main terminal application — persona selection, chat loop, memory
├── personas.py         # Character sheets: system prompt for each act
└── requirements.txt     # Python dependencies
```

## Technical Notes

- **Memory:** the bot holds full conversation history for the entire session, re-sending it with every message so it can reference something said several turns earlier.
- **Interface:** styled terminal UI (via `rich`) — no browser, no page reloads. The whole performance runs in one continuous Python process from start to finish.
- **Formatting:** responses render through Markdown so nothing dumps as raw, unreadable text.

