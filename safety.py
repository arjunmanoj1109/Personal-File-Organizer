
# Called by organizer.execute_plan() for every proposed move before any files are moved.
from pathlib import Path  # Imports path utilities for resolving and checking filesystem locations.


def validate_move(root, source, destination):  # Approves one move or raises an error that stops plan execution.

    root = Path(root).resolve()  # Converts the allowed root directory to an absolute resolved path.

    source_path = Path(source)  # Parses the requested source as a filesystem path.
    destination_path = Path(destination)  # Parses the requested destination as a filesystem path.

    # Only allow simple filenames as sources
    if source_path.is_absolute() or len(source_path.parts) != 1:  # Rejects absolute paths and sources with directory components.
        raise ValueError("Invalid source path")  # Reports that the source must be a simple filename.

    # Prevent absolute paths and directory traversal
    if destination_path.is_absolute() or ".." in destination_path.parts:  # Rejects absolute paths and parent-directory traversal.
        raise ValueError("Unsafe destination path")  # Reports that the requested destination could escape the root.

    if len(destination_path.parts) < 2:  # Requires the destination to include a category folder and filename.
        raise ValueError("Destination must be inside a category folder")  # Explains the required destination structure.

    src = (root / source_path).resolve()  # Resolves the source path relative to the allowed root.
    dest = (root / destination_path).resolve()  # Resolves the destination path relative to the allowed root.

    # Ensure both paths stay inside the selected directory
    if not src.is_relative_to(root):  # Verifies that the resolved source remains under the allowed root.
        raise ValueError("Source outside allowed directory")  # Rejects a source that resolves outside the root.

    if not dest.is_relative_to(root):  # Verifies that the resolved destination remains under the allowed root.
        raise ValueError("Destination outside allowed directory")  # Rejects a destination that resolves outside the root.

    # Source must be a normal file, not a symbolic link
    if not src.is_file() or src.is_symlink():  # Requires the source to be a regular file, not a symbolic link.
        raise ValueError("Invalid source file")  # Reports that the source is missing or unsafe.

    # Never overwrite an existing file
    if dest.exists() or dest.is_symlink():  # Checks whether a file or symbolic link already occupies the destination.
        raise ValueError("Destination already exists")  # Prevents replacing an existing destination.

    # Check that destination folders are safe
    current = root  # Starts checking the destination's parent folders from the allowed root.

    for part in destination_path.parts[:-1]:  # Checks each destination directory component, excluding the filename.
        current = current / part  # Advances to the next directory in the destination path.

        if current.is_symlink():  # Detects category directories that redirect through symbolic links.
            raise ValueError("Symbolic link directory not allowed")  # Rejects a destination through a symbolic link.

        if current.exists() and not current.is_dir():  # Rejects an existing path component that is not a directory.
            raise ValueError("Invalid destination directory")  # Reports the invalid destination folder structure.

    return src, dest  # Gives organizer.execute_plan() safe absolute paths to queue for the move phase.
