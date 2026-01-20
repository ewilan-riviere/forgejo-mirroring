"""forgejo-mirroring main"""

import sys
import logging
import argparse
from forgejo_mirroring.env import python_check, logger
from forgejo_mirroring.command import CommandSync
from .args import ForgejoMirroringArgs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    """forgejo-mirroring main"""
    parser = argparse.ArgumentParser(
        prog="forgejo-mirroring",
        description="Migrate repositories to Forgejo with mirroring",
    )

    args = ForgejoMirroringArgs(parser)
    python_check()

    print(f"Execute command {args.command}...\n")

    try:
        if args.command == "sync":
            CommandSync(args, override=False)
        elif args.command == "override":
            CommandSync(args, override=True)
    except Exception as e:
        logger.error("Error %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
