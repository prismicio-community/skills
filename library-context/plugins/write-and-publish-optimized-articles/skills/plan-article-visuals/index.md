---
title: Plan Article Visuals
summary: Decide which sections of an article earn a visual, generate the diagrams and charts, and get a precise screenshot shot list.
description: A free AI skill that plans an article's visuals, draws diagrams and charts as SVG, and writes captions, alt text and a screenshot list.
categories: [content, design]
tags: [visuals, diagrams, charts, alt-text, screenshots, articles]
featured: false
draft: true
output: Diagram and chart files, captions and alt text, and a numbered shot list
platforms: [claude, claude-code]
requirements:
  - name: Code execution
    required: false
    details: Runs the skill's scripts to draw diagrams and charts. Without it, you get the specs and the shot list for someone else to produce.
examples:
  - prompt: What images does this article need?
    note: An audit of where a visual earns its place.
  - prompt: Make a diagram for the "How it works" section.
    note: One visual, drawn from the section's content.
---

The assistant reads an article, decides which sections a visual would make clearer, draws the diagrams and charts it can, and writes a precise shot list for screenshots, with captions that say what to notice and alt text that carries the same information.

## How it works

1. **Audits the draft** for the sections where a visual adds information, not decoration.
2. **Draws what can be drawn**: flows, comparisons and charts from real data, as SVG files.
3. **Specifies the rest**: every screenshot with its page, state, crop and annotation, so anyone can capture it.
4. **Writes captions and alt text** that say what the reader should notice.

## Setup

No setup is needed.

## What it is not

- **Not an image generator.** No photos, illustrations or stock imagery.
- **Not a screenshot tool.** Screenshots come as a shot list.
