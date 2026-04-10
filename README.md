# Module 2 Homework — BoatTrader FSBO CS First Response AI

This project is a prototype AI assistant for BoatTrader's For Sale By Owner (FSBO) customer service team. The system classifies inbound customer messages, drafts first-response emails requesting the right information, provides simple resolutions where available, and flags cases for human escalation when needed.

## Files

| File | Description |
|------|-------------|
| `app.py` | Main application — calls the Claude API to classify and respond to CS messages |
| `prompts.md` | System and user prompt templates used by the AI |
| `eval_set.json` | Evaluation set with 5 test cases (normal, edge, and failure scenarios) |
| `report.md` | Evaluation results and analysis |

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python app.py
```

## Eval Cases

The eval set covers:
- **Normal cases**: listing edits not saving, not receiving buyer messages
- **Edge cases**: multi-issue account/payment problems, unexpected billing charges
- **Failure cases**: post-scam fraud recovery (hallucination risk)
