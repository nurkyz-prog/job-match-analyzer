# Job Match Analyzer

A small tool that compares a CV against a job description and reports how well
they match — built while applying for software engineering internships, to
solve a real problem: figuring out which of my own skills to highlight for a
specific posting.

## Problem

It's hard to judge, just by eye, how well a CV lines up with a specific job
description, or which existing skills are worth emphasizing for that role.

## Solution

A Streamlit app where you paste in CV text and a job description. It sends
both to Claude (Anthropic's LLM API) with a structured prompt, and displays:

- A match score (0–100)
- Skills from the CV that match the posting
- Skills the posting asks for that the CV doesn't show
- Suggestions on which existing skills to highlight more

## Tech Stack

- Python
- Streamlit (UI)
- Anthropic Claude API (analysis)

## How to Run

1. Install dependencies:
