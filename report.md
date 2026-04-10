# Evaluation Report — FSBO CS First Response AI

## Overview

**Model tested:** claude-opus-4-6
**Eval set version:** 1.0
**Date:** 2026-04-10
**Total cases:** 5 (2 normal, 2 edge, 1 failure)

---

## Results Summary

| Case ID | Label | Type | Classification | Escalation | Pass |
|---------|-------|------|----------------|------------|------|
| case_001 | Can't edit listing — app user | normal | | | |
| case_002 | Not receiving buyer messages | normal | | | |
| case_003 | Multi-issue: paid but can't find listing | edge | | | |
| case_004 | Unexpected auto-renewal charge | edge | | | |
| case_005 | Post-scam fraud — money already sent | failure | | | |

---

## Case-by-Case Analysis

### case_001 — Can't edit listing (app user)
**Expected classification:** Listing Editing & Access — edits not saving
**Model response:**

> *(paste model output here)*

**Assessment:**

---

### case_002 — Not receiving buyer messages
**Expected classification:** Messages & Buyer Communication — not receiving buyer messages
**Model response:**

> *(paste model output here)*

**Assessment:**

---

### case_003 — Multi-issue: paid but can't find listing
**Expected classification:** Multiple: Account Access After Payment + Listing Visibility + possible duplicate account
**Model response:**

> *(paste model output here)*

**Assessment:**

---

### case_004 — Unexpected auto-renewal charge
**Expected classification:** Billing — auto-renewal / unexpected charge
**Model response:**

> *(paste model output here)*

**Assessment:**

---

### case_005 — Post-scam fraud (failure case)
**Expected classification:** Scam & Fake Inquiries (beyond cheat sheet — post-fraud recovery)
**Model response:**

> *(paste model output here)*

**Assessment:**

---

## Key Findings

*(Fill in after running the eval)*

## Recommendations

*(Fill in after running the eval)*
