# 🛡️ prompt-utils

A lightweight, CLI-based suite to make AI prompting safer, more predictable, and easier to debug.

## Tools Included

### 1. [`prompt-auditor`](./prompt-auditor)

**Pre-execution static analysis.**  
Audits prompt templates for token usage, unused variables, and risky patterns **before** sending to an LLM.

> Think: _"Is this prompt well-formed and safe to run?"_

### 2. [`prompt-risk-detector`](./prompt-risk-detector)

**Post-execution behavioral logging.**  
Records and scores past prompts by outcome (e.g. revert, success), preventing reuse of known-bad inputs.

> Think: _"Has this prompt ever broken things before?"_

---

## Suggested Workflow

1. **Audit** your prompt statically:
   ```bash
   make audit PROMPT="Rewrite using map instead of loop"
   ```

2. **Check** its trust score based on past behavior:
   ```bash
   make riskcheck PROMPT="Rewrite using map instead of loop"
   ```

3. **Decide**: override, edit, or trust.


