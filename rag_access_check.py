import json


def check_access(user, retrieved_docs, allowed_docs):
    unauthorized = [doc for doc in retrieved_docs if doc not in allowed_docs]

    if unauthorized:
        print(f"FAIL  {user} retrieved unauthorized documents:")
        for doc in unauthorized:
            print(f"  - {doc}")
        return False

    print(f"PASS  {user} retrieved only authorized documents")
    return True


def load_test_cases(path="test_cases.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    data = load_test_cases()

    failures = 0

    for user in data["users"]:
        passed = check_access(
            user["name"],
            user["retrieved"],
            user["allowed"],
        )

        if not passed:
            failures += 1

    print()
    print(f"Completed {len(data['users'])} access-control tests.")
    print(f"Failures: {failures}")
