# Push this completed solution to GitHub

The ChatGPT GitHub connector is currently unable to push repository contents directly, so use the local Git history created for this submission.

## 1. Open Terminal

```bash
cd /path/to/incubyte-data-craftsperson
```

## 2. Set your Git identity once

Use the same name/email you normally use for GitHub:

```bash
git config user.name "Your GitHub name"
git config user.email "Your GitHub email"
```

## 3. Add the GitHub remote

```bash
git remote add origin https://github.com/shikhabansal7/incubyte-data-craftsperson.git
```

If a remote already exists:

```bash
git remote set-url origin https://github.com/shikhabansal7/incubyte-data-craftsperson.git
```

## 4. Push the commits

```bash
git branch -M main
git push -u origin main
```

Authenticate with GitHub when prompted.

## 5. Verify

Open the repository and confirm that the history contains the incremental assessment commits.

Do not squash the commits: the assessment explicitly asks for incremental commits so the reviewer can understand how the solution evolved.
