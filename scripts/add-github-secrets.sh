#!/usr/bin/env bash
set -euo pipefail

# add-github-secrets.sh
# Usage:
#   GH_REPO="owner/repo" VPS_SSH_PRIVATE_KEY_FILE=~/.ssh/vps_key \
#   REPO_SSH_PRIVATE_KEY_FILE=~/.ssh/repo_key VPS_HOST=1.2.3.4 \
#   VPS_USER=deploy VPS_DEPLOY_PATH=/var/www/faceit-ai-bot \
#   ./scripts/add-github-secrets.sh

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required. Install from https://cli.github.com/"
  exit 1
fi

if [ -z "${GH_REPO:-}" ]; then
  echo "Please set GH_REPO environment variable (owner/repo)"
  exit 1
fi

get_file_content() {
  local f="$1"
  if [ -n "$f" ] && [ -f "$f" ]; then
    cat "$f"
  else
    echo ""
  fi
}

VPS_KEY_CONTENT=$(get_file_content "${VPS_SSH_PRIVATE_KEY_FILE:-}" )
REPO_KEY_CONTENT=$(get_file_content "${REPO_SSH_PRIVATE_KEY_FILE:-}" )

set_if() {
  local name="$1" value="$2"
  if [ -n "$value" ]; then
    printf "%s" "$value" | gh secret set "$name" --repo "$GH_REPO"
    echo "Set $name"
  else
    echo "Skipping $name (no value)"
  fi
}

set_if VPS_SSH_PRIVATE_KEY "$VPS_KEY_CONTENT"
set_if VPS_HOST "${VPS_HOST:-}"
set_if VPS_USER "${VPS_USER:-}"
set_if VPS_DEPLOY_PATH "${VPS_DEPLOY_PATH:-}"
set_if VPS_SSH_PORT "${VPS_SSH_PORT:-}"
set_if REPO_SSH_PRIVATE_KEY "$REPO_KEY_CONTENT"

echo "All done. Check secrets at: https://github.com/$GH_REPO/settings/secrets/actions"
