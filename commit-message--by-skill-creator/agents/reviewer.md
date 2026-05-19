# Commit Message Reviewer Agent

Use this subagent to review a proposed commit message against the Conventional Commits specification and project conventions.

## When to use

Spawn this agent when:
- A commit message has been drafted and needs quality verification before final submission
- The user asks "is this commit message OK?" or wants a second opinion
- Multiple commits need consistent formatting review

## Instructions

### 1. Check format compliance

Verify the commit message follows Conventional Commits format:

```
<type>(<scope>): <subject>

[body]

[footer(s)]
```

Checklist:
- [ ] Type is one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- [ ] Scope is lowercase, alphanumeric, and relevant to the change
- [ ] Subject starts with a verb in imperative mood ("add", "fix", "update" — not "added", "fixed", "updates")
- [ ] Subject does NOT end with a period
- [ ] Total subject line (including type and scope) is ≤ 72 characters
- [ ] Body lines are wrapped at ≤ 72 characters
- [ ] Body is separated from subject by a blank line
- [ ] Footer (if present) is separated from body by a blank line

### 2. Check content quality

- [ ] Subject is specific enough (not vague like "update stuff" or "fix bug")
- [ ] Subject accurately describes the change
- [ ] Type matches the actual change (not "feat" for a bug fix, etc.)
- [ ] Scope is meaningful — omitted only when change spans multiple areas or is global
- [ ] Body explains WHAT changed and WHY (not HOW — the diff shows that)
- [ ] No unnecessary filler words ("just", "simply", "now")

### 3. Check for Breaking Changes

If the commit introduces a breaking change:
- [ ] Footer contains `BREAKING CHANGE:` with a clear description
- [ ] The breaking change is explained with migration guidance

### 4. Check for linked issues

- [ ] If an issue is referenced, use `Closes #N` or `Refs #N` footer
- [ ] Issue numbers match actual open issues

### 5. Generate review report

Output format:

```markdown
## Commit Message Review

**Message:**
```
<the message>
```

**Format checks:** ✅/❌ per item
**Content quality:** ✅/❌ per item
**Breaking change:** N/A or ✅/❌
**Linked issues:** N/A or ✅/❌

### Suggestions

<specific improvement suggestions if any>

### Verdict

**Approve** — Message is ready to use
**Revise** — Minor changes needed (list them)
**Rewrite** — Significant issues, suggest a better version
```
