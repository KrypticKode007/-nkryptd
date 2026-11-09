# Publish the repaired code to the existing GitHub repository

The repaired branches are prepared locally, but this session does not have authenticated write access to GitHub. The repository identified in your runner notes is `KrypticKode007/-nkryptd`.

## Recommended: preserve the existing Git history

1. Download and extract `nkryptd-fixed-source.zip`.
2. Clone your existing repository and make a backup first:

   ```bash
   git clone https://github.com/KrypticKode007/-nkryptd.git nkryptd
   cp -a nkryptd nkryptd-backup
   ```

3. Copy the contents of the extracted `nkryptd-fixed/` folder over the clone (do not copy `.git`, `.env`, or runtime `data/`). Remove obsolete files that are no longer part of the repaired project, including the old `proof_of_execution.py` transcript and the old runner-token instructions.
4. On each branch, commit and push the updated files:

   ```bash
   cd nkryptd
   git checkout main
   # Copy the repaired source files into this working tree.
   printf 'main\n' > branches/active-branch.txt
   git add -A && git commit -m "fix: repair nkryptd core and deployment"
   git push origin main

   git checkout 9999.99-actuator
   # Copy the same repaired source files into this working tree.
   printf '9999.99-actuator\n' > branches/active-branch.txt
   git add -A && git commit -m "fix: repair nkryptd actuator branch"
   git push origin 9999.99-actuator

   git checkout incognito-gateway
   # Copy the same repaired source files into this working tree.
   printf 'incognito-gateway\n' > branches/active-branch.txt
   git add -A && git commit -m "fix: repair nkryptd WebSocket gateway branch"
   git push origin incognito-gateway
   ```

If a branch does not exist on GitHub yet, create it from `main` with `git checkout -b <branch>` before copying the repaired files. Do not force-push over existing history unless you intentionally want to replace it.

## Alternative: use the supplied Git bundle for a new/empty remote

`nkryptd-all-branches.bundle` contains the repaired local Git history and all three branches. It is suitable for creating a new repository or an empty GitHub remote. Do not push this unrelated history over your existing repository without first deciding how to preserve or replace its history.

```bash
git clone nkryptd-all-branches.bundle nkryptd
cd nkryptd
git remote add origin https://github.com/KrypticKode007/-nkryptd.git
git push -u origin main 9999.99-actuator incognito-gateway
```

Use your normal Git credential manager or SSH key when prompted. Never paste a personal access token or runner registration token into chat or commit one to Git.
