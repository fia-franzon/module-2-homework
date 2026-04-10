import anthropic
# import google.generativeai as genai  # uncomment to use Gemini
# import os                             # uncomment to use Gemini
import csv
import json
import re

# Load prompts
with open("prompts_revision_2.md", "r") as f:
    prompts_content = f.read()

# Extract system prompt (between first ```...``` block)
system_match = re.search(r"## System Prompt\s+```\n(.*?)```", prompts_content, re.DOTALL)
SYSTEM_PROMPT = system_match.group(1).strip() if system_match else ""

# Extract user prompt template
user_match = re.search(r"## User Prompt Template\s+```\n(.*?)```", prompts_content, re.DOTALL)
USER_PROMPT_TEMPLATE = user_match.group(1).strip() if user_match else ""

# ── PROVIDER: Anthropic Claude (active) ──────────────────────
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

# ── PROVIDER: Google Gemini (swap in if needed) ───────────────
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# gemini_model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)


def run_case(case: dict) -> dict:
    customer_message = case["customer_message"]
    user_prompt = USER_PROMPT_TEMPLATE.replace("{customer_message}", customer_message)

    # ── Anthropic call (active) ───────────────────────────────
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    response_text = message.content[0].text

    # ── Gemini call (swap in if needed) ──────────────────────
    # message = gemini_model.generate_content(user_prompt)
    # response_text = message.text

    return {
        "id": case["id"],
        "label": case["label"],
        "case_type": case["case_type"],
        "customer_message": customer_message,
        "model_response": response_text,
        "expected": case["expected_behavior"],
    }


def run_eval():
    with open("eval_set.json", "r") as f:
        eval_data = json.load(f)

    cases = eval_data["cases"]
    results = []

    print(f"Running {len(cases)} eval cases...\n")
    for case in cases:
        print(f"[{case['id']}] {case['label']}")
        result = run_case(case)
        results.append(result)
        print(f"  -> done\n")

    return results


def save_csv(results: list, path: str = "eval_results.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Label", "Customer Message", "AI Response", "Expected Escalation", "Notes"])
        for r in results:
            writer.writerow([
                r["id"],
                r["case_type"],
                r["label"],
                r["customer_message"],
                r["model_response"],
                r["expected"]["escalate"],
                r["expected"].get("notes", ""),
            ])
    print(f"\nSaved to {path}")


if __name__ == "__main__":
    results = run_eval()
    save_csv(results, "eval_results_revision_2.csv")
