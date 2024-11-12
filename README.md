# SSH Command Runner for CrackMapExec

This Python script allows you to run a series of SSH commands over a list of IP addresses using [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec). The script supports authentication using either a password or a private key, and it will display the results of the commands executed on remote hosts in a clean, tabular format.This script allows you to quickly run commands on multiple machines, offers flexible authentication options, automates tasks, and presents the results in a clean tabular format, saving time.

## Features:
- Execute multiple SSH commands on remote machines using CrackMapExec.
- Supports authentication using either a password or a private key.
- Display the results in a clean, tabular format using `tabulate`.
- Read a list of IP addresses from a file.
- Option to add custom commands to be executed.

## Prerequisites:
Before using the script, make sure you have the following installed:

- Python 3.6+
- CrackMapExec ([Installation guide](https://github.com/byt3bl33d3r/CrackMapExec))
- Python `tabulate` library (can be installed via pip)

To install the required dependencies:

```bash
pip install tabulate
```

## Usage:

### Command-Line Arguments
The script accepts several arguments that allow you to customize its behavior:
- `--ip_file`: Path to a file containing the list of IP addresses to target
- `--username`: SSH username for authentication.
- `--password`: Password for SSH authentication. Either this or the --key_file option must be provided.
- `--key_file`: Path to a private SSH key file for authentication. Either this or the --password option must be provided.
- `--commands`: A space-separated list of additional commands to execute on the remote machines.

## Example Usage:

### Using Password Authentication
```bash
python ssh_executor.py --ip_file ips.txt --username user --key_file '/path/to/private_key' --commands 'uptime' 'df -h'
```

### Using Private Key Authentication
```bash
python ssh_executor.py --ip_file ips.txt --username user --key_file '/path/to/private_key' --commands 'uptime' 'df -h'
```

## Default Commands:

- `whoami /priv`
- `net user`
- `qwinsta`
- `query user`
- `uname -a`

If you provide additional commands via the `--commands` argument, those will be appended to the default commands.

## Output:

The script will display the results in a table with IP addresses and their corresponding command outputs.

### Exaple Output:

```bash
+-------------+-------------------------+-----------------------------+-----------------------------+------------------------+-----------------------+
| IP          | whoami /priv             | net user                    | qwinsta                     | query user             | uname -a              |
+-------------+-------------------------+-----------------------------+-----------------------------+------------------------+-----------------------+
| 192.168.1.1 | user                     | user1, user2                | 1 RDP-Tcp#1                 | user1                  | Linux server123       |
| 192.168.1.2 | user                     | user1, admin                | 1 RDP-Tcp#1                 | user2                  | Linux server124       |
+-------------+-------------------------+-----------------------------+-----------------------------+------------------------+-----------------------+
```
