# PDF QA Bot

## Overview
PDF QA Bot is a Flask-based application designed to parse and retrieve information from PDF, DOCX, and TXT documents using a Retrieval-Augmented Generation (RAG) pipeline. The application allows users to upload documents and query them for specific information.

## Project Structure
```
pdf_qa_bot/
├── app.py              # Main entry point for the application
├── loader.py           # Functions for parsing PDF, DOCX, and TXT files
├── rag_pipeline.py     # Implements the RAG pipeline for document retrieval
├── .env                # Environment variables (e.g., GOOGLE_API_KEY)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pdf_qa_bot.git
   cd pdf_qa_bot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory and add your `GOOGLE_API_KEY`:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage
1. Run the application:
   ```
   python app.py
   ```

2. Access the application in your web browser at `http://127.0.0.1:5000`.

3. Upload your documents and start querying for information.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.