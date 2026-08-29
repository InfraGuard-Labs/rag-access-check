def check_access(user, retrieved_docs, allowed_docs):
    unauthorized = [doc for doc in retrieved_docs if doc not in allowed_docs]

    if unauthorized:
        print(f"FAIL  {user} retrieved unauthorized documents:")
        for doc in unauthorized:
            print(f"  - {doc}")
        return False

    print(f"PASS  {user} retrieved only authorized documents")
    return True


if __name__ == "__main__":
    users = {
        "User A": {
            "allowed": ["finance-a.pdf", "finance-b.pdf"],
            "retrieved": ["finance-a.pdf", "hr-a.pdf"],
        },
        "User B": {
            "allowed": ["hr-a.pdf", "hr-b.pdf"],
            "retrieved": ["hr-a.pdf", "hr-b.pdf"],
        },
    }

    for user, data in users.items():
        check_access(user, data["retrieved"], data["allowed"])
