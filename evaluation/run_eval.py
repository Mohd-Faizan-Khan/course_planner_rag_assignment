from query import query

with open("evaluation/test_queries.txt") as f:
    queries = f.readlines()

for q in queries:
    print("\n======================")
    print("Q:", q.strip())
    query(q.strip())