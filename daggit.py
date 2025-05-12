# argparse is module for implementing basic command line applications
# https://docs.python.org/3/library/argparse.html
import argparse
import os
import hashlib

def main():
    # Define core directory paths once
    daggit_dir = ".daggit"
    objects_dir = os.path.join(daggit_dir, "objects")
    commits_dir = os.path.join(daggit_dir, "commits")
    index_path = os.path.join(daggit_dir, "index")

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="daggit - custom version control system"
    )
    
    parser.add_argument("command", help="Command to run (init, add, commit, etc.)")
    parser.add_argument("target", nargs="?", help="Target file (used with 'add') or commit message (used with 'commit')")  # optional

    args = parser.parse_args()

    # Command: init
    if args.command == "init":
        if os.path.exists(daggit_dir):
            print("Repository already initialized")
        else:
            os.makedirs(objects_dir)
            os.makedirs(commits_dir)
            print(f"Initialized Daggit repository in ./{daggit_dir}/")

    # Command: add
    elif args.command == "add":
        # Return early based on three conditions
        if not os.path.exists(daggit_dir):
            print("Error: No Daggit repository found. Did you run 'daggit init'?")
            return

        if not args.target:
            print("Error: Must provide a file")
            return
        
        if not os.path.exists(args.target):
            print("Error: Target file does not exist.")
            return

        # Read the file in binary mode
        with open(args.target, "rb") as f:
            content = f.read()

        # Hash the content using SHA1
        sha1 = hashlib.sha1(content).hexdigest()
        object_path = os.path.join(objects_dir, sha1)

        # Write content if object doesn't already exist
        if not os.path.exists(object_path):
            with open(object_path, "wb") as f:
                f.write(content)
            print(f"File stored as: {sha1}")
        else:
            print("File already stored")

        # Append entry to .daggit/index
        with open(index_path, "a") as index_file:
            index_file.write(f"{sha1} {args.target}\n")

    # Command: commit
    elif args.command == "commit":
        # Early return if .daggit doesn't exist
        if not os.path.exists(daggit_dir):
            print("Error: No Daggit repository found. Did you run 'daggit init'?")
            return
        
        # Return if index file doesn't exist
        if not os.path.exists(index_path):
            print("Nothing to commit.")
            return

        # Read staged files
        with open(index_path, "r") as index_file:
            index_content = index_file.read()

        # If index is empty or only whitespace
        if not index_content.strip():
            print("Nothing to commit.")
            return

        # Generate commit hash from index content
        commit_hash = hashlib.sha1(index_content.encode()).hexdigest()

        # Ensure commits directory exists
        if not os.path.exists(commits_dir):
            os.makedirs(commits_dir)

        # Save snapshot as commit file
        commit_path = os.path.join(commits_dir, commit_hash)
        if not os.path.exists(commit_path):
            message = args.target 
            with open(commit_path, "w") as commit_file:
                commit_file.write(f"Message: {message}\n")
                commit_file.write(index_content)
            print(f"Committed as: {commit_hash}")
        else:
            print("There are no updates to commit")

    else:
        print(f"Error: {args.command} is not a valid command")

if __name__ == "__main__":
    main()
