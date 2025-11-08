#!/usr/bin/env bash
set -euo pipefail

# setup-ubuntu.sh
# Idempotent script to prepare an Ubuntu LTS server for deploying this project with Docker Compose.
# Usage on the server (as root or sudo):
#   sudo bash setup-ubuntu.sh deploy
# Where the single argument is the deploy username to create (e.g. 'deploy').

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <deploy-user> [public-key-file]"
  exit 1
fi

DEPLOY_USER="$1"
PUBKEY_FILE="${2:-}"  # optional path to a public key to add to the deploy user's authorized_keys

echo "Preparing Ubuntu server for deploy user: ${DEPLOY_USER}"

apt update -y
apt upgrade -y

apt install -y ca-certificates curl gnupg lsb-release git

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update -y
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Docker installed. Enabling service..."
systemctl enable --now docker

if id "${DEPLOY_USER}" &>/dev/null; then
  echo "User ${DEPLOY_USER} already exists"
else
  echo "Creating user ${DEPLOY_USER}"
  useradd -m -s /bin/bash "${DEPLOY_USER}"
fi

mkdir -p "/home/${DEPLOY_USER}/.ssh"
chown "${DEPLOY_USER}:" "/home/${DEPLOY_USER}/.ssh"
chmod 700 "/home/${DEPLOY_USER}/.ssh"

if [ -n "${PUBKEY_FILE}" ] && [ -f "${PUBKEY_FILE}" ]; then
  echo "Adding provided public key to authorized_keys"
  cat "${PUBKEY_FILE}" >> "/home/${DEPLOY_USER}/.ssh/authorized_keys"
  chown "${DEPLOY_USER}:" "/home/${DEPLOY_USER}/.ssh/authorized_keys"
  chmod 600 "/home/${DEPLOY_USER}/.ssh/authorized_keys"
fi

echo "Adding ${DEPLOY_USER} to docker group"
usermod -aG docker "${DEPLOY_USER}"

echo "Setup complete. Verifying docker access for ${DEPLOY_USER}..."

# verify that the deploy user can run docker compose
if su -l "${DEPLOY_USER}" -c 'docker compose version' >/dev/null 2>&1; then
  echo "OK: ${DEPLOY_USER} can run 'docker compose'"
else
  echo "Warning: ${DEPLOY_USER} cannot run 'docker compose' without re-login. The user may need to re-login or the session needs a restart."
  echo "You can force a new group session by running: 'newgrp docker' or logging out and back in."
fi

echo "You can now SSH as ${DEPLOY_USER} and run:"
echo "  git clone https://github.com/<owner>/<repo>.git /var/www/faceit-ai-bot"
echo "  cd /var/www/faceit-ai-bot && docker compose up -d --build"

exit 0
