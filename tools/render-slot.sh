#!/bin/bash
# Runs one heavy render command in one of a few shared slots (Hoang, 7 Nov 2026: parallel is fine, without overloading the laptop).
# Usage: tools/render-slot.sh <command> [args...]
# RENDER_SLOTS  how many renders may run at once (default 3)
# RENDER_MAXLOAD  a new render waits while the 1-minute load is above this (default 14, on 11 cores). Lesson renders count too.
# Pause: touch "${TMPDIR:-/tmp}/edlintics-render-slot.pause"; resume: rm it.
SLOTS="${RENDER_SLOTS:-3}"; MAXLOAD="${RENDER_MAXLOAD:-14}"; BASE="${TMPDIR:-/tmp}/edlintics-render-slot"
while :; do
  LOAD=$(sysctl -n vm.loadavg | awk '{print int($2)}')
  # touch "$BASE.pause" to hold every new render (e.g. while another project needs the laptop); rm it to resume
  if [ "$LOAD" -lt "$MAXLOAD" ] && [ ! -e "$BASE.pause" ]; then
    for i in $(seq 1 "$SLOTS"); do
      if mkdir "$BASE.$i" 2>/dev/null; then echo $$ > "$BASE.$i/pid"; HELD="$BASE.$i"; break; fi
      holder=$(cat "$BASE.$i/pid" 2>/dev/null)
      if [ -n "$holder" ] && ! kill -0 "$holder" 2>/dev/null; then rm -rf "$BASE.$i"; fi
    done
    [ -n "$HELD" ] && break
  fi
  sleep 15
done
trap 'rm -rf "$HELD"' EXIT
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2 NUMEXPR_NUM_THREADS=2
nice -n 10 "$@"
