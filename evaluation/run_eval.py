from query import query

tests = [
    "Can I take CS301 after CS101?",
    "Completed: CS101 plan my semester",
    "Completed: CS101 CS102 CS201 plan",
    "Can I take CS401 after CS301?",
    "Who teaches CS301?"
]

for t in tests:
    print("\n================")
    print("Q:", t)
    query(t)