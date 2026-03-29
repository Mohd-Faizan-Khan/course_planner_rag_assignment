def check_prerequisites(course, completed_courses, catalog):
    """
    Recursive multi-hop prerequisite check
    """

    def dfs(prereq):
        # already completed
        if prereq in completed_courses:
            return True

        # find prereq course in catalog
        for c in catalog:
            if c["code"] == prereq:

                sub_prereqs = c.get("prerequisites", [])

                # if no further prereqs
                if not sub_prereqs:
                    return prereq in completed_courses

                # check chain
                for p in sub_prereqs:
                    if not dfs(p):
                        return False

                return prereq in completed_courses

        return False

    prereqs = course.get("prerequisites", [])
    missing = []

    for p in prereqs:
        if not dfs(p):
            missing.append(p)

    return len(missing) == 0, missing


def generate_course_plan(
    completed_courses,
    catalog_courses,
    max_courses=3
):
    """
    Generate next semester course plan
    """

    eligible_courses = []
    reasoning = {}

    for course in catalog_courses:

        course_code = course["code"]

        # skip already completed
        if course_code in completed_courses:
            continue

        eligible, missing = check_prerequisites(
            course,
            completed_courses,
            catalog_courses
        )

        if eligible:
            eligible_courses.append(course)

            reasoning[course_code] = {
                "status": "eligible",
                "prerequisites": course.get("prerequisites", [])
            }

        else:
            reasoning[course_code] = {
                "status": "not eligible",
                "missing": missing
            }

    # choose top N
    plan = eligible_courses[:max_courses]

    return plan, reasoning