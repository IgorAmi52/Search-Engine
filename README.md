# Search Engine

This is an open-source search engine project that uses the **PageRank algorithm** to return the best page results from a parsed PDF file. The project was developed during my **first-year Algorithm and Data Structures course**.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Introduction

The search engine aims to simulate how a web search engine works by analyzing the structure and content of a parsed PDF file. Using the **PageRank algorithm**, the search engine ranks pages based on the number and quality of links between them. A **graph** structure is used to store the relationships between pages, and a **trie structure** is employed for efficient word matching and retrieval.

---

## Features

- **PageRank Algorithm**: Ranks pages based on link quality and quantity.
- **Graph Structure**: Stores page content and links.
- **Trie Data Structure**: Maps words to the pages that match them.
- **PDF Parsing**: Converts PDF files into structured data.
- **Search Functionality**: Retrieves ranked pages based on query words.
- **Boolean Query Support**: Supports advanced query functionalities like `AND`, `OR`, `NOT`, and parentheses `()` for grouping terms.
- **Export Option**: Allows exporting the pages returned by a search query to a file for further analysis or review.

---

## Technologies Used

- **Programming Language**: Python
- **Libraries**: 
  - `pymupdf` for PDF parsing.

---

## Installation

### Using Conda (Recommended)

If you are using Conda to manage your environment, follow these steps:


1. Clone the repository:
   ```bash
   git clone https://github.com/IgorAmi52/Search-Engine.git
2. Navigate to the project directory:
   ```bash
   cd checkers-engine
3. Install the necessary dependencies:
   ```bash
   conda env create -f environment.yml
---

## Usage

- **Run the Project**:
   ```bash
   python main.py
---

## License

This project is licensed under the MIT License.
