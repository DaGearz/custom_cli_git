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

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="daggit - custom version control system"
    )
    
    parser.add_argument("command", help="Command to run (init, add, commit, etc.)")
    parser.add_argument("target", nargs="?", help="Target file or input (used with 'add')")  # optional

    args = parser.parse_args()

    # Command: init
    if args.command == "init":
        if os.path.exists(daggit_dir):
            print("Repository already initialized")
        else:
            os.makedirs(objects_dir)
            print(f"Initialized empty Daggit repository in ./{daggit_dir}/")

    # Command: add
    elif args.command == "add":
        #return earlybased on three conditionns
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

        #create index file with
        index_path = os.path.join(daggit_dir, "index")
        with open(index_path, "a") as index_file:
            index_file.write(f"{sha1} {args.target}\n")
    
    #Command: commit
    elif args.command == "commit":
        if not os.path.exists(daggit_dir):
            print("Error: No Daggit repository found. Did you run 'daggit init'?")
            return
        index_path = os.path.join(daggit_dir, index)
        if not os.path.exists("commit")
            os.mkdir("commit")

    else :
        print(f"Error: {args.command} is not a valid command")

if __name__ == "__main__":
    main()
