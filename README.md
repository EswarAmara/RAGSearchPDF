# RAG Streamlit Application

A local RAG (Retrieval-Augmented Generation) chatbot built with Streamlit, using HuggingFace models for embeddings and text generation.

## Features

- 📄 **Document Processing**: Upload and process PDF and TXT files
- 🤖 **Local AI**: Uses free HuggingFace models (no API keys required)
- 🔍 **Semantic Search**: FAISS vector database for efficient retrieval
- 💬 **Interactive Chat**: Real-time Q&A with document context
- 📊 **Source Attribution**: View source documents for each answer
- 🧠 **Memory**: Maintains conversation context

## Quick Start

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv RAGenv
   source RAGenv/bin/activate  # On Windows: RAGenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open browser**: Navigate to `http://localhost:8501`

### Option 2: Docker Deployment

#### Using Docker Compose (Recommended)
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop
docker-compose down
```

#### Using Docker directly
```bash
# Build image
docker build -t rag-streamlit .

# Run container
docker run -p 8501:8501 rag-streamlit

# Run with volume for file persistence
docker run -p 8501:8501 -v $(pwd)/uploads:/app/uploads rag-streamlit
```

### Option 3: Streamlit Cloud Deployment

1. **Push to GitHub**
2. **Connect to Streamlit Cloud**
3. **Deploy automatically**

## Usage

1. **Upload Documents**: Use the sidebar to upload PDF or TXT files
2. **Process Documents**: Click "Process Documents" to index your files
3. **Ask Questions**: Type questions about your documents
4. **View Sources**: Expand source sections to see relevant document snippets
5. **Clear Chat**: Reset conversation history when needed

## Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with LangChain framework
- **Embeddings**: HuggingFace sentence-transformers
- **Vector Store**: FAISS for efficient similarity search
- **LLM**: Local HuggingFace transformers models
- **File Processing**: PyPDF2 for PDFs, built-in for TXTs

## Requirements

- Python 3.8+
- 4GB+ RAM (for model loading)
- Internet connection (for initial model download)

## Dependencies

See `requirements.txt` for complete list:
- streamlit
- langchain
- langchain-community
- langchain-huggingface
- faiss-cpu
- pypdf2
- sentence-transformers
- transformers
- torch

## Container Specifications

- **Base Image**: Python 3.11-slim
- **Port**: 8501
- **Health Check**: Streamlit health endpoint
- **Volume Mounts**: Optional file persistence
- **Environment**: Headless mode for container deployment

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   - Check internet connection
   - Increase timeout settings
   - Use VPN if needed

2. **Memory Issues**
   - Reduce chunk size in `utils.py`
   - Use smaller embedding models
   - Increase container memory limits

3. **File Upload Issues**
   - Check file permissions
   - Ensure file format is supported
   - Verify file size limits

### Performance Optimization

- Use GPU if available (modify Dockerfile)
- Adjust chunk sizes based on document types
- Implement caching for repeated queries
- Use smaller models for faster inference

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request 