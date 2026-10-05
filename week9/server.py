from fastmcp import FastMCP

mcp = FastMCP("Employee Directory")


EMPLOYEES = [
    {
        "id": "INVX001",
        "name": "Dharmesh",
        "department": "PHP",
        "role": "Senior Backend Developer",
        "location": "Ahmedabad",
        "skills": ["Python", "Node.js", "PostgreSQL"],
    },
    {
        "id": "INVX002",
        "name": "Himanshu",
        "department": "PHP",
        "role": "Frontend Developer",
        "location": "Mumbai",
        "skills": ["React", "Next.js", "TypeScript"],
    },
    {
        "id": "INVX003",
        "name": "Dhruv",
        "department": "DevOps",
        "role": "DevOps Engineer",
        "location": "Ahmedabad",
        "skills": ["AWS", "Docker", "Kubernetes"],
    },
    {
        "id": "INVX004",
        "name": "Khushboo",
        "department": "HR",
        "role": "HR Manager",
        "location": "Pune",
        "skills": ["Recruitment", "Employee Relations"],
    },
    {
        "id": "INVX005",
        "name": "Bhushan",
        "department": "Sales",
        "role": "Sales Manager",
        "location": "Delhi",
        "skills": ["B2B Sales", "CRM", "Negotiation"],
    },
]


@mcp.resource("employees://directory")
def employee_directory() -> str:
    """Return the complete employee directory."""

    lines = []

    for employee in EMPLOYEES:
        lines.append(
            f"{employee['id']} | "
            f"{employee['name']} | "
            f"{employee['department']} | "
            f"{employee['role']} | "
            f"{employee['location']}"
        )

    return "\n".join(lines)


@mcp.tool
def search_employees(
    query: str,
    department: str | None = None,
) -> list[dict]:
    """
    Search employees by name, role, skill, location or department.
    Optionally filter by department.
    """

    query = query.lower().strip()

    results = []

    for employee in EMPLOYEES:

        searchable_text = " ".join(
            [
                employee["name"],
                employee["department"],
                employee["role"],
                employee["location"],
                *employee["skills"],
            ]
        ).lower()

        matches_query = query in searchable_text

        matches_department = (
            department is None
            or employee["department"].lower() == department.lower()
        )

        if matches_query and matches_department:
            results.append(employee)

    return results


@mcp.tool
def get_employee(employee_id: str) -> dict:
    """Get an employee by employee ID."""

    for employee in EMPLOYEES:
        if employee["id"].lower() == employee_id.lower():
            return employee

    return {
        "error": f"Employee {employee_id} not found"
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
