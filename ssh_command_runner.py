import subprocess
import argparse
from tabulate import tabulate
import os
import csv
import re

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
parser.add_argument('--output_csv', action='store_true', help="Save results to a CSV file")
parser.add_argument('--output_html', action='store_true', help="Save results to an HTML file")

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
            if process.returncode == 0:
                result = process.stdout.strip()
            else:
                result = f"Error: {process.stderr.strip()}"
            ip_results.append(result)
        except ValueError as ve:
            ip_results.append(str(ve))
        except Exception as e:
            ip_results.append(f"Error executing command: {e}")
    results.append(ip_results)

headers = ["IP"] + default_commands
print(tabulate(results, headers=headers, tablefmt="grid"))

if args.output_csv:
    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for result in results:
            writer.writerow(result)
    print("Results saved to 'output.csv'")

if args.output_html:
    with open('output.html', mode='w') as file:
        file.write('<html><head><title>Command Execution Results</title></head><body>')
        file.write('<h2>Command Execution Results</h2>')
        file.write('<table border="1" style="border-collapse: collapse; width: 100%;">')
        file.write('<tr>')
        for header in headers:
            file.write(f'<th style="padding: 8px; text-align: center;">{header}</th>')
        file.write('</tr>')
        for result in results:
            file.write('<tr>')
            for col in result:
                file.write(f'<td style="padding: 8px; text-align: center;">{col}</td>')
            file.write('</tr>')
        file.write('</table></body></html>')
    print("Results saved to 'output.html'")
