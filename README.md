# GFR & PM Assistant Chatbot

A sophisticated chatbot application that provides intelligent responses to queries about General Financial Rules (GFR) 2017 and Procurement Manual (PM) 2025. The application uses advanced NLP techniques and the Gemini API to provide accurate, context-aware responses with proper citations.

## Features

### Core Features
1. **Intelligent Document Processing**
   - Automated extraction of rules from GFR 2017 and PM 2025 PDFs
   - Hierarchical rule organization (chapters, sections, subsections)
   - Smart rule validation and categorization
   - Support for both GFR and PM specific rule patterns

2. **Advanced Search Capabilities**
   - Semantic search across both documents
   - Keyword-based matching
   - Entity recognition for better context understanding
   - Rule hierarchy consideration in search results
   - Citation tracking with page numbers and sources

3. **Chat Interface**
   - Real-time chat with the assistant
   - Conversation history tracking
   - Markdown support for formatted responses
   - Citation display with source documents
   - Quick action buttons for common queries
   - Export chat history functionality

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn
- Gemini API key

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create `.env` file in backend directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Install spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Start the backend server:
   ```bash
   PYTHONPATH=$PYTHONPATH:. python -m uvicorn main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure
```
.
├── backend/
│   ├── data/                  # PDF documents
│   │   ├── GFR2017.pdf
│   │   └── pm2025.pdf
│   ├── utils/
│   │   ├── knowledge_base.py  # Core NLP and rule processing
│   │   ├── document_processor.py
│   │   └── vector_store.py
│   ├── scripts/
│   │   ├── process_documents.py
│   │   └── setup.py
│   ├── main.py               # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   └── ChatInterface.tsx
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── public/
│   │   ├── GFR2017.pdf
│   │   └── pm2025.pdf
│   └── package.json
└── README.md
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Google Gemini API for advanced language processing
- FastAPI for the robust backend framework
- Next.js team for the excellent frontend framework
- The open-source community for various tools and libraries 


python scripts/process_documents.py

## Deploying Backend on Render.com

1. Ensure `backend/data/` contains `GFR2017.pdf` and `pm2025.pdf` and they are committed to your repository.
2. In Render, set the root directory to `backend` if your repo has both frontend and backend.
3. Set the build command to:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```
4. Set the start command to:
   ```bash
   gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:10000
   ```
5. Add your Vercel frontend domain to the CORS `allow_origins` list in `main.py`.
6. The backend will serve PDFs from `/static/GFR2017.pdf` and `/static/pm2025.pdf`.
7. Set the `GEMINI_API_KEY` environment variable in Render (if/when you want to secure the key).
8. After deployment, update your frontend to use the Render backend URL for API calls.