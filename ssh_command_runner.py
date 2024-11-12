import subprocess
import argparse
from tabulate import tabulate
import os

'''
Created by Haktan Durak
Check my github repository https://github.com/Haktan-Durak/
'''

parser = argparse.ArgumentParser(description="Run commands over SSH and display the results.")
parser.add_argument('--ip_file', type=str, required=True, help="IP file with path")
parser.add_argument('--username', type=str, required=True, help="Username")
parser.add_argument('--password', type=str, help="Password (optional)")
parser.add_argument('--key_file', type=str, help="Private key file with path (optional)")
parser.add_argument('--commands', nargs='*', help="Additional commands (space-separated)")

args = parser.parse_args()

if not os.path.isfile(args.ip_file):
    print(f"Error: IP file '{args.ip_file}' not found or not readable.")
    exit(1)

with open(args.ip_file, 'r') as file:
    ip_list = [line.strip() for line in file if line.strip()]

if not ip_list:
    print("Error: IP file is empty or contains only invalid entries.")
    exit(1)

default_commands = [
    "whoami /priv",
    "net user",
    "qwinsta",
    "query user",
    "uname -a"
]

if args.commands:
    default_commands.extend(args.commands)

results = []

for ip in ip_list:
    ip_results = [ip]
    for command in default_commands:
        try:
            if args.key_file:
                cmd = ["crackmapexec", "ssh", ip, "-u", args.username, "-k", args.key_file, "-x", command]
            elif args.password:
                cmd = ["crackmapexec", "ssh", ip, "-u", args.username, "-p", args.password, "-x", command]
            else:
                raise ValueError("Either password or key file must be provided.")

            process = subprocess.run(cmd, capture_output=True, text=True)
            result = process.stdout if process.returncode == 0 else process.stderr
            ip_results.append(result.strip())
        except ValueError as ve:
            ip_results.append(str(ve))
        except Exception as e:
            ip_results.append(f"Error executing command: {e}")
    results.append(ip_results)

headers = ["IP"] + default_commands
print(tabulate(results, headers=headers, tablefmt="grid"))
