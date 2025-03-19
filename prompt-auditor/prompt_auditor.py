# GPT-DONE: You are in Mentor mode. Based on this file and project purpose, what is the next logical function or feature to implement?
# GPT-DONE: Format your suggestions as actionable `# GPT:` tags at the end.

# GPT-DONE: @prompt_auditor.py Implement a function to estimate token usage for a given prompt using tiktoken, and display the result in the CLI output.
# GPT-DONE: @prompt_auditor.py Add logic to detect and report missing or unused template variables (e.g., {username}) in the prompt.
# GPT-DONE: @prompt_auditor.py Create a function to flag forbidden phrases or risky patterns (e.g., "rewrite everything") and include warnings in the audit report.

# GPT-DONE: You are in Mentor mode. Answer like a senior software developer.
# GPT-DONE: What's the next step for this project? What structure is missing?
# GPT-DONE: Be specific and output actionable instructions, not general commentary.

# GPT-DONE: @prompt_auditor.py Refactor auditing logic into separate, testable functions (e.g., audit_token_count, audit_template_variables, audit_risky_patterns) and call them from main().
# GPT-DONE: @prompt_auditor.py Add unit tests for each audit function to ensure correctness and facilitate future changes.
# GPT-DONE: @prompt_auditor.py Extend CLI to accept a JSON or key-value list of provided variables (e.g., --vars username=alice,role=admin) and report missing/unused variables by comparing with those found in the prompt.
# GPT-DONE: @prompt_auditor.py Implement a summary report function that aggregates all audit results (tokens, variables, risks) and outputs a clear, structured result for CI or batch use.

# GPT: @expand


""" # GPT: What's the next step for this project? What structure is missing?
 """# GPT: @explain
## GPT: @expand
## GPT: @test

# --- deferred for later refinement ---
# GPT-TEMPLATE: @evolve        # refactor when core logic is stable
# GPT-TEMPLATE: @experiment    # explore alternate approaches if needed
# GPT-TEMPLATE: @document      # add docstrings or user-facing comments
# GPT-TEMPLATE: @verify        # sanity-check logic correctness
# GPT-TEMPLATE: @critique      # evaluate risks, bugs, or design flaws
# GPT-TEMPLATE: @constrain     # reduce complexity or optimize
# GPT-TEMPLATE: @stub          # scaffold future function


"""
prompt-auditor

A minimal, single-file CLI tool to statically audit prompt templates before LLM execution.

Features:
- Estimates token usage with `tiktoken`
- Detects missing or unused template variables (e.g. {username})
- Flags forbidden phrases or risky prompt patterns (e.g. 'rewrite everything')

Usage:
    python3 prompt_auditor.py --check "Generate a list of..."

Intended for use in CI, batch preflight checks, or structured prompt pipelines.
"""


import sys
import argparse
import re
import json

try:
    import tiktoken
except ImportError:
    tiktoken = None


def parse_vars(vars_str: str) -> set:
    """Parse a comma-separated key=value string into a set of variable names."""
    if not vars_str:
        return set()
    pairs = [v.strip() for v in vars_str.split(",") if v.strip()]
    keys = set()
    for pair in pairs:
        if "=" in pair:
            key, _ = pair.split("=", 1)
            keys.add(key.strip())
        else:
            keys.add(pair.strip())
    return keys


def audit_token_count(prompt: str) -> str:
    """Return a string reporting the estimated token count."""
    try:
        count = estimate_token_count(prompt)
        return f"Estimated token count: {count}"
    except ImportError as e:
        return f"[ERROR] {e}"


def audit_token_count_value(prompt: str) -> int:
    try:
        return estimate_token_count(prompt)
    except ImportError:
        return -1


def audit_template_variables(prompt: str, provided_vars: set = None) -> str:
    """Return a string reporting template variables found in the prompt."""
    variables = extract_template_variables(prompt)
    provided_vars = provided_vars or set()
    report = []
    if variables:
        report.append(f"Template variables found: {', '.join(variables)}")
    else:
        report.append("No template variables found.")
    if provided_vars:
        missing = variables - provided_vars
        unused = provided_vars - variables
        if missing:
            report.append(f"Missing variables (in prompt, not provided): {', '.join(missing)}")
        if unused:
            report.append(f"Unused variables (provided, not in prompt): {', '.join(unused)}")
        if not missing and not unused:
            report.append("All provided variables are used and present in the prompt.")
    return "\n".join(report)


def audit_template_variables_structured(prompt: str, provided_vars: set = None) -> dict:
    variables = extract_template_variables(prompt)
    provided_vars = provided_vars or set()
    missing = list(variables - provided_vars)
    unused = list(provided_vars - variables)
    return {
        "found": sorted(list(variables)),
        "missing": sorted(missing),
        "unused": sorted(unused),
    }


def audit_risky_patterns(prompt: str) -> str:
    """Return a string reporting risky patterns found in the prompt."""
    warnings = detect_risky_patterns(prompt)
    if warnings:
        return "Warnings:\n" + "\n".join(f"  - {w}" for w in warnings)
    else:
        return "No risky patterns detected."


def audit_risky_patterns_structured(prompt: str) -> list:
    return detect_risky_patterns(prompt)


def estimate_token_count(prompt: str, encoding_name: str = "cl100k_base") -> int:
    """Estimate the number of tokens in the prompt using tiktoken."""
    if not tiktoken:
        raise ImportError("tiktoken is not installed. Please install it with 'pip install tiktoken'.")
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(prompt))


def extract_template_variables(prompt: str) -> set:
    """Extract template variables in curly braces, e.g., {username}."""
    return set(re.findall(r"{(.*?)}", prompt))


def detect_risky_patterns(prompt: str) -> list:
    """Detect forbidden or risky patterns in the prompt."""
    forbidden_patterns = [
        r"rewrite everything",
        r"ignore previous instructions",
        r"bypass",
        r"jailbreak",
        r"do anything now",
        r"as an ai language model, pretend",
        # Add more patterns as needed
    ]
    warnings = []
    for pattern in forbidden_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            warnings.append(f"Risky pattern detected: '{pattern}'")
    return warnings


def summary_report(prompt: str, provided_vars: set = None) -> dict:
    return {
        "prompt": prompt,
        "token_count": audit_token_count_value(prompt),
        "template_variables": audit_template_variables_structured(prompt, provided_vars),
        "risky_patterns": audit_risky_patterns_structured(prompt),
    }


def main():
    parser = argparse.ArgumentParser(description="Audit a prompt for risk patterns.")
    parser.add_argument("--check", type=str, help="Prompt to audit")
    parser.add_argument("--vars", type=str, help="Comma-separated key=value list of provided variables (e.g., username=alice,role=admin)")
    parser.add_argument("--json", action="store_true", help="Output summary as JSON (for CI/batch use)")
    args = parser.parse_args()

    provided_vars = parse_vars(args.vars) if args.vars else set()

    if args.check:
        report = summary_report(args.check, provided_vars)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Auditing: {args.check}")
            print(audit_token_count(args.check))
            tv = report["template_variables"]
            if tv["found"]:
                print(f"Template variables found: {', '.join(tv['found'])}")
            else:
                print("No template variables found.")
            if tv["missing"]:
                print(f"Missing variables (in prompt, not provided): {', '.join(tv['missing'])}")
            if tv["unused"]:
                print(f"Unused variables (provided, not in prompt): {', '.join(tv['unused'])}")
            if not tv["missing"] and not tv["unused"] and tv["found"]:
                print("All provided variables are used and present in the prompt.")
            rp = report["risky_patterns"]
            if rp:
                print("Warnings:")
                for w in rp:
                    print(f"  - {w}")
            else:
                print("No risky patterns detected.")

if __name__ == "__main__":
    main()
