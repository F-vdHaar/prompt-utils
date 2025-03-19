""" # GPT: What’s the next step for this project? What structure is missing?
 """# GPT: @explain
# GPT: @expand
# GPT: @test

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

def main():
    parser = argparse.ArgumentParser(description="Audit a prompt for risk patterns.")
    parser.add_argument("--check", type=str, help="Prompt to audit")
    args = parser.parse_args()

    if args.check:
        print(f"Auditing: {args.check}")
        # TODO: Add actual checks

if __name__ == "__main__":
    main()
