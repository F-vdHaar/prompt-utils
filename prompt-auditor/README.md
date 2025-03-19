# 🧠 Project: prompt-auditor

A single-file CLI tool to audit prompt templates for token cost, variable usage, and forbidden content—**before** LLM execution.

👉 Part of the [`prompt-utils`](../) suite.

## Features

- Estimates token usage with `tiktoken`
- Detects missing or unused template variables (e.g. {username})
- Flags forbidden phrases or risky prompt patterns (e.g. 'rewrite everything')
- Compares provided variables to those in the prompt and reports missing/unused ones
- Outputs a summary report (human-readable or JSON)
- Returns an audit score via exit code for CI/batch use

## Audit Score Table

| Score | Meaning | Description |
|-------|---------|-------------|
| 0     | Pass    | No issues: all variables provided and used, no risky patterns |
| 1     | Warn    | Unused variables provided, but no missing variables or risky patterns |
| 2     | Fail    | Missing variables or risky patterns detected |

## CLI Usage Example

### Example: Audit a Prompt with Variables and Risky Pattern

```bash
python3 prompt_auditor.py --check "Rewrite everything for {user}" --vars user=alice,role=admin
```

**Expected output:**
```
Auditing: Rewrite everything for {user}
Estimated token count: 6
Template variables found: user
Missing variables (in prompt, not provided):
Unused variables (provided, not in prompt): role
Warnings:
  - Risky pattern detected: 'rewrite everything'
Audit score: 2 (0=pass, 1=warn, 2=fail)
```

### Example: JSON Output for CI

```bash
python3 prompt_auditor.py --check "Rewrite everything for {user}" --vars user=alice,role=admin --json
```

**Expected output:**
```json
{
  "prompt": "Rewrite everything for {user}",
  "token_count": 6,
  "template_variables": {
    "found": ["user"],
    "missing": [],
    "unused": ["role"]
  },
  "risky_patterns": [
    "Risky pattern detected: 'rewrite everything'"
  ],
  "score": 2
}
```

**Exit code meanings:**
- `0`: Pass (prompt is well-formed, no issues)
- `1`: Warn (prompt has unused variables)
- `2`: Fail (prompt has missing variables or risky patterns)

## Intended Use

- Run as a preflight check in CI, batch jobs, or structured prompt pipelines.
- Prevents risky or malformed prompts from reaching production LLMs.
