#!/usr/bin/env sh

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
build_dir="$script_dir/_build"
output_name=${1:-dissertation_reviewed.pdf}

case "$output_name" in
    ''|.|..|*/*)
        printf '%s\n' 'Output name must be a file name without a directory path.' >&2
        exit 2
        ;;
esac

bundled="$script_dir/../_tools/tectonic/tectonic"
if [ -x "$bundled" ]; then
    tectonic="$bundled"
elif command -v tectonic >/dev/null 2>&1; then
    tectonic=$(command -v tectonic)
else
    if ! command -v curl >/dev/null 2>&1; then
        printf '%s\n' 'Tectonic and curl were not found. Install Tectonic in PATH.' >&2
        exit 1
    fi

    tool_dir="$script_dir/../_tools/tectonic"
    installer="$tool_dir/.install-tectonic.sh"
    mkdir -p "$tool_dir"

    printf '%s\n' 'Tectonic was not found. Downloading the latest official release...'
    curl --proto '=https' --tlsv1.2 -fsSL \
        https://drop-sh.fullyjustified.net \
        -o "$installer"
    (
        cd "$tool_dir"
        sh "$installer"
    )
    rm -f "$installer"

    if [ ! -x "$bundled" ]; then
        printf '%s\n' 'The official installer did not create an executable Tectonic file.' >&2
        exit 1
    fi
    tectonic="$bundled"
fi

mkdir -p "$build_dir"

(
    cd "$script_dir"
    "$tectonic" main.tex --outdir "$build_dir" --keep-logs
)

cp "$build_dir/main.pdf" "$script_dir/$output_name"
printf 'Ready: %s\n' "$script_dir/$output_name"
