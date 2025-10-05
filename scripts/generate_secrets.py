#!/usr/bin/env python3
"""
Generate Secure Random Secrets

This script generates cryptographically secure random secrets for use in
environment variables like SECRET_KEY, DB_PASSWORD, etc.

Usage:
    python scripts/generate_secrets.py

    # Generate and append to .env
    python scripts/generate_secrets.py >> .env

    # Generate specific number of secrets
    python scripts/generate_secrets.py --count 5
"""

import secrets
import argparse
import string


def generate_secret(length: int = 32) -> str:
    """
    Generate a cryptographically secure random secret.

    Args:
        length: Number of characters in the secret

    Returns:
        URL-safe base64-encoded secret string
    """
    return secrets.token_urlsafe(length)


def generate_password(length: int = 16, include_symbols: bool = True) -> str:
    """
    Generate a random password with letters, digits, and optionally symbols.

    Args:
        length: Number of characters in the password
        include_symbols: Whether to include special characters

    Returns:
        Random password string
    """
    alphabet = string.ascii_letters + string.digits
    if include_symbols:
        alphabet += string.punctuation

    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def generate_hex_secret(length: int = 32) -> str:
    """
    Generate a hexadecimal secret (useful for some APIs).

    Args:
        length: Number of bytes (output will be 2x this length)

    Returns:
        Hexadecimal string
    """
    return secrets.token_hex(length)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate secure random secrets for Performia',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate default secrets
  python scripts/generate_secrets.py

  # Generate and append to .env
  python scripts/generate_secrets.py >> .env

  # Generate specific number of secrets
  python scripts/generate_secrets.py --count 5

  # Generate only passwords
  python scripts/generate_secrets.py --type password
        """
    )

    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of secrets to generate (default: 1)'
    )

    parser.add_argument(
        '--type',
        choices=['all', 'secret', 'password', 'hex'],
        default='all',
        help='Type of secret to generate (default: all)'
    )

    parser.add_argument(
        '--length',
        type=int,
        default=32,
        help='Length of secret in characters/bytes (default: 32)'
    )

    args = parser.parse_args()

    print("# Secure Random Secrets for Performia")
    print("# Generated using Python secrets module")
    print("# Add these to your .env file\n")

    if args.type in ['all', 'secret']:
        print("# Application Secret Key (for session signing, etc.)")
        for i in range(args.count):
            secret = generate_secret(args.length)
            if args.count > 1:
                print(f"SECRET_KEY_{i+1}={secret}")
            else:
                print(f"SECRET_KEY={secret}")
        print()

    if args.type in ['all', 'password']:
        print("# Database Password")
        for i in range(args.count):
            password = generate_password(args.length // 2)
            if args.count > 1:
                print(f"DB_PASSWORD_{i+1}={password}")
            else:
                print(f"DB_PASSWORD={password}")
        print()

    if args.type in ['all', 'hex']:
        print("# Hexadecimal Secret (for API tokens, etc.)")
        for i in range(args.count):
            hex_secret = generate_hex_secret(args.length // 2)
            if args.count > 1:
                print(f"API_TOKEN_{i+1}={hex_secret}")
            else:
                print(f"API_TOKEN={hex_secret}")
        print()

    print("# Security Notes:")
    print("# 1. Never commit these secrets to version control")
    print("# 2. Store securely (environment variables, secret manager)")
    print("# 3. Rotate secrets regularly")
    print("# 4. Use different secrets for dev/staging/production")


if __name__ == "__main__":
    main()
