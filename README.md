# Chatbot safety: designing safe tutoring systems

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.14751365-blue.svg)](https://doi.org/10.5281/zenodo.14751365)
[![arXiv](https://img.shields.io/badge/arXiv-2407.04915-b31b1b.svg)](https://arxiv.org/abs/2407.04915)
[![License](https://img.shields.io/github/license/DigitalHarborFoundation/chatbot-safety)](https://github.com/DigitalHarborFoundation/chatbot-safety/blob/main/LICENSE)

> [!NOTE]
> This repository was archived in October 2026 and is now read-only.

This repository contains analysis code and figures for the research paper ["Designing Safe and Relevant Generative Chats for Math Learning in Intelligent Tutoring Systems"](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/840), published in the _Journal of Educational Data Mining_.
It extends our earlier workshop paper, ["Safe Generative Chats in a WhatsApp Intelligent Tutoring System"](https://arxiv.org/abs/2407.04915).

In addition, we include a reference moderation system using OpenAI's Moderation API in `src/student_guardrails`.
This system is usable as-is, but should mostly be useful as a reference. Features:
 - OpenAI Moderation API interface appropriate for both human-written and LLM-generated messages, including custom, per-category moderation thresholds.
 - Banned word lists that supercede OpenAI moderation scores.
 - Email alerting system using [SendGrid](https://github.com/sendgrid/sendgrid-python) for messages in particular categories.
 - Pre-written moderation responses designed for users of the WhatsApp-based chatbot [Rori](https://rori.ai).
 - Unit tests that provide mocked interfaces to the OpenAI Moderation API and the SendGrid API.

If this work is useful to you in any way, please cite the journal paper:

>Levonian, Z., Henkel, O., Li, C., & Postle, M.-E. (2025). [Designing Safe and Relevant Generative Chats for Math Learning in Intelligent Tutoring Systems](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/840). _Journal of Educational Data Mining_, 17(1), 66-97. https://doi.org/10.5281/zenodo.14751365

```bibtex
@article{levonian2025designing,
  title   = {Designing Safe and Relevant Generative Chats for Math Learning in Intelligent Tutoring Systems},
  author  = {Levonian, Zachary and Henkel, Owen and Li, Chenglu and Postle, Millie-Ellen},
  journal = {Journal of Educational Data Mining},
  volume  = {17},
  number  = {1},
  pages   = {66--97},
  year    = {2025},
  doi     = {10.5281/zenodo.14751365},
  url     = {https://jedm.educationaldatamining.org/index.php/JEDM/article/view/840}
}
```

The earlier workshop paper:

>Zachary Levonian, Owen Henkel. [Safe Generative Chats in a WhatsApp Intelligent Tutoring System](https://arxiv.org/abs/2407.04915). _Educational Data Mining (EDM) Workshop: Leveraging Large Language Models for Next Generation Educational Technologies_. 2024.

```bibtex
@inproceedings{levonian2024safe,
  title     = {Safe Generative Chats in a {WhatsApp} Intelligent Tutoring System},
  author    = {Levonian, Zachary and Henkel, Owen},
  booktitle = {Educational Data Mining (EDM) Workshop: Leveraging Large Language Models for Next Generation Educational Technologies},
  year      = {2024},
  eprint    = {2407.04915},
  archivePrefix = {arXiv},
  url       = {https://arxiv.org/abs/2407.04915}
}
```

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

Note: `notebooks/AnalyzeStudentUsage.ipynb` depends on private Rori data and the internal `rori-orm` package, so it can't be re-run outside of Rori. It's included for reference, with outputs preserved.

### Other useful commands

 - `poetry run <command>` - Run the given command, e.g. `poetry run pytest` invokes the tests.
 - `poetry add <package>` - Add the given package as a dependency. Use flag `-G dev` to add it as a development dependency.
