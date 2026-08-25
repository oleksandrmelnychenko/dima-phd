---
name: dissertation-memory
description: Maintain the repository's dissertation writing memory during drafting, rewriting, author approval, and reviewer-feedback processing. Use whenever dissertation prose is proposed, reviewed, accepted, rejected, or corrected so decisions remain consistent across chats.
---

# Dissertation Memory

Keep `memory/MEMORY.md` as the durable, reviewable record of dissertation-writing decisions across chats. Follow `memory/README.md` for status meanings, precedence, and record format.

This skill complements `$doctoral-dissertation`; it does not replace its scientific, evidence, structure, or language rules.

## At the start of relevant work

1. Read `memory/README.md` completely.
2. Read `memory/MEMORY.md` completely.
3. Identify only the approved, avoid, and applicable contextual rules relevant to the current fragment.
4. Treat `Очікує рішення` entries as review questions, not binding rules.
5. Read the target fragment with its complete preceding and following paragraphs; read the containing subsection when the change is substantive.

## Independent memory audit

For substantive dissertation drafting, rewriting, or review, use a read-only subagent named `memory_auditor` when subagents are available. Give it the target text, local context, proposed revision, and relevant evidence anchors. The subagent must compare the work with memory and return findings; it must not edit files.

The main agent remains the sole writer and decides how to synthesize the audit. Do not delegate simultaneous writes to `MEMORY.md`.

## Automatic tracking workflow

### New draft or proposed rewrite

1. Check the proposal against approved memory rules.
2. Distinguish a local correction from a reusable writing rule.
3. If the work produces a new, non-duplicate lesson, add one `MEM-REVIEW-YYYY-MM-DD-NNN` entry with status `Очікує рішення` before ending the task.
4. Record what is correct as well as what is deficient.
5. Preserve reviewer or agent provenance and the exact scope of the proposed rule.
6. Do not modify the dissertation file until the author explicitly approves the wording.

### Reviewer feedback

Add the feedback as `Очікує рішення` even when the reviewer presents it as mandatory. Record:

- the reviewed location;
- what the reviewer accepted;
- what the reviewer criticized;
- the evidence or rationale;
- the proposed correction;
- whether it conflicts with an approved rule or verified project fact;
- the author's decision, when later supplied.

Do not generalize one reviewer's stylistic preference into a manuscript-wide rule without author approval and a defensible scope.

### Author decision

Interpret explicit decisions such as “погоджено”, “ок”, “внось”, “не приймаю”, or an unambiguous equivalent in their local context.

- If accepted, update the matching pending record with the decision and date. Promote a reusable rule to the active profile only when the decision supports that generalization.
- If rejected, retain the record, document the rejection, and prevent the same rejected proposal from being reintroduced without new evidence.
- If partly accepted, split or narrow the rule instead of marking the entire record approved.
- Apply the approved dissertation edit only when the author has also authorized the file change.

## Record discipline

- Store and report repository paths relative to the repository root; never persist machine-specific absolute paths.
- Search existing IDs and rules before adding a record.
- Use the next unused daily sequence number.
- Link repeated cases to an existing rule instead of duplicating it.
- Never fabricate reviewer identity, evidence, dates, citations, or approval.
- Never silently change `Очікує рішення` to an approved status.
- Preserve replaced rules with status `Замінено` and a link to the superseding record.
- Keep raw drafting history out of the dissertation body; it belongs only in memory.

After changing memory, run:

```powershell
python .agents/skills/dissertation-memory/scripts/validate_memory.py --root .
```

If validation warns that a pending record points to an already modified manuscript file, report the mismatch and ask the author whether that working-tree change is approved. Do not infer approval or revert the file.

Report which memory records were added or changed and whether dissertation files were modified.
