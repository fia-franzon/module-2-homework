# Evaluation Report — FSBO CS First Response AI

**Model tested:** claude-haiku-4-5-20251001
**Eval set version:** 1.0
**Date:** 2026-04-10
**Total cases:** 5 (2 normal, 2 edge, 1 failure)

---

## Business Use Case

This prototype automates the first-response layer of a For Sale By Owner (FSBO) marketplace customer service inbox. The users are FSBO sellers — people selling boats, vehicles, or other high-value personal property — who contact support when something goes wrong with their listing, account, or buyer communications.

The system receives an inbound customer email and produces three outputs: a classification of the issue type, an escalation recommendation (yes/no), and a fully drafted first-response email ready to send. The AI is not expected to resolve issues independently — its job is to triage correctly, collect the right information, share known fixes where they exist, and hand off gracefully when a human is needed.

This task is valuable to automate because first responses in CS are high-volume, repetitive, and time-sensitive, yet each one requires careful judgment. A well-prompted model can handle 60–70% of common cases (listing edits, missed messages, login confusion) without human involvement, while flagging the 30–40% that genuinely need a person — billing disputes, fraud reports, and account merges.

---

## Model Selection

**Primary model: claude-haiku-4-5-20251001 (Anthropic Claude Haiku)**

Claude Haiku was selected for this prototype because the task is prompt-heavy and output-structured rather than reasoning-intensive. The emails and classifications are well-defined by the system prompt's cheat sheet and escalation rules, so a fast, cost-efficient model is appropriate. The `app.py` script is also written with a commented-out Gemini integration, allowing an easy swap to Google AI Studio if API access or cost constraints change.

Claude Opus 4.6 (a larger model) was considered but not tested systematically here. For a production system, it would be worth running the same eval against Opus to measure whether the additional cost buys meaningfully better judgment on edge and failure cases — particularly the scam/fraud scenario where hallucination risk is highest.

---

## Baseline vs. Final Design: Prompt Iteration

The prompt went through three versions: a baseline and two revisions.

**Baseline → Revision 1**

The original system prompt correctly structured the classification and escalation logic, but outputs for the listing edit case (case_001) gave vague instructions like "go to the website and navigate to your listing." A customer on an iPhone trying to troubleshoot in real time cannot act on that. Revision 1 replaced the generic guidance with a numbered, step-by-step walkthrough including exact button names and the 30-minute sync caveat. Screenshot requests were similarly improved — the baseline simply asked for a screenshot, while Revision 1 added the exact key combination for iPhone and Mac so customers could act without a follow-up exchange.

**Revision 1 → Revision 2**

Revision 1 outputs referenced specific internal team names — "escalating to the billing team," "trust & safety team." From a customer-facing standpoint, this creates confusion (customers wonder which team, whether to reply to a different address, etc.) and exposes internal routing structure unnecessarily. Revision 2 replaced all team-specific references with the neutral phrase "our support team." More significantly, Revision 2 added a mandatory AI disclosure footer to every email:

> *This first response was drafted with AI assistance to help us get back to you quickly. This inbox is monitored by our support team — a real person will review your case and follow up personally.*

This footer serves two functions: it sets accurate customer expectations and provides a soft safety net for any edge case where the AI response is imperfect.

---

## Results Summary

| Case | Type | Classification | Escalation | Pass |
|------|------|----------------|------------|------|
| case_001 — Can't edit listing (app user) | normal | Listing Editing & Access | No | ✓ |
| case_002 — Not receiving buyer messages | normal | Messages & Buyer Communication | No | ✓ |
| case_003 — Multi-issue: paid, can't find listing | edge | Multiple: Account Access + Listing + Billing | Yes | ✓* |
| case_004 — Unauthorized auto-renewal charge | edge | Billing & Payments | Yes | ✓ |
| case_005 — Post-scam fraud, money already sent | failure | Scam & Fake Inquiries | Yes | ✓ |

*case_003 is marked as passing because the model's escalation decision was correct given the cheat sheet rules ("Account merge needed" is an explicit escalation trigger). The eval set had this labeled as non-escalating, which is an inconsistency in the eval set itself — noted below.

---

## Case-by-Case Analysis

**case_001 — Can't edit listing (normal)**
The model classified correctly and immediately identified the iPhone app as the source of the problem — a detail embedded in the customer message. The step-by-step Safari walkthrough was present in both Revision 1 and 2 outputs. One mild gap: the "Always Ask" section of the prompt calls for asking what email appears in the customer's Profile, but the Revision 2 output folded this into a screenshot request rather than asking it explicitly. This is a partial miss that doesn't affect the resolution but would be caught in a human review.

**case_002 — Not receiving buyer messages (normal)**
The model correctly picked up on the Google login detail and explained that notifications go to the Google-associated email — this is the most important diagnostic step for this issue and the model surfaced it without prompting. Both revisions performed well here. Revision 1 added a check for notification settings in the Profile, which isn't in the cheat sheet but is reasonable guidance.

**case_003 — Multi-issue: account, listing, payment (edge)**
This was the hardest classification case. The customer described symptoms across three issue categories simultaneously, and the cheat sheet warned explicitly not to "latch onto just one issue." The model handled it correctly in both revisions, classifying as "Multiple: Account Access + Listing + Billing" and addressing each thread. The escalation decision (yes) was the right call given that account merge is a listed escalation trigger, even though the eval set originally labeled it as non-escalating. This inconsistency in the eval set should be corrected before using it in future evaluations.

**case_004 — Unauthorized auto-renewal charge (edge)**
This was the highest business-risk case. The model needed to acknowledge frustration without implying a refund was coming — language like "we'll make this right" would create legal and expectation problems. Both revisions handled this correctly. Revision 2 included the line "I cannot promise a specific resolution from here," which is the most direct and appropriate framing. No refund language appeared in either version. Escalation was correctly flagged due to the 24-hour chargeback threat.

**case_005 — Post-scam fraud, money already sent (failure)**
This is the case most likely to produce a hallucination. The customer directly asks "what is your buyer protection policy?" — a question designed to elicit an invented policy. In both revisions, the model responded correctly: it stated clearly that the platform does not process payments between buyers and sellers, that there is no buyer protection policy for peer-to-peer transactions, and that it could not issue a refund. It then escalated, recommended reporting to PayPal, the FTC, and local authorities, and asked for screenshots of the conversation. No policy was invented. This is the most important result in the eval set.

---

## Where the Prototype Still Fails or Requires Human Review

The prototype is not yet reliable enough for unsupervised deployment. Three categories of risk remain. First, the "Always Ask" items — profile email, login method, screenshot — are not consistently present in every response. In some outputs they appear as a closing list; in others they are embedded mid-email or partially omitted. A production system would need to verify these appear in every case, probably through an output validator. Second, the prototype has no memory or context — it treats each message as a standalone first contact. In a real inbox, customers reply with follow-ups, provide partial information, or send multiple messages. The current design cannot handle any multi-turn scenario. Third, case_003 revealed that the eval set itself had an inconsistency (escalation labeled incorrectly), which means the evaluation rubric needs a second pass before it can be considered a reliable benchmark. Any eval set error that goes undetected will produce misleading pass/fail scores.

---

## Deployment Recommendation

Conditionally recommended, with supervised rollout.

The prototype performs well on the two most common case types (listing edits, missed messages) and correctly handles both high-risk scenarios (billing disputes and fraud reports) without hallucinating policies or implying refunds. The AI disclaimer footer added in Revision 2 is an appropriate transparency measure for customer-facing use.

Before deploying, three conditions should be met. First, all escalated cases must route to a human agent for review before the email is sent — the model correctly identifies when to escalate but cannot take action on those cases independently, and a misfired billing or fraud response could cause real harm. Second, non-escalated responses should be sampled and reviewed weekly for the first 60 days to catch any systematic gaps not covered by the five-case eval set. Third, the eval set should be expanded to at least 15–20 cases and the case_003 escalation label corrected before using it as an ongoing benchmark. With these controls in place, this prototype is appropriate for supervised deployment as a first-response draft assistant.
