import anthropic
import json
import re

# Load prompts
with open("prompts.md", "r") as f:
    prompts_content = f.read()

# Extract system prompt (between first ```...``` block)
system_match = re.search(r"## System Prompt\s+```\n(.*?)```", prompts_content, re.DOTALL)
SYSTEM_PROMPT = system_match.group(1).strip() if system_match else ""

# Extract user prompt template
user_match = re.search(r"## User Prompt Template\s+```\n(.*?)```", prompts_content, re.DOTALL)
USER_PROMPT_TEMPLATE = user_match.group(1).strip() if user_match else ""

client = anthropic.Anthropic()


def run_case(case: dict) -> dict:
    customer_message = case["customer_message"]
    user_prompt = USER_PROMPT_TEMPLATE.replace("{customer_message}", customer_message)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = message.content[0].text

    return {
        "id": case["id"],
        "label": case["label"],
        "case_type": case["case_type"],
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


if __name__ == "__main__":
    results = run_eval()

    print("\n" + "=" * 60)
    print("EVAL RESULTS")
    print("=" * 60)
    for r in results:
        print(f"\n--- {r['id']}: {r['label']} ({r['case_type']}) ---")
        print(r["model_response"])
        print()
