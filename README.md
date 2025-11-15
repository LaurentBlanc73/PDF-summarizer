# PDF-summarizer
A Webapplication that allows for uploading and summarizing PDF files. 

This repository contains the the development of the language model for summarizing the PDFs, example patent files and the frontend which includes a UI.
The language model itself is hosted on Hugging Face and was finetuned using the dataset `cnn_dailymail`.
The backend features two post-functions. 
The first function takes the through dash uploaded pdf, extracts and cleans the text. 
The second function calls the finetuned language model and summarizes a given text (which is in this case the result of the first api function).

The API base url and key are managed by environment variables as they are sensitive information. The `.env.template` serves as a blueprint for the necessary variables.

## Project structure

```bash
PDF-summarizer
├── .github/workflows/      # GitHub Actions CI workflow for running tests
├── example_pdfs/           # collection of sample PDFs for testing the application
├── model_development/      # notebooks for fine-tuning and evaluating the model
└── summarizer_app/         # source code for the web application
    ├── frontend/           # functions and classes
    │   └── assets/         # assets of the frontend
    ├── .env.template       # template for .env file
    ├── Dockerfile          # instructions for building Docker image
    ├── requirements.txt    # python dependencies
    ├── run.py              # application entry point for local development
    └── wsgi.py             # WSGI entry point for production servers
```

## Getting started

### Clone the repository

```bash
: Download repository
git clone https://github.com/LaurentBlanc73/PDF-summarizer.git pdf_summarizer

: Go to to downloaded folder 
cd pdf_summarizer
```

### Docker Setup

```bash
: Build Docker image
cd summarizer_app
docker build -t pdf-summarizer-frontend .

: Run Docker container
docker run -e PORT=8000 -p 8000:8000 pdf-summarizer-frontend
```

The frontend is then available at [http://localhost:8000](http://localhost:8000)

## License

This project uses components licensed under the Apache License 2.0.
