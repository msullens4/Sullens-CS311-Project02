# USI Pathfinder

CS311 · 100 points · Due December 9, 2026 at 11:59 PM Central

Build a weighted campus graph, find shortest routes with Dijkstra, and handle closed connections. Read **Project 2 USI Pathfinder.pdf** for the requirements, rubric, and submission checklist.

## Start

Choose **Use this template** to create a repository under your own GitHub account, then clone your copy. Use Python 3.11 or later; no packages are needed.

- `pathfinder.py`: complete the graph and routing code here.
- `CampusMap.py`: the supplied campus data.
- `TestPathfinder.py`: the supplied tests.
- `RunCampus.py`: the schedule simulation and Final Token.

Keep the supplied map, tests, and simulator unchanged. The starter raises `NotImplementedError` until you complete `pathfinder.py`.

## Run

From the project folder:

```sh
python -m unittest -v TestPathfinder.py
python RunCampus.py
```

The simulator runs the tests and 10 schedules. After all checks pass, enter your own USI username to generate the Final Token.

## Submit

Push your completed code and documents to your own repository. In Blackboard, submit the repository URL, final commit SHA, and `v1.0-final` tag, along with the Final Token, screenshot, and raw terminal log from the same run. The handout lists the required documents.

## If you cloned the instructor repository

Create an empty repository under your own account. Replace the URL below with yours:

```sh
git remote rename origin upstream
git remote add origin <your-repository-url>
git remote -v
git branch --show-current
git push -u origin main
```

Check that `origin` points to your repository. Use your branch name if it differs from `main`.
