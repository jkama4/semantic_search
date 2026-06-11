from typing import List, Dict


def parse_profile_sections(
    text: str
) -> Dict:

    sections: Dict = {
        "summary": "",
        "education": [],
        "work_experience": []
    }

    current_section = "summary"
    summary_lines: List = []

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.lower() == "education:":
            current_section = "education"
            continue
        elif stripped.lower() == "work experience:":
            current_section = "work_experience"
            continue

        if current_section == "summary":
            if stripped:
                summary_lines.append(stripped)
        elif current_section == "education":
            if stripped.startswith("- "):
                sections["education"].append(stripped[2:])
            elif stripped and sections["education"]:
                sections["education"][-1] += f" — {stripped}"
        elif current_section == "work_experience":
            if stripped.startswith("- "):
                sections["work_experience"].append({"title": stripped[2:], "details": []})
            elif stripped and sections["work_experience"]:
                sections["work_experience"][-1]["details"].append(stripped)

    sections["summary"] = " · ".join(summary_lines)
    return sections
