# 🎇 Contributing Guidelines

[🏠 Main README](README.md) • [📖 Code of Conduct](CODE_OF_CONDUCT.md) • [🗺️ Learning Roadmap](ROADMAP.md) • [📋 Project README Template](.github/readme_template.md) • [🔀 PR Template](.github/pullrequest_template.md)

This documentation contains a set of guidelines to help you during the contribution process.

We welcome all contributions from anyone willing to add new scripts or refine projects in this repository. Thank you for helping out — **no contribution is too small.**

---

## 💻 Local Environment Setup

Before contributing, set up a isolated Python development environment to ensure clean dependencies.

```bash
# 1. Clone your fork
git clone https://github.com/<your-username>/ML-CaPsule.git
cd ML-CaPsule

# 2. Create and activate a virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python -m venv venv
source venv/bin/activate

# 3. Install core dependencies & Jupyter Notebook
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn scikit-learn jupyter notebook
```

---

## 🙌 Contribution Scope

Any contribution is accepted, from fixing documentation typos to implementing complex Machine Learning models, Deep Learning architectures, NLP pipelines, and Computer Vision solutions.

---

## 🔖 Step-by-Step Contribution Workflow

1. **Fork the repo** and clone it on your local machine:
   ```bash
   git clone https://github.com/<your-username>/ML-CaPsule.git
   ```

2. **Add an upstream link** to track changes from the main repository:
   ```bash
   git remote add upstream https://github.com/Niketkumardheeryan/ML-CaPsule.git
   ```

3. **Keep your repo up to date** by syncing with `upstream`:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

4. **Create a descriptive feature branch** (do not work directly on `main`):
   ```bash
   # Branch Naming Conventions:
   #   feature/<feature-name> (for new ML project / feature)
   #   fix/<bug-name>         (for bug fixes)
   #   docs/<doc-name>        (for documentation improvements)
   git checkout -b feature/heart-disease-predictor
   ```

5. **Commit your changes** with clear, imperative commit messages:
   ```bash
   # Format: <type>: <short summary>
   git commit -m "docs: improve project structure section in CONTRIBUTING.md"
   ```

6. **Push the branch** to your fork:
   ```bash
   git push origin feature/heart-disease-predictor
   ```

7. **Create a Pull Request on GitHub**:
   Follow the provided [.github/pullrequest_template.md](.github/pullrequest_template.md) template, link the corresponding issue (`Closes #issue_number`), and attach screenshots/results.

---

## 🏗️ Project Structure Expectations for New Submissions

When adding a new project directory to `ML-CaPsule`, ensure it contains:
1. **Descriptive Folder Name**: Use clear names (e.g., `Heart_Disease_Prediction`).
2. **Standardized README.md**: Follow the structure in [.github/readme_template.md](.github/readme_template.md).
3. **Executable Notebook (`.ipynb`)**: Clear outputs, code comments, and visualizations.
4. **Visual Demonstrations**: Screenshots, output tables, or confusion matrices stored in an `assets/` or `images/` folder inside the project directory.

---

## 🔨 Repository Rules & Best Practices

> - Do not edit/delete someone else's code unless explicitly fixing a bug or improving performance.
> - Avoid duplicate projects; check existing directories or [ROADMAP.md](ROADMAP.md) before starting.
> - Maintain clean snake_case file names for scripts (e.g., `model_training.py`).

---

## 🎗Coding Style

We want your work to be readable by others; therefore, we encourage you to note the following:

- Follow [PEP 8](https://pep8.org/) guidelines.
- Please write in Python 3.7+. `print()` is a function in Python 3, so `print "Hello"` will _not_ work but `print("Hello")` will.
- Focus on naming of functions, classes, and variables. Use **descriptive names** to reduce the need for redundant comments.
  - Follow the [Python Naming Conventions](https://pep8.org/#prescriptive-naming-conventions): `variable_names` and `function_names` should be lower_case, `CONSTANTS` in UPPERCASE, `ClassNames` should be CamelCase, etc.
- Prefer `.ipynb` files over `.py` files.
- Add a proper `README.md` with headings and results (screenshots, recorded videos).
- Code must be properly documented.

---

## 🤖 Automated Quality Checks (CI)

Every pull request targeting `main` / `master` is checked automatically by **GitHub Actions**
(`.github/workflows/pr_quality_check.yml`). The checks look **only at the files your PR
changed**, so pre-existing issues elsewhere in the repository never block your contribution.

### What gets checked

**🐍 Python files (`.py`)**

| Check | Tool | Catches | Blocks the PR? |
|-------|------|---------|:--------------:|
| Syntax errors | `py_compile` | Invalid Python that will not even import | ✅ Yes |
| PEP8 style | `flake8` | Indentation, spacing, naming, line length (max 120) | ❌ Advisory |

**📓 Notebooks (`.ipynb`)** — `.github/scripts/check_notebooks.py`

| Check | Catches | Blocks the PR? |
|-------|---------|:--------------:|
| Valid notebook JSON | Corrupt or truncated files | ✅ Yes |
| Committed error outputs | A saved traceback, meaning the notebook was committed while failing | ✅ Yes |
| Local absolute paths | `/Users/you/...` or `C:\Users\you\...`, which will not exist for anyone else | ❌ Advisory |
| Large notebooks | Bulky embedded outputs that bloat every clone | ❌ Advisory |
| No code cells | A notebook that contains only prose | ❌ Advisory |

This is separate from the existing **Notebook Health Check**, which *executes* changed
notebooks. These checks read the file without running it.

### Where results appear

Findings show up as **inline annotations on your diff** and in the **job summary** on the
Actions tab. Results are not posted as a PR comment, because a pull request opened from a
fork gets a read-only token, so a bot comment would fail for most contributors.

### Running the checks locally

```bash
pip install flake8

flake8 path/to/your_file.py                       # PEP8, uses the repo's .flake8
python -m py_compile path/to/your_file.py         # syntax
python .github/scripts/check_notebooks.py --changed-files your_notebook.ipynb
```

To check everything you changed against `master`:

```bash
git diff --name-only --diff-filter=ACM master...HEAD | grep '\.py$'    | xargs -r flake8
git diff --name-only --diff-filter=ACM master...HEAD | grep '\.ipynb$' \
  | xargs -r python .github/scripts/check_notebooks.py --changed-files
```

---

## 🔑Guidelines

1. Welcome to this repository, if you are here as an open source program participant/contributor.
2. Participants/contributors have to **comment** on issues they would like to work on, and mentors or the PA will assign you.
3. Issues will be assigned on a **first-come, first-serve basis.**
4. Participants/contributors can also **open their issues** using [issue_template](https://github.com/Niketkumardheeryan/ML-CaPsule/tree/main/.github/issue_template), but it needs to be verified and labeled by a mentor or PA. Please discuss with the team before opening your issues.
5. When you raise an issue, make sure you get it assigned to you before you start working on it.
6. Each participant/contributor will be **assigned 1 issue (max)** at a time to work on.
7. Participants are expected to follow **project guidelines** and [**coding style**](https://pep8.org/). **Structured code** is a top priority.
8. Try to **explain your approach** to solve any issue in the comments. This increases the chances of being assigned.
9. Don't create issues that are **already listed**.
10. Don't pick up an issue already assigned to someone else. Work on issues only after they are **assigned to you**.
11. Make sure you **discuss issues** before starting work.
12. Pull requests will be merged after being **reviewed** by a mentor or PA.
13. It might take **a day or two** to review your pull request. Please have patience.
14. Always create a pull request from a **branch** other than `main`.
15. Participants/contributors have to complete issues before the decided deadline. If you fail to make a PR within the deadline, the issue will be reassigned.
16. While making PRs, don't forget to **add a description** and **screenshots** of your work.
17. Include the issue number (`Fixes: #issue_number`) in your commit message while creating a pull request.
18. Make sure your solution is better in terms of performance and other parameters compared to the previous work.
19. We all are here to learn. You are allowed to make mistakes — that's how you learn.

---

## 🧲Pull Requests Review Criteria

1. Fill the **[PR Template](https://github.com/Niketkumardheeryan/ML-CaPsule/blob/main/.github/pullrequest_template.md)** properly while making a Pull Request.
2. You must add your `.ipynb` file into the respective **folders**.
3. Your work must be original, written by you — not copied from other resources.
4. Comment your code where necessary.
5. Follow the proper [style guides](https://google.github.io/styleguide/) for your work.
6. For any queries or discussions, please feel free to drop a message.

---

## 📍Other points to remember while submitting your work

- Create a folder with a meaningful name (e.g., if submitting a Digital Clock project, name the folder "Digital Clock" and the file `digital_clock.ipynb`).
- File extension for code should be `.ipynb`.
- Strictly use snake_case (underscore_separated) in your file names, as it will be easier to parse using scripts.
- Avoid creating new directories if possible. Try to fit your work into the existing directory structure. Contact maintainers before creating new ones.
- The [README.md](https://github.com/Niketkumardheeryan/ML-CaPsule/blob/main/.github/readme_template.md) file should be concise and clear about what the project does.
- Include screenshots — this is required.
- If you have modified/added code, make sure it compiles before submitting.
- If you have modified/added documentation, ensure your language is concise and contains no grammar errors.

---

## 📖Resources

**Markdown** — A lightweight markup language with plain text formatting syntax:
- [Markdown Cheat-Sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

**Git** — A distributed version-control system for tracking changes in source code:
- [Videos to get started](https://www.youtube.com/watch?v=xAAmje1H9YM&list=PLeo1K3hjS3usJuxZZUBdjAcilgfQHkRzW)
- [Cheat Sheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)

---

## 🤔Need more help?

Refer to the following articles on basics of Git and GitHub:
- [Forking a Repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
- [Cloning a Repo](https://help.github.com/en/desktop/contributing-to-projects/creating-an-issue-or-pull-request)
- [How to create a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
- [Getting started with Git and GitHub](https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6)
- [Learn GitHub from Scratch](https://lab.github.com/githubtraining/introduction-to-github)

## 😇Tip from me
It always takes time to understand and learn. So, do not worry at all. You can do this**!💪


🎉 🎊 😃 Happy Contributing 😃 🎊 🎉

---

## Issue Labels Guide

To improve issue organization and contributor onboarding, the repository follows a standardized labeling system.

### Common Labels

| Label | Purpose |
|-------|---------|
| good first issue | Suitable for beginners |
| beginner friendly | Easy tasks for new contributors |
| bug | Something is not working correctly |
| documentation | Documentation improvements or fixes |
| enhancement | Improvement to existing features |
| feature request | Suggestion for a new feature |
| help wanted | Maintainers are seeking contributions |
| duplicate | Issue already exists |
| invalid | Not a valid issue or request |
| priority: low | Low priority task |
| priority: medium | Medium priority task |
| priority: high | High priority task |

### Why Labels Matter

- Helps contributors identify suitable tasks
- Improves issue discoverability
- Simplifies project management
- Enhances contributor experience during open-source programs like GSSoC
