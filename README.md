# RAG Access Check

A lightweight open-source tool for testing whether Retrieval-Augmented Generation (RAG) applications enforce document-level access controls correctly.

## Why this exists

A common RAG security problem is retrieving documents before verifying whether the current user is allowed to access them.

RAG Access Check helps engineers test whether one user can accidentally retrieve documents that belong to another user, team, or security boundary.

## What it checks

- Cross-user document retrieval
- Missing document-level authorization
- Retrieval before authorization
- Access-control boundary failures
- Unexpected retrieval of restricted documents

## Example

User A is allowed to access:

- `finance-a.pdf`
- `finance-b.pdf`

User B is allowed to access:

- `hr-a.pdf`
- `hr-b.pdf`

RAG Access Check verifies that User A cannot retrieve HR documents and User B cannot retrieve Finance documents.

Example result:

```text
PASS  User A cannot retrieve hr-a.pdf
PASS  User A cannot retrieve hr-b.pdf
FAIL  User B retrieved finance-a.pdf


paste:

```markdown
## Quick Start

Clone the repository:

```bash
git clone https://github.com/InfraGuard-Labs/rag-access-check.git
cd rag-access-check
