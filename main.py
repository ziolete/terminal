import sys
import os
import shutil
import subprocess
import shlex
BUILTINS = ["echo", "exit"]
def main():
    while True:
        sys.stdout.write("$ ")
        command = input().strip()

        if not command:
            continue

        if command == 'exit':
            break

        elif '>' in command:
            subprocess.run(command, shell=True)
            continue

        elif command == 'cd':
            tokens = command.split(maxsplit=1)
            if len(tokens) < 2:
                print("cd: missing argument")
                continue

            path = tokens[1]
            if path == '~':
                os.chdir(os.environ.get('HOME', '/'))
            elif os.path.isdir(path):
                os.chdir(path)
            else:
                print(f"cd: {path}: No such file or directory")

        elif command == 'pwd':
            print(os.getcwd())

        elif command.startswith('echo'):
            args = shlex.split(command)
            print(" ".join(args[1:]))

        elif command.startswith('type'):
            tokens = command.split(maxsplit=1)
            if len(tokens) < 2:
                print("type: missing argument")
                continue
            arg = tokens[1]
            if arg in ['cd', 'echo', 'exit', 'pwd', 'type']:
                print(f"{arg} is a shell builtin")
            elif path := shutil.which(arg):
                print(f"{arg} is {path}")
            else:
                print(f"{arg}: not found")



        else:
            parts = shlex.split(command)
            try:
                subprocess.run(parts)
            except FileNotFoundError:
                print(f"{parts[0]}: command not found")


if __name__ == "__main__":
    main()

