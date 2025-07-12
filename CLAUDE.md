# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal GitHub profile repository for user "pi-dal". It contains:

- A profile README.md with introduction and snake contribution animation
- A GitHub Actions workflow that generates a snake eating contributions visualization

## GitHub Actions Workflows

The repository includes two workflows:

### 1. Snake Contribution Animation (`.github/workflows/snk.yml`)
- Runs every 6 hours via cron schedule
- Generates a snake animation consuming GitHub contributions
- Outputs files to a separate `output` branch
- Uses the Platane/snk action to create both GIF and SVG formats

### 2. Claude Code Integration (`.github/workflows/claude-code.yml`)
- Triggers when @claude is mentioned in issues, PRs, or comments
- Provides AI assistance for repository management and code tasks
- Requires `ANTHROPIC_AUTH_TOKEN` and `GITHUB_TOKEN` secrets
- Has permissions to write to contents, pull requests, and issues
- Includes GitHub MCP tools for PR reviews and interactions

## Repository Structure

This is a minimal profile repository with no development dependencies, build processes, or application code. The main content is the README.md profile page and the automated snake contribution visualization.

## Note

Since this is a profile repository without development code, there are no build commands, linting tools, testing frameworks, or architectural patterns to document.