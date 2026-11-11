
# This is the program's entry point: it connects scanning, classification, planning, and execution.
from pathlib import Path  # Provides platform-independent filesystem path handling.

from file_scanner import scan_directory  # Imports the first workflow step, which returns metadata for each file.
from classifier import classify_files  # Imports the next step, which labels those files by type.
from organizer import generate_plan, confirm_and_execute  # Imports the final steps: propose moves, ask approval, and execute.


def main():  # Runs the whole workflow in order, passing each step's results to the next.

    print("================================")  # Prints the top border of the application title.
    print("     PERSONAL FILE ORGANIZER")  # Prints the application title.
    print("================================")  # Prints the bottom border of the application title.

    folder = Path(__file__).parent / "test_files"  # Chooses the sample input folder next to this script.

    try:  # Runs the file organization workflow while handling expected filesystem/input errors.

        print("\nScanning directory...")  # Announces that the target directory is being scanned.
        files = scan_directory(folder)  # Step 1: gets file metadata (name, extension, size, and modified time).

        if not files:  # Checks whether the scan returned any files.
            print("No files found!")  # Informs the user that the directory contains no files to organize.
            return  # Stops the workflow because there are no files to process.

        print("\nClassifying files...")  # Announces that the discovered files are being categorized.
        classified = classify_files(files)  # Step 2: converts metadata into file names paired with categories.

        print("\nGenerating execution plan...")  # Announces that an organization plan is being prepared.
        plan = generate_plan(classified)  # Step 3: turns each file/category pair into a proposed move.

        confirm_and_execute(folder, plan)  # Step 4: shows the plan, gets approval, then validates and moves files.

    except (ValueError, OSError) as error:  # Catches invalid-operation and filesystem errors from the workflow.
        print(f"\nError: {error}")  # Displays the caught error message to the user.


if __name__ == "__main__":  # Prevents the workflow from starting just because another module imports this file.
    main()  # Starts the complete scan-to-organize workflow when this script is run.
