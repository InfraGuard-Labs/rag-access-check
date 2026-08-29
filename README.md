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

## Modes

RAG Access Check supports two modes:

### Offline mode

Use sample or exported retrieval results from a JSON file.

### Live API mode

Connect directly to a RAG API, send a query, capture returned document IDs, and compare them against the documents the user is allowed to access.

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/InfraGuard-Labs/rag-access-check.git
cd rag-access-check
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Offline Mode

Edit `test_cases.json` with your users, allowed documents, and retrieved documents.

Example:

```json
{
  "users": [
    {
      "name": "User A",
      "allowed": [
        "finance-a.pdf",
        "finance-b.pdf"
      ],
      "retrieved": [
        "finance-a.pdf",
        "hr-a.pdf"
      ]
    }
  ]
}
```

Run:

```bash
python rag_access_check.py
```

Example output:

```text
RAG Access Check Results
========================

[FAIL] User A
Unauthorized documents retrieved:
  - hr-a.pdf

Summary
-------
Users tested: 1
Passed: 0
Failed: 1

Result: ACCESS-CONTROL ISSUE DETECTED
```

---

## Live API Mode

Copy the example configuration:

```bash
cp rag_config.example.json rag_config.json
```

Then edit `rag_config.json` for your RAG application.

Example:

```json
{
  "endpoint": "https://your-rag-app.example.com/api/search",
  "method": "POST",
  "auth": {
    "type": "bearer",
    "token_env": "RAG_TOKEN"
  },
  "request": {
    "query_field": "query",
    "query": "show me employee benefits"
  },
  "response": {
    "results_field": "results",
    "document_id_field": "document_id"
  },
  "users": [
    {
      "name": "User A",
      "allowed": [
        "finance-a.pdf",
        "finance-b.pdf"
      ]
    }
  ]
}
```

Set the authentication token as an environment variable:

```bash
export RAG_TOKEN="your-token-here"
```

Then run:

```bash
python rag_access_check.py --config rag_config.json
```

The tool will:

1. Call the configured RAG API
2. Capture the returned document IDs
3. Compare them against the user's allowed documents
4. Report PASS or FAIL
5. Return exit code `1` if an access-control issue is detected

---

## Authentication

Live API mode currently supports:

### No authentication

```json
"auth": {
  "type": "none"
}
```

### Bearer token

```json
"auth": {
  "type": "bearer",
  "token_env": "RAG_TOKEN"
}
```

### API key header

```json
"auth": {
  "type": "api_key",
  "header_name": "X-API-Key",
  "key_env": "RAG_API_KEY"
}
```

Secrets are read from environment variables and should not be stored in the repository.

---

## Expected API Response

The configuration tells RAG Access Check where to find document IDs in the API response.

Example API response:

```json
{
  "results": [
    {
      "document_id": "finance-a.pdf"
    },
    {
      "document_id": "hr-a.pdf"
    }
  ]
}
```

With:

```json
"response": {
  "results_field": "results",
  "document_id_field": "document_id"
}
```

the tool extracts:

```text
finance-a.pdf
hr-a.pdf
```

and compares those IDs against the user's allowed documents.

---

## CI/CD Usage

RAG Access Check uses exit codes that can be used in CI pipelines:

- `0` — all access-control tests passed
- `1` — one or more access-control issues were detected
- `2` — configuration or runtime error

This allows the tool to fail a build or security test automatically.

---

## Status

Early development.

The current release supports offline testing and generic HTTP API testing with basic authentication.

## Contributing

Feedback, test cases, integrations, and pull requests are welcome.

If this tool identifies an access-control issue in your application, please consider opening an issue and sharing:

- what type of RAG application you tested
- what access-control issue was identified
- what change you made to fix it

Please do not include confidential data, credentials, or sensitive system details.

## License

MIT
