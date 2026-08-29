import argparse
import json
import os
import sys

import requests


def check_access(user, retrieved_docs, allowed_docs):
    unauthorized = [doc for doc in retrieved_docs if doc not in allowed_docs]

    if unauthorized:
        print(f"[FAIL] {user}")
        print("Unauthorized documents retrieved:")
        for doc in unauthorized:
            print(f"  - {doc}")
        print()
        return False

    print(f"[PASS] {user}")
    print("No unauthorized documents retrieved.")
    print()
    return True


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_auth_headers(auth_config):
    auth_type = auth_config.get("type", "none").lower()

    if auth_type == "none":
        return {}

    if auth_type == "bearer":
        token_env = auth_config.get("token_env")
        token = os.getenv(token_env)

        if not token:
            raise ValueError(
                f"Environment variable '{token_env}' is not set."
            )

        return {
            "Authorization": f"Bearer {token}"
        }

    if auth_type == "api_key":
        header_name = auth_config.get("header_name", "X-API-Key")
        key_env = auth_config.get("key_env")
        api_key = os.getenv(key_env)

        if not api_key:
            raise ValueError(
                f"Environment variable '{key_env}' is not set."
            )

        return {
            header_name: api_key
        }

    raise ValueError(f"Unsupported auth type: {auth_type}")


def extract_document_ids(response_json, results_field, document_id_field):
    results = response_json.get(results_field, [])

    if not isinstance(results, list):
        raise ValueError(
            f"Response field '{results_field}' must contain a list."
        )

    document_ids = []

    for item in results:
        if not isinstance(item, dict):
            continue

        document_id = item.get(document_id_field)

        if document_id is not None:
            document_ids.append(str(document_id))

    return document_ids


def run_offline(path="test_cases.json"):
    data = load_json(path)

    print("RAG Access Check Results")
    print("========================")
    print()

    passed = 0
    failed = 0

    for user in data["users"]:
        result = check_access(
            user["name"],
            user["retrieved"],
            user["allowed"],
        )

        if result:
            passed += 1
        else:
            failed += 1

    return print_summary(len(data["users"]), passed, failed)


def run_live(config_path):
    config = load_json(config_path)

    endpoint = config["endpoint"]
    method = config.get("method", "POST").upper()
    auth = config.get("auth", {"type": "none"})
    request_config = config["request"]
    response_config = config["response"]

    headers = get_auth_headers(auth)

    query_field = request_config.get("query_field", "query")
    query = request_config["query"]

    results_field = response_config["results_field"]
    document_id_field = response_config["document_id_field"]

    print("RAG Access Check - Live API Mode")
    print("===============================")
    print(f"Endpoint: {endpoint}")
    print()

    passed = 0
    failed = 0

    for user in config["users"]:
        payload = {
            query_field: query
        }

        print(f"Testing: {user['name']}")

        try:
            if method == "POST":
                response = requests.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=30,
                )
            elif method == "GET":
                response = requests.get(
                    endpoint,
                    params=payload,
                    headers=headers,
                    timeout=30,
                )
            else:
                raise ValueError(
                    f"Unsupported HTTP method: {method}"
                )

            response.raise_for_status()

            response_json = response.json()

            retrieved_docs = extract_document_ids(
                response_json,
                results_field,
                document_id_field,
            )

            result = check_access(
                user["name"],
                retrieved_docs,
                user["allowed"],
            )

            if result:
                passed += 1
            else:
                failed += 1

        except (requests.RequestException, ValueError, json.JSONDecodeError) as error:
            print(f"[ERROR] {user['name']}")
            print(str(error))
            print()
            failed += 1

    return print_summary(len(config["users"]), passed, failed)


def print_summary(total, passed, failed):
    print("Summary")
    print("-------")
    print(f"Users tested: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Result: ACCESS-CONTROL ISSUE DETECTED")
        return 1

    print("Result: ALL ACCESS-CONTROL TESTS PASSED")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Test RAG applications for unauthorized document retrieval."
    )

    parser.add_argument(
        "--config",
        help="Path to a live RAG API configuration JSON file.",
    )

    parser.add_argument(
        "--offline",
        default="test_cases.json",
        help="Path to offline test cases. Default: test_cases.json",
    )

    args = parser.parse_args()

    try:
        if args.config:
            exit_code = run_live(args.config)
        else:
            exit_code = run_offline(args.offline)

        sys.exit(exit_code)

    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        sys.exit(2)


if __name__ == "__main__":
    main()
