# GitHub Discussions Guide

Use GitHub Discussions for questions, proposed audits, reproduced checks, failed checks, counterexamples, and integration ideas for the WCT symbolic-audit layer.

## Recommended categories

- **Announcements**: Releases, schema changes, canonical audit changes, and maintainer notices.
- **General**: Broad discussion about symbolic validation and repository direction.
- **Q&A**: Focused questions with a minimal SymPy expression, assumptions, environment, and expected result.
- **Ideas**: New audits or invariants with explicit machine-evaluable verdicts and positive and negative fixtures.
- **Show and tell**: Reproductions, discrepancies, independent implementations, mutation tests, and new audit artifacts.

## Interpretation rule

A symbolic PASS means that the encoded relation satisfies the declared symbolic gate under the declared domains and assumptions. It does not prove that the assumptions are physically correct, that a derivation is complete, or that WCT is empirically validated.

A strong discussion identifies:

- the exact claim, equation, function, or test;
- symbol domains, units, positivity and nonzero assumptions;
- the repository commit and dependency versions;
- a minimal executable example;
- PASS, FAIL, or INCOMPLETE criteria;
- positive and negative fixtures;
- the reduced expression, residual, or exception;
- machine-readable output and provenance;
- the narrow consequence for upstream and downstream claims.

Use issues for scoped implementation work and defects. Keep questions about meaning, assumptions, audit design, and research implications in Discussions.
