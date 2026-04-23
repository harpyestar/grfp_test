# grfp-ui-test Project Skills

This directory contains project-specific skills designed to improve code quality and documentation consistency.

## Available Skills

### sync-project-docs-before-commits.md
**Use when:** About to commit code changes to git

This skill ensures that CLAUDE.md is updated with the current project structure and implementation status before every commit.

**What it does:**
- Scans the current directory structure
- Updates CLAUDE.md with new files, directories, and organization
- Updates the "已实现功能清单" (implementation checklist) with completed features
- Ensures documentation always reflects code reality

**Key sections in CLAUDE.md maintained by this skill:**
- `实际项目目录结构（已实现）` - Full directory tree
- `已实现功能清单` - Table of completed features with status badges

## How Skills Work

Project skills are automatically discovered and loaded by Claude Code. When you reference them (e.g., `/sync-project-docs-before-commits`), they'll be available to use.

## Adding New Skills

To add more skills to this project:

1. Create a new `.md` file in this directory
2. Follow the format of existing skills (YAML frontmatter + markdown content)
3. The skill will be auto-discovered on next session

## Conventions

- Use kebab-case for skill filenames
- Keep YAML frontmatter with `name` and `description` fields
- Description should start with "Use when..."
- Keep skills focused and reusable