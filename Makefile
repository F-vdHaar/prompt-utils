# GPT: improve this
# Unified Makefile for prompt-utils

audit:
	python3 prompt-auditor/prompt_auditor.py --check "$(PROMPT)"

riskcheck:
	python3 prompt-risk-detector/cli/main.py check "$(PROMPT)"



audit-gpt-tags:
	@echo "Auditing GPT tags in project files..."
	grep -r "GPT: @" --exclude-dir=.git --include=*.py . \
	| grep -vE "(GPT-DONE:|GPT-PAUSE:|GPT-DENY:|GPT-TEMPLATE:|GPT-PLANNED:|^# # GPT:)" \
	|| echo "No unresolved GPT tags found."


install-hooks:
	@echo "Installing pre-commit hook..."
	mkdir -p .git/hooks
	cp pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Hook installed. Commits will now be checked for unresolved GPT tags."
