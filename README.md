# PDF-summarizer
A Webapplication that allows for uploading and summarizing PDF files.

## Project structure

PDF-summarizer
├── .github/workflows/      # GitHub Actions CI workflow for running tests
├── example_pdfs/           # collection of sample PDFs for testing the application
├── model_development/      # notebooks for fine-tuning and evaluating the model
└── summarizer_app/         # source code for the web application
    ├── frontend/           # functions and classes
    │   └── assets/         # assets of the frontend
    ├── run.py              # application entry point for local development
    ├── wsgi.py             # WSGI entry point for production servers
    ├── requirements.txt    # Python dependencies
    └── Dockerfile          # Instructions for building Docker image

## Getting started

### Clone the repository

```
: Download repository
git clone https://github.com/LaurentBlanc73/PDF-summarizer.git pdf_summarizer

: Goto to downloaded folder 
cd pdf_summarizer

```

### Docker Setup

```
: Build Docker image
cd summarizer_app
docker build -t pdf-summarizer-frontend .

: Run Docker container
docker run -e PORT=8000 -p 8000:8000 pdf-summarizer-frontend
```

The frontend is then available at [http://localhost:8000](http://localhost:8000)

## License

This project uses components licensed under the Apache License 2.0.