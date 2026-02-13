from app.core.firebase_service import db

def calculate_job_population(location, job):
    query = db.collection("role") \
        .where("Location", "==", location) \
        .where("Job", "==", job) \
        .stream()

    return len(list(query))


def dynamic_salary(location, job, base_salary):

    population = calculate_job_population(location, job)

    if population > 5:
        return int(base_salary * 0.9)

    if population < 2:
        return int(base_salary * 1.2)

    return base_salary
