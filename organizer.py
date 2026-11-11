
# Workflow steps 3 and 4: build a reviewable move plan, then execute it only after user approval.
import json  # Imports JSON formatting for displaying the plan clearly.
import shutil  # Imports file-moving utilities used to execute approved operations.
from pathlib import Path  # Imports path handling for resolving the organization root.
from safety import validate_move  # Imports validation that keeps move operations within safe boundaries.

def generate_plan(classified_files):  # Workflow step 3: turns classifier output into source/destination operations.

    plan = []  # Collects move instructions that will be displayed and later validated.

    for file in classified_files:  # Processes every classified file.

        source = file["name"]  # Gets the current file's source name.
        category = file["category"]  # Gets the destination category for the current file.

        destination = f"{category}/{source}"  # Builds the relative destination inside its category folder.

        plan.append({  # Records the move operation in the plan.
            "action": "move",  # Identifies this operation as a file move.
            "source": source,  # Records the file to move.
            "dest": destination  # Records the intended destination path.
        })  # Finishes adding this move operation.

    return plan  # Returns the proposed operations to main.py; no files are moved at this stage.


def display_plan(plan):  # Shows the user what would happen before any filesystem changes are made.

    print("\n========== EXECUTION PLAN ==========")  # Displays the heading for the plan.

    print(json.dumps(plan, indent=4))  # Prints the plan as readable, indented JSON.

    print("====================================")  # Displays the bottom border of the plan.

def execute_plan(root, plan):  # Runs only after approval: validate all operations first, then move the files.

    root = Path(root).resolve()  # Resolves the organization directory to an absolute path.

    # First ask safety.validate_move() to approve every source and destination; nothing moves in this phase.
    validated_moves = []  # Stores validated source and destination paths before execution begins.

    for operation in plan:  # Checks every requested operation before any file is moved.

        if operation["action"] != "move":  # Rejects operations other than supported move actions.
            raise ValueError("Unsupported action")  # Stops execution when a plan contains an unsupported action.

        src, dest = validate_move(  # Validates and resolves the operation's source and destination.
            root,  # Supplies the allowed root directory.
            operation["source"],  # Supplies the source filename to validate.
            operation["dest"]  # Supplies the destination path to validate.
        )  # Receives the validated absolute source and destination paths.

        validated_moves.append((src, dest))  # Queues the validated paths for the execution phase.

    # Only after all operations pass validation, create category folders and move the files.
    for src, dest in validated_moves:  # Executes each path pair after the full plan passed validation.

        dest.parent.mkdir(parents=True, exist_ok=True)  # Creates missing category folders when necessary.

        # Recheck destination immediately before moving
        if dest.exists() or dest.is_symlink():  # Checks again that no file or symbolic link occupies the destination.
            raise ValueError("Destination already exists")  # Prevents overwriting an existing destination.

        shutil.move(str(src), str(dest))  # Moves the source file to its validated destination.

        print(f"Moved: {src.name} -> {dest}")  # Reports the completed move to the user.


def confirm_and_execute(root, plan):  # Workflow step 4: display the plan, get the user's decision, then act or stop.

    display_plan(plan)  # Presents the proposed operations before requesting approval.

    choice = input(  # Prompts the user to approve or cancel the planned changes.
        "\nDo you want to execute these changes? (yes/no): "  # Displays the confirmation question.
    )  # Stores the user's response.

    if choice.strip().lower() == "yes":  # Accepts an affirmative response regardless of surrounding spaces or case.
        execute_plan(root, plan)  # Sends approved operations through safety checks before moving any file.
        print("\nFiles organized successfully!")  # Confirms that the organization operation completed.

    else:  # Handles any response other than "yes" as a cancellation.
        print("\nOperation cancelled. No files were moved.")  # Informs the user that no moves were performed.
