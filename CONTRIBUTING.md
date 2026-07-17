# 🎇Contributing Guidelines

This documentation contains a set of guidelines to help you during the contribution process.

We welcome all contributions from anyone willing to add new scripts to this repository. Thank you for helping out — **no contribution is too small.**

---

## 💻Before Contributing

Welcome to [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule). Before sending your pull requests, make sure that you **read the whole guidelines**. If you have any doubt on the contributing guide, please feel free to reach out.

---

## 🙌Contribution

Any contribution is accepted, from fixing grammatical mistakes to implementing complex Python scripts. Please read this section if you are contributing your work.

---

## 🔖Steps to Contribute

1. **Fork the repo** and clone it on your machine:
   ```
   git clone https://github.com/<your-username>/ML-CaPsule.git
   ```

2. **Add an upstream link** to the main branch in your cloned repo:
   ```
   git remote add upstream https://github.com/Niketkumardheeryan/ML-CaPsule.git
   ```

3. **Keep your cloned repo up to date** by pulling from upstream (this also avoids merge conflicts):
   ```
   git pull upstream main
   ```

4. **Create your feature branch** (do not skip this step):
   ```
   git checkout -b <feature-name>
   ```

5. **Commit your changes** with a meaningful but concise message:
   ```
   git commit -m "Write a meaningful but small commit message"
   ```

6. **Push the changes** for review:
   ```
   git push origin <branch-name>
   ```

7. **Create a PR on GitHub.** Don't just hit the button — write a PR message to clarify why and what you are contributing.

### 💡What should I keep in mind while contributing?

## 🔨Note

> - Do not edit/delete someone else's code in this repository. You can only insert new files/folders.
> - Give a meaningful name to whatever file or folder you are adding. For example, if you have written a Python script for Hello World, then `hello_world.py` is a valid name.

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
