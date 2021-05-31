#!/usr/bin/env bash

set -euo pipefail

HERE="$(dirname "$0")"
VENVDIR="$HERE/virtualenv"

ensure_venv() {
    if [[ ! -d "$VENVDIR" ]]; then
        python3 -m venv "$VENVDIR"
        . "$VENVDIR/bin/activate"
        pip install -r "$HERE/requirements.txt"
    else
        . "$VENVDIR/bin/activate"
    fi
}

main() {
    ensure_venv

    if [[ -z "${PYTHONPATH:-}" ]]; then
        PYTHONPATH="$PWD"
    else
        PYTHONPATH="$PYTHONPATH:$PWD"
    fi

    export PYTHONPATH

    if [[ "${1:-}" = --bash ]]; then
        shift
        bash -c "$*"
    else
        python3 "$HERE/maildeclutter/__init__.py" "$@"
    fi
}

main "$@"
