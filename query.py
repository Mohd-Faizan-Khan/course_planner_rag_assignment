from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from planner.course_planner import generate_course_plan

INDEX_PATH = "faiss_index"


def load_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(search_kwargs={"k": 4})


def extract_prereqs(docs):
    prereqs = []

    for doc in docs:
        text = doc.page_content.lower()

        if "prerequisites" in text:
            prereqs.append(doc.page_content)

    return prereqs


def extract_courses_from_docs(docs):
    # import re

    courses = []

    for doc in docs:
        text = doc.page_content

        # extract course code
        code_match = re.search(r"(CS\d{3}|MATH\d{3})", text)
        if not code_match:
            continue

        code = code_match.group(1)

        # extract title from "Course: XXX Title"
        title_match = re.search(
            r"Course:\s*(.*?)\n",
            text,
            re.IGNORECASE
        )

        title = f"Course {code}"

        if title_match:
            title = title_match.group(1)

        # extract prereqs
        prereq_match = re.search(
            r"Prerequisites?:\s*(.*)",
            text,
            re.IGNORECASE
        )

        prereqs = []

        if prereq_match:
            prereqs = re.findall(
                r"(CS\d{3}|MATH\d{3})",
                prereq_match.group(1)
            )

        courses.append({
            "code": code,
            "title": title,
            "prerequisites": prereqs
        })

    return courses


def extract_completed_courses(question):
    # import re

    q = question.upper()

    # Case 1: Completed:
    match = re.search(r"COMPLETED:\s*(.*)", q)
    if match:
        courses = re.findall(
            r"(CS\d{3}|MATH\d{3})",
            match.group(1)
        )
        return list(set(courses))

    # Case 2: after
    match = re.search(r"AFTER\s+(.*)", q)
    if match:
        courses = re.findall(
            r"(CS\d{3}|MATH\d{3})",
            match.group(1)
        )
        return list(set(courses))

    # Case 3: "after CS201" inside sentence
    courses = re.findall(
        r"AFTER\s+(CS\d{3}|MATH\d{3})",
        q
    )

    if courses:
        return list(set(courses))

    return []


def check_eligibility(question, docs):
    # import re

    q = question.upper()

    # extract target course
    target_match = re.search(r"(CS\d{3})", q)
    if not target_match:
        return "Need more information", docs

    target = target_match.group(1)

    # extract completed
    completed = re.findall(
        r"AFTER\s+(.*)", q
    )

    completed_courses = []

    if completed:
        completed_courses = re.findall(
            r"(CS\d{3}|MATH\d{3})",
            completed[0]
        )

    # find prereqs
    for doc in docs:
        text = doc.page_content.upper()

        if target in text:

            prereq_match = re.search(
                r"PREREQUISITES?:\s*(.*)",
                text
            )

            if not prereq_match:
                return "Eligible", docs

            prereqs = re.findall(
                r"(CS\d{3}|MATH\d{3})",
                prereq_match.group(1)
            )

            missing = [
                p for p in prereqs
                if p not in completed_courses
            ]

            if missing:
                return f"Not eligible — missing {missing}", docs

            return "Eligible", docs

    return "Not in catalog", docs


def format_response(question, docs):
    decision, prereqs = check_eligibility(question, docs)

    print("\n==============================")
    print("Answer / Plan:\n")
    print(decision)

    print("\nWhy:")
    print("Decision based on prerequisite matching.")

    print("\nCitations:")
    for i, doc in enumerate(docs):
        print(f"Source {i+1}:")
        print(doc.page_content[:200])
        print()

    print("Clarifying Questions:")
    if decision == "Need more information":
        print("- What courses have you completed?")
    else:
        print("- None")

    print("\nAssumptions / Not in catalog:")
    print("- Course availability not checked")

    print("==============================\n")


def verify_response(plan, docs):
    if not docs:
        return False
    return True

def get_all_documents():
    retriever = load_retriever()
    return retriever.vectorstore.docstore._dict.values()


def query(question):
    retriever = load_retriever()
    docs = retriever.invoke(question)

    # PLAN MODE
    if "plan" in question.lower():

        completed = extract_completed_courses(question)

        all_docs = get_all_documents()
        catalog = extract_courses_from_docs(all_docs)
        plan, reasoning = generate_course_plan(
            completed,
            catalog,
            max_courses=5
        )

        if not verify_response(plan, docs):
            print("Response failed verification")
            return

        print("\n==============================")
        print("Answer / Plan:\n")

        for course in plan:
            code = course["code"]

            print(f"{code} - {course['title']}")
            print("Why:", reasoning[code])
            print()

        print("Citations:")
        for i, doc in enumerate(docs):
            print(f"Source {i+1}:")
            print(doc.page_content[:200])
            print()

        print("==============================\n")
        return

    # DEFAULT MODE
    format_response(question, docs)


def build_catalog():
    """
    Temporary catalog 
    """

    catalog = [
        {
            "code": "CS101",
            "title": "Intro to CS",
            "prerequisites": []
        },
        {
            "code": "CS201",
            "title": "Data Structures",
            "prerequisites": ["CS101"]
        },
        {
            "code": "CS301",
            "title": "Algorithms",
            "prerequisites": ["CS201"]
        }
    ]

    return catalog



if __name__ == "__main__":
    while True:
        q = input("\nAsk question: ")
        query(q)