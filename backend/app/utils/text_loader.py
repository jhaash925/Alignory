import os


def load_resume_text():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "../../data/resume_knowledge.txt"
    )

    file_path = os.path.abspath(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text