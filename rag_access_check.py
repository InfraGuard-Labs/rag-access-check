import json
import sys


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


def load_test_cases(path="test_cases.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    print("RAG Access Check Results")
    print("========================")
    print()

    data = load_test_cases()

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

    print("Summary")
    print("-------")
    print(f"Users tested: {len(data['users'])}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Result: ACCESS-CONTROL ISSUE DETECTED")
        sys.exit(1)

    print("Result: ALL ACCESS-CONTROL TESTS PASSED")
    sys.exit(0)
