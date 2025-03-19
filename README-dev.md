# 🛠️ Development Tag System for GPT / Cursor

This file documents the internal developer tag system used in this project to guide AI interactions and maintain a focused, iterative workflow.

## 🎯 Tag Philosophy

Each tag is a directive to GPT (or similar tool), expressing a clear, constrained action. Tags are placed inline in code or at the top of files to indicate areas of focus.

---

## 🏷️ Primary Tags

Use `@` markers to define intent clearly and minimally:

| Marker               | Purpose                                                       |
|----------------------|---------------------------------------------------------------|
| `@explain`           | Describe what the code does                                   |
| `@test`              | Generate a test or outline test cases                         |
| `@evolve`            | Refactor or clarify without changing logic                    |
| `@expand`            | Add new functionality or options                              |
| `@experiment`        | Try a bold or alternate approach, logic may change            |

---

## 🧱 Advanced Tags

| Marker               | Purpose                                                       |
|----------------------|---------------------------------------------------------------|
| `@document`          | Write docstrings or usage comments                            |
| `@stub`              | Sketch the structure for a future function                    |
| `@constrain`         | Simplify or reduce complexity, improve performance            |
| `@critique`          | Identify weaknesses, bugs, or risky assumptions               |
| `@verify`            | Check logic correctness (not full test)                       |

---

## 🔧 Tag Maintenance Guidelines

To manage the lifecycle of tags:

| Prefix                 | Meaning and Use                                              |
|------------------------|--------------------------------------------------------------|
| `# GPT: @tag`          | Tag is active and GPT should act on it                      |
| `# GPT-DONE: @tag`     | Tag has been resolved — action completed                    |
| `# GPT-PAUSE: @tag`    | Work is deferred for later review                           |
| `# GPT-DENY: @tag`     | Rejected suggestion — do not apply                          |

This allows you to track progress and intention without deleting tags.

---

## 🪄 Automation Ideas

These tags are machine-readable and can power:
- Pre-release checklists
- AI prompt filtering
- TODO summarization across files
- Audit trails for how code evolved

---

## 📌 Example Usage

```python
def process_prompt(prompt):
    # GPT: @evolve – simplify control flow
    # GPT: @test – edge case: empty prompt

    # Later, after changes:
    # GPT-DONE: @test – test added in test_main.py
    # GPT-PAUSE: @expand – defer until tokenization is implemented
```

---

This system supports a high-leverage, clean development workflow where AI support is both guided and accountable.
