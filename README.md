
## Project Structure

```
.
├── backend/                 # FastAPI Backend
│   ├── app/                # Application code
│   │   ├── main.py        # FastAPI application
│   │   ├── models/        # Data models
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Example environment variables
│
└── frontend/              # Streamlit Frontend
    ├── src/              # Source code
    │   └── app.py        # Streamlit application
    ├── tests/            # Frontend tests
    ├── requirements.txt  # Frontend dependencies
    └── .env.example      # Example environment variables
```

## Quick Start

### Backend (FastAPI)

1. Set up Python environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the backend:
```bash
uvicorn backend.app.main:app --reload
```

Visit http://localhost:8000/docs for API documentation

### Frontend (Streamlit)

1. Set up Python environment:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the frontend:
```bash
streamlit run frontend/src/main.py
```

Visit http://localhost:8501 to use the application

## Development

### Backend
- Built with FastAPI for high performance
- Uses Pydantic for data validation
- Groq integration for natural language search
- JSON file-based storage for simplicity

### Frontend
- Built with Streamlit for rapid development
- Clean and intuitive user interface
- Real-time form validation
- Responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
