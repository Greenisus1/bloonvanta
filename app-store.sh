#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
# pi-app-store-description: Original offline tower defense with10 waves, dart/splash towers, upgrade levels1-3, coin rewards and20 lives.
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-}" in
 install) python3 -c 'import curses;from pathlib import Path;[compile(p.read_bytes(),str(p),"exec") for p in Path(".").glob("*.py")]';python3 install_commands.py ;;
 uninstall) python3 install_commands.py uninstall ;;
 run) shift;exec python3 bloonvanta.py "$@" ;;
 *) echo 'Use: bash app-store.sh install|run|uninstall';exit 1 ;;
esac
