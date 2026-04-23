---
name: sync-project-docs-before-commits
description: Use when about to commit code changes to git and have added files, changed project structure, or completed new features - ensures CLAUDE.md is updated with current state before pushing
---

# Sync Project Docs Before Commits

## Overview

This skill ensures that before any git commit, the project documentation (CLAUDE.md) reflects the current project state, including directory structure and newly completed features. This prevents documentation drift and maintains an accurate record of implementation progress.

**Core principle:** Documentation must always mirror code reality - commit the documentation update along with the implementation.

## When to Use

Use this skill BEFORE running `git commit` when:

- You've added new test files or pages (POM classes)
- You've created new utilities or helper functions
- You've reorganized directory structure
- You've completed a feature or test case
- You've modified existing implementation

**Symptoms indicating you need this skill:**
- You're about to commit code
- Project structure has changed since last commit
- You completed a new feature or test
- CLAUDE.md hasn't been updated this session
- You have uncommitted documentation updates pending

## Quick Reference: Pre-Commit Workflow

```
1. Run: git status
   ↓ Check what files have changed
   
2. Scan current directory structure
   ↓ Find new files/directories
   
3. Update CLAUDE.md sections:
   ├─ "实际项目目录结构" - add new files/paths
   ├─ "已实现功能清单" - add completed features with ✅
   └─ Update status badges
   
4. Review changes:
   ├─ Verify new items appear in tree
   ├─ Check spelling and formatting
   └─ Confirm all features are listed
   
5. Stage documentation:
   ↓ git add CLAUDE.md
   
6. Commit with semantic message:
   ↓ git commit -m "docs: update structure and implementation status"
   
7. Verify commit includes both code and docs:
   ↓ git log -1 --stat
```

## Implementation Steps

### Step 1: Identify Changes

```bash
# See all changes since last commit
git status

# See file additions/modifications
git diff --name-status

# Get detailed directory tree for current state
find . -not -path './.venv/*' -not -path './.pytest_cache/*' \
  -not -path './__pycache__/*' -not -path '*/__pycache__/*' \
  -not -path './.git/*' -type f | sort
```

### Step 2: Update Directory Structure

In CLAUDE.md, update the "实际项目目录结构（已实现）" section:

**Rules:**
- Indent with 4 spaces per level (consistency)
- Use `├── ` for regular items, `└── ` for last item in a group
- Add `__init__.py` files explicitly
- Mark files with ✅ if they're implemented (have code)
- Add brief comment explaining new files
- Remove files that are deleted
- Reorganize alphabetically within each level when structure changes

**Example addition:**
```
├── pages/
│   └── operate/
│       └── rfp_management/
│           ├── __init__.py
│           ├── create_rfp_project_page.py  # ✅ RFP 项目创建页 POM
│           └── bidding_analysis_page.py    # ✅ [NEW] 评标分析页面
```

### Step 3: Update Implementation Checklist

In CLAUDE.md, update "已实现功能清单" table:

**For completed features:**
- Add status: ✅ 
- Add brief description: what was implemented
- Example: `| RFP 项目创建 | ✅ | create_rfp_project_page.py + test_create_rfp_project.py |`

**For refactored code:**
- Mark as ✅ with description: `| POM 元素定位集中管理 | ✅ | 定位器在顶部集中定义，方法中复用 |`

**For newly discovered files:**
- Add entries explaining their purpose
- Cross-reference with directory tree above

### Step 4: Review and Verify

Checklist before committing:

- [ ] All new .py files listed in directory structure
- [ ] New directories properly indented with correct symbols (├─/└─)
- [ ] All new features added to "已实现功能清单"
- [ ] Checkmarks (✅) correctly placed
- [ ] No duplicate entries
- [ ] Comments are accurate and up-to-date
- [ ] No spelling errors
- [ ] Formatting is consistent with existing structure

### Step 5: Commit Documentation

```bash
# Stage only CLAUDE.md updates if you want separate commit
git add CLAUDE.md

# Or include with other changes
git add .
```

**Commit message format:**

```
# For pure documentation updates:
git commit -m "docs: update project structure and implementation status"

# For docs + code changes together:
git commit -m "feat: implement bidding analysis page

- Add create_rfp_project_page.py for RFP project creation
- Add test cases for project creation flow
- Update CLAUDE.md with new structure and features"
```

## Common Mistakes

### ❌ Forgetting to Update CLAUDE.md
**Reality:** Documentation becomes stale immediately. Future work references outdated info.
**Fix:** Make CLAUDE.md update a required step before EVERY commit.

### ❌ Only Updating Directory Tree, Not Feature List
**Reality:** Structure looks current but feature status is unclear.
**Fix:** Update BOTH "实际项目目录结构" AND "已实现功能清单" sections together.

### ❌ Inconsistent Formatting
**Reality:** Tree structure becomes messy and hard to read.
**Fix:** Use 4-space indents, consistent symbols (├──/└──), comment every .py file.

### ❌ Not Removing Deleted Files from CLAUDE.md
**Reality:** Documentation references files that no longer exist.
**Fix:** When deleting code, immediately remove corresponding entries from CLAUDE.md.

### ❌ Misplacing ✅ Marks
**Reality:** Feature looks complete but test file is missing.
**Fix:** Only mark ✅ when BOTH page.py (POM) AND test_*.py files exist.

### ❌ Vague Feature Descriptions
**Reality:** "Updated code" doesn't explain what was done.
**Fix:** Be specific: "Added parameterized test data loading", "Centralized element locators in POM class".

## Automation Hooks (Optional)

You can configure a git pre-commit hook to remind you before committing:

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
echo "⚠️  REMINDER: Did you update CLAUDE.md?"
echo "   - Check 'git status' for modified files"
echo "   - Add new files to directory structure"
echo "   - Update 已实现功能清单 with completed features"
echo ""
echo "Proceed with commit? (y/n)"
read response
[ "$response" != "y" ] && exit 1
exit 0

# Make it executable
chmod +x .git/hooks/pre-commit
```

## Related Skills

**REQUIRED BACKGROUND:** This skill assumes you know basic git workflow - see your team's git guidelines for commit message conventions.

## Success Criteria

A successful pre-commit workflow following this skill:

1. ✅ CLAUDE.md shows all new files/directories added
2. ✅ All completed features listed in "已实现功能清单"
3. ✅ Directory tree is current and properly formatted
4. ✅ Git commit includes both code changes and documentation update
5. ✅ Future Claude instances can read CLAUDE.md to understand current project state