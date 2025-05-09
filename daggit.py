
#argparse is module for implementing basic command line applications
#https://docs.python.org/3/library/argparse.html
import argparse
import os

def main():
    #we must add description when we initiate parser
    parser = argparse.ArgumentParser(
         description="daggit - custom version control system"
         )
    
    #setting arguments. arguments are in the order they appear in code
    parser.add_argument("command", help="Command to run (init, add, commit, etc.)")

      
    parser.add_argument("target", nargs="?", help="Target file or input (used with 'add')") #note: nargis="?" is for optional arguments

    #pull the argument typed into console
    args = parser.parse_args()

    if args.command == "init":
        if os.path.exists(".daggit"):
                print("Repository already initialized")
        else:
            os.mkdir(".daggit")
            print("Initialized empty Daggit repository in ./.daggit/")

    elif args.command == "add":
        if not os.path.exists(".daggit"):
            print("Error: No Daggit repository found. Did you run 'daggit init'?")

        if args.target:
            if not os.path.exists(args.target):
                 print(f"Error: file '{args.target}' does not exist")
            else :
                print(f'Adding file: {args.target}')

        else :
            print("Error: No file specified to add .")

    else:
         print (f"unknown command: {args.command}")

if __name__ == "__main__":
    main()