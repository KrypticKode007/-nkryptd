#!/usr/bin/env bash
# Safe helper: initialize Git in this directory without deleting files or branches.
set -Eeuo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
if [ -e .git ]; then
  echo "Git repository already exists; refusing to overwrite it." >&2
  exit 1
fi
git init -b main
git config user.name "${GIT_AUTHOR_NAME:-nkryptd maintainer}"
git config user.email "${GIT_AUTHOR_EMAIL:-nkryptd-maintainer@users.noreply.github.com}"
printf 'main\n' > branches/active-branch.txt
git add .
git commit -m "build: initialize repaired nkryptd repository"
git checkout -b 9999.99-actuator
printf '9999.99-actuator\n' > branches/active-branch.txt
git add branches/active-branch.txt
git commit -m "feat(actuator): activate concurrent processing branch"
git checkout main
git checkout -b incognito-gateway
printf 'incognito-gateway\n' > branches/active-branch.txt
git add branches/active-branch.txt
git commit -m "feat(gateway): activate WebSocket transport branch"
git checkout main
echo "Initialized main, 9999.99-actuator, and incognito-gateway."
