# Chatbot safety analysis

[![arXiv](https://img.shields.io/badge/arXiv-2407.04915-b31b1b.svg)](https://arxiv.org/abs/2407.04915)
[![License](https://img.shields.io/github/license/DigitalHarborFoundation/chatbot-safety)](https://github.com/DigitalHarborFoundation/chatbot-safety/blob/main/LICENSE)

This repository contains analysis code and figures for ["Safe Generative Chats in a WhatsApp Intelligent Tutoring System"](https://arxiv.org/abs/2407.04915). In addition, a reference moderation system using OpenAI's Moderation API is provided in `src/student_guardrails`.

If this work is useful to you in any way, please cite the corresponding paper:

>Zachary Levonian, Owen Henkel. [Safe Generative Chats in a WhatsApp Intelligent Tutoring System]((https://arxiv.org/abs/2407.04915)). _Educational Data Mining (EDM) Workshop: Leveraging Large Language Models for Next Generation Educational Technologies_. 2024.

## Development

Primary code contributor:

 - Zachary Levonian (<zach@levi.digitalharbor.org>)

## Local development setup

This project uses `make` and `Poetry` to manage and install dependencies.

On Windows, you'll need to use WSL and maybe make some other changes.

### Python development

Use `make install` to install all needed dependencies (including the pre-commit hooks and Poetry).

You'll probably need to manually add Poetry to your PATH, e.g. by updating your `.bashrc` (or relevant equivalent):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Run tests

```bash
make test
```

### Run Jupyter Lab

```bash
make jupyter
```

Which really just runs `poetry run jupyter lab`, so feel free to customize your Jupyter experience.

### Other useful commands

 - `poetry run <command>` - Run the given command, e.g. `poetry run pytest` invokes the tests.
 - `poetry add <package>` - Add the given package as a dependency. Use flag `-G dev` to add it as a development dependency.
