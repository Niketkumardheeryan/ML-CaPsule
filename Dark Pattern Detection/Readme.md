# Dark Pattern Detection in E-commerce Websites

## Overview

Dark patterns are deceptive design techniques used in user interfaces that trick users into doing things they might not otherwise do. These can include making unintended purchases, subscribing to services, or sharing more personal information than intended. This project aims to detect such dark patterns on e-commerce websites by analyzing text extracted from website screenshots.

## Table of Contents

1. [What Are Dark Patterns?](#what-are-dark-patterns)
2. [Why Are Dark Patterns Important?](#why-are-dark-patterns-important)
3. [Project Description](#project-description)
4. [How It Works](#how-it-works)
5. [Detected Dark Patterns](#detected-dark-patterns)
6. [Installation](#installation)
7. [Usage](#usage)


## What Are Dark Patterns?

Dark patterns are tricks used in websites and apps that make you do things that you didn't mean to, like buying or signing up for something. These deceptive designs exploit cognitive biases and are typically aimed at benefiting the business at the expense of the user experience.

### Common Types of Dark Patterns

- **Sneak into Basket**: Adding items to a shopping cart without the user's consent.
- **Roach Motel**: Making it easy to get into a situation (like a subscription) but hard to get out.
- **Privacy Zuckering**: Tricking users into sharing more information than they intended.
- **Hidden Costs**: Revealing extra charges only at the last step of the checkout process.
- **Bait and Switch**: Advertising one thing and then delivering another.
- **Confirmshaming**: Guilt-tripping users into opting into something.
- **Forced Continuity**: Making it hard to cancel a service or subscription after a free trial ends.

## Why Are Dark Patterns Important?

Understanding and detecting dark patterns is crucial because:

- **User Trust**: Dark patterns erode user trust and can lead to negative brand perception.
- **Legal Compliance**: Many regions have regulations against deceptive practices, and failure to comply can result in legal consequences.
- **User Experience**: A fair and transparent user experience promotes user satisfaction and loyalty.

## Project Description

This project provides a tool to detect dark patterns on e-commerce websites by taking screenshots, extracting text using OCR (Optical Character Recognition), and analyzing the text for keywords associated with dark patterns.

## How It Works

1. **Take Screenshots**: The tool navigates the e-commerce website and captures multiple screenshots.
2. **Extract Text**: Text is extracted from these screenshots using Tesseract OCR.
3. **Analyze Text**: The extracted text is analyzed for the presence of dark pattern keywords.
4. **Report Findings**: The tool outputs a report of detected dark patterns based on keyword occurrences.

## Detected Dark Patterns

The algorithm currently detects the following types of dark patterns based on specific keyword groups:

1. **Sneak into Basket**: Phrases like "added to your cart" without user action.
2. **Roach Motel**: Terms indicating difficulty in canceling services, such as "cannot cancel" or "must call to cancel".
3. **Privacy Zuckering**: Keywords indicating forced information sharing, like "must provide email".
4. **Hidden Costs**: Phrases like "additional charges" or "extra fees".
5. **Bait and Switch**: Keywords such as "terms may change" or "substitute item".
6. **Confirmshaming**: Phrases like "are you sure?" with guilt-tripping language.
7. **Forced Continuity**: Keywords indicating automatic renewals, such as "auto-renew" or "subscription renewal".

Example keywords and phrases detected by the algorithm:
- "40% off", "50% off", "sale", "80% off", "70% off", "discount code", "clearance sale", "limited time offer".

## installation
Clone the repository
->  git clone 
-> cd Dark Pattern Detection

## Usage   
1. Update the url_to_analyze variable in the script with the URL of the e-commerce website you want    to  analyze.
2. run this command in terminal
   ```bash
   python scrapp_ocr_csv.py

## Example output   
   ```python 
   Extracted Text from screenshot 1:
    ... (extracted text) ...

    Dark Patterns Detected in screenshot 1:
    40% off: 2 occurrences
    sale: 1 occurrence
    ...

    Extracted Text from screenshot 2:
    ... (extracted text) ...

    Dark Patterns Detected in screenshot 2:
    limited time offer: 1 occurrence
    ...


    Dark Patterns Detected in screenshot 1:
    40% off: 2 occurrences
    sale: 1 occurrence
    ...

    Extracted Text from screenshot 2:
    ... (extracted text) ...

    Dark Patterns Detected in screenshot 2:
    limited time offer: 1 occurrence
    ...

   
