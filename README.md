# Business Contract Validation

## Overview

Business Contract Validation is a web-based application designed to assist users in uploading and analyzing business contract PDFs. The application parses the text within the contracts, identifies named entities, and provides a highlighted version of the contract for easy reference. This tool is particularly useful for legal professionals and businesses to validate and review contracts efficiently.

## Features

- **PDF Upload**: Upload business contract PDFs directly through the web interface.
- **Text Parsing**: Extract and display the text content of the uploaded PDF.
- **Named Entity Recognition**: Identify and list key entities such as parties involved, dates, monetary values, locations, legal terms, and products/services.
- **Highlighted PDF**: Download a highlighted version of the PDF with important entities marked for quick reference.

## Technologies Used

- **Frontend**: HTML, CSS, Bootstrap, JavaScript, jQuery
- **Backend**: Flask (Python)
- **PDF Processing**: pdfplumber (Python library)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- Flask
- pdfplumber

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/business-contract-validation.git
