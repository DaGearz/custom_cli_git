# argparse is module for implementing basic command line applications
# https://docs.python.org/3/library/argparse.html
import argparse
import os
import hashlib
from datetime import datetime

def main():
    # Define core directory paths once
    daggit_dir = ".daggit"
    objects_dir = os.path.join(daggit_dir, "objects")
    commits_dir = os.path.join(daggit_dir, "commits")
    index_path = os.path.join(daggit_dir, "index")
    logs_dir = os.path.join(daggit_dir, "logs")

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
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(commit_path, "w") as commit_file:
                commit_file.write(f"Timestamp: {timestamp}\n")
                commit_file.write(f"Message: {message}\n")
                commit_file.write(index_content)
            print(f"Committed as: {commit_hash}")
        else:
            print("There are no updates to commit")

    elif args.command == "logs":

        #early return if commit directory doesnt exist
        if not os.path.exists(commits_dir):
            return print("No commits found")
        
        #early return if no files in commit directory
        commit_files = os.listdir(commits_dir)
        if not commit_files:
            return print("No commits found")
        
        #create log directory
        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)
        
        # Sort by modification time, newest first
        commit_files.sort(key=lambda f: os.path.getmtime(os.path.join(commits_dir, f)), reverse=True)

        #loop over all files in commit
        for commit_hash in commit_files:
            commit_path = os.path.join(commits_dir, commit_hash)
            with open(commit_path, "r") as f:
                lines = f.readlines()
                timestamp_line = lines[0].strip() if len(lines) > 0 else "Timestamp: unknown"
                message_line = lines[1].strip() if len(lines) > 1 else "Message: no message"
                logs_path = os.path.join(logs_dir, "logs.txt")
                with open(logs_path, "a") as f:
                    f.write(f"Commit hash: {commit_hash}\n")
                    f.write(f"{timestamp_line}\n")
                    f.write(f"{message_line}\n")
                    f.write("-" * 40 + "\n")

                print(f"Commit hash: {commit_hash}")
                print(timestamp_line)
                print(message_line)
                print("-" * 40 + "\n")

    elif args.command == "status":
        staged = []
        modified = []
        untracked = []

        #Read indexed files
        indexed_files = {}
        if os.path.exists(index_path):
            with open(index_path, "r") as f:
                for line in f:
                    parts = line.strip().split(" ",1)
                    if len(parts) == 2:
                        indexed_files[parts[1]] = parts[0]

        #walk through current working directory
        for fname in os.listdir("."):

            #exlude program and .daggit directory
            if fname.startswith(".") or fname in ["daggit.py"]:
                continue

            #hash each file
            if os.path.isfile(fname):
                with open(fname, "rb") as f:
                    content = f.read()
                file_hash = hashlib.sha1(content).hexdigest()

                #compare above hash to saved hash and use to save in approriate array
                if fname in indexed_files:
                    #if file exist in both and match
                    if file_hash == indexed_files[fname]:
                        staged.append(fname)
                    #if file exist and both and hash dont match
                    else:
                        modified.append(fname)
                #if file doesn't exist in staged. Meaning these are new files that have not been added
                else:
                    untracked.append(fname)

        #Display status
        print("Staged Files")
        for f in staged:
            print(f" {f}")

        print("\nModified files:")
        for f in modified:
            print(f" {f}")

        print("\nUntracked files:")
        for f in untracked:
            print(f" {f}")



    else:
        print(f"Error: {args.command} is not a valid command")

if __name__ == "__main__":
    main()
