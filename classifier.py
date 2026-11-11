
def classify_file(file):  # Helper used below to assign one scanner record to a category.

    extension = file["extension"]  # Reads the normalized extension from the file's metadata.

    categories = {  # Maps each supported category to the file extensions it accepts.
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],  # Lists common image formats.
        "Documents": [".pdf", ".docx", ".doc", ".txt"],  # Lists common document formats.
        "Videos": [".mp4", ".mkv", ".avi"],  # Lists common video formats.
        "Audio": [".mp3", ".wav", ".aac"],  # Lists common audio formats.
        "Logs": [".log", ".json"],  # Lists log and JSON data formats.
        "Code": [".py", ".cpp", ".java", ".html", ".css", ".js"]  # Lists supported source-code formats.
    }  # Finishes the extension-to-category mapping.

    for category, extensions in categories.items():  # Checks each category's supported extensions.

        if extension in extensions:  # Tests whether this file's extension belongs to the category.
            return category  # Returns the first matching category.

    return "Others"  # Classifies unrecognized extensions into the fallback category.


def classify_files(files):  # Workflow step 2: converts scanner records into the simpler input for plan generation.

    classified = []  # Collects the name/category pairs that organizer.generate_plan() needs.

    for file in files:  # Processes every file discovered by the scanner.

        category = classify_file(file)  # Finds the category for the current file.

        classified.append({  # Adds the file's identifying name and category to the results.
            "name": file["name"],  # Stores the file's name for the organization plan.
            "category": category  # Stores the category selected for the file.
        })  # Finishes adding this file's classification.

    return classified  # Hands the classified records back to main.py for move-plan creation.
