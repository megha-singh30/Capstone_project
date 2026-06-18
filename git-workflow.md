# Git Workflow — churn-prediction-service

A reference for the daily Git loop on this project. The goal: a commit/PR/branch
history that reads like a real production repo, not a tutorial dump.

## The daily loop

Repeat this once per day's work (or per logical chunk).

```bash
# 1. Start clean from an up-to-date main
git checkout main
git pull

# 2. New branch for today's work (name it meaningfully)
git checkout -b day-4-dockerize-training

# 3. Work, then commit — several small commits as you go
git add .                       # or: git add <specific files>
git commit -m "feat: add Dockerfile for training"

# 4. Push — first push sets upstream, then plain `git push`
git push -u origin day-4-dockerize-training
# ...keep committing + `git push` while you work...

# 5. On GitHub: open ONE Pull Request, review it, merge it

# 6. After merge — clean up
git checkout main
git pull                                            # pull merged work into local main
git branch -d day-4-dockerize-training              # delete local branch
git push origin --delete day-4-dockerize-training   # delete remote branch
```

## Branch policy

- **New branch every day.** One branch per logical unit of work. Never commit
  directly to `main`.
- **Name them meaningfully:** `day-5-fastapi-serving`, not `test` or `branch2`.
- **Delete after merge.** A merged branch is dead weight — the work is in `main`'s
  history now. GitHub shows a "Delete branch" button right after merge (handles the
  remote); then delete locally.
- **Use `-d`, not `-D`.** `git branch -d` refuses to delete an unmerged branch,
  which protects you from losing work. `-D` forces it — only use when you mean it.

## Commit messages — conventional commits

Prefix every commit so the history is scannable:

- `feat:` a new capability      → `feat: add /predict endpoint`
- `fix:`  a bug fix             → `fix: coerce TotalCharges to numeric`
- `chore:` tooling / setup      → `chore: add .dockerignore`
- `docs:` documentation         → `docs: write architecture trade-offs`
- `test:` tests                 → `test: cover feature/target split`
- `refactor:` restructure, no behavior change

## A PR tracks a branch, not a commit

Once a PR is open for a branch, **every new push to that branch shows up in the
same PR automatically.** So you never open a PR per commit — push as many times as
you want, open one PR when the branch's work is done. You can even open it early as
a *draft* and keep pushing into it.

Right granularity: **one PR per day**, several clean commits inside it. Not one PR
per commit (noise), not one giant PR for the whole month (unreviewable).

## Learning curve — staged, matched to the 30-day plan

1. **Now:** the daily loop above. Make it automatic.
2. **This week:** conventional commits + tight `.gitignore` discipline.
3. **Week 2:** branch protection on `main` (forces PRs, blocks direct pushes),
   GitHub Actions CI (tests run on every PR before merge), tags + releases
   (`v0.1.0`), GitHub Secrets.
4. **Later:** issues as a roadmap (open = todo, closed = shipped); squash-and-merge
   to keep `main` history tidy (collapses a branch into one clean commit, using your
   conventional-commit title as the headline).

## Don't

- Don't manufacture fake activity or backdate commits to look busy. It's detectable
  and reads worse than an honest history.
- Don't commit secrets (AWS keys, tokens) — ever. `.gitignore` them, use GitHub
  Secrets. This matters most in Week 3.
- Don't commit large binaries (model `.joblib`, datasets) — those belong in S3 /
  MLflow / artifact storage, not Git.
