# Oratio On-Premises Prototype

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org)

Oratio is an advanced AI-powered legal question answering system specifically designed for Tunisian accounting and legal standards. This on-premises prototype provides a complete RAG (Retrieval-Augmented Generation) pipeline for processing legal documents and delivering accurate, contextual responses to legal and accounting queries.

## 🏗️ Architecture Overview

Oratio follows a microservices architecture with real-time data processing capabilities:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │  Data Pipeline  │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (Bytewax)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐    ┌─────────────────┐
         │              │  Vector Store   │    │   Document DB   │
         └──────────────►│   (Qdrant)      │    │   (MongoDB)     │
                        └─────────────────┘    └─────────────────┘
                                 │                       │
                                 └───────────────────────┘
                                     Message Queue
                                     (RabbitMQ)
```

## 🚀 Key Features

- **🤖 AI-Powered Legal Assistant**: Advanced RAG system using LangChain and OpenAI for accurate legal document analysis
- **📚 Tunisian Legal Standards**: Pre-loaded with Tunisian accounting standards (NC 01-05) and legal frameworks
- **⚡ Real-time Data Processing**: Stream processing pipeline using Bytewax for continuous document ingestion
- **🔍 Semantic Search**: Vector-based document retrieval using Qdrant for contextually relevant responses
- **💬 Conversational Interface**: Modern React frontend with conversation history and document source tracking
- **🏢 Enterprise Ready**: Containerized deployment with MongoDB replica sets and message queuing
- **🌐 Multilingual Support**: i18n support with language detection capabilities

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **LangChain**: LLM orchestration and RAG implementation
- **OpenAI**: Language model integration
- **Qdrant**: Vector database for semantic search
- **MongoDB**: Document storage with replica set support
- **RabbitMQ**: Message queuing for data pipeline
- **Bytewax**: Stream processing framework

### Frontend
- **React 18**: Modern UI framework with TypeScript
- **Vite**: Fast build tool and development server
- **TailwindCSS**: Utility-first CSS framework
- **Redux Toolkit**: State management
- **React Router**: Client-side routing
- **React Markdown**: Markdown rendering for responses

### Infrastructure
- **Docker**: Containerization and orchestration
- **Kubernetes**: Container orchestration (configs in `/infra/k8s/`)
- **Nginx**: Reverse proxy and static file serving

## 📁 Project Structure

```
oratio-on-prem-prototype/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic models
│   │   ├── retriever/      # RAG implementation
│   │   ├── core/           # Core utilities
│   │   └── prompts/        # LLM prompt templates
│   └── Dockerfile
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── api/            # API client
│   │   └── hooks/          # Custom React hooks
│   └── Dockerfile
├── data-indexing/          # Data processing pipeline
│   ├── 2-data-ingestion/   # CDC and data ingestion
│   ├── 3-feature-pipeline/ # Stream processing with Bytewax
│   ├── etl-backend/        # ETL service
│   ├── data/              # Legal documents (NC standards)
│   └── docker-compose.yml # Infrastructure services
├── infra/                 # Kubernetes deployment configs
└── tests/                 # Test suites
```

## 🚦 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd oratio-on-prem-prototype
   ```

2. **Start infrastructure services**
   ```bash
   cd data-indexing
   docker-compose up -d mongo1 mongo2 mongo3 mq qdrant
   ```

3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Qdrant Dashboard: http://localhost:6333/dashboard
   - RabbitMQ Management: http://localhost:15673

### Development Setup

#### Backend Development
```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

#### Data Pipeline Development
```bash
cd data-indexing/3-feature-pipeline
uv sync
uv run python main.py
```

## 📊 Data Pipeline

The system includes a sophisticated data processing pipeline:

1. **Document Ingestion**: Legal documents are stored in MongoDB
2. **Change Data Capture (CDC)**: Monitors document changes in real-time
3. **Stream Processing**: Bytewax processes document updates and creates embeddings
4. **Vector Storage**: Embeddings are stored in Qdrant for semantic search
5. **RAG Retrieval**: Backend queries relevant documents for user questions

## 🔧 Configuration

### Environment Variables

Create `.env` files in respective directories:

**Backend (.env)**
```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URL=mongodb://localhost:30001,localhost:30002,localhost:30003/?replicaSet=my-replica-set
QDRANT_URL=http://localhost:6333
RABBITMQ_URL=amqp://localhost:5673
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test

# Integration tests
cd tests
pytest
```

## 📈 Monitoring and Health Checks

- **Health Endpoint**: `GET /health`
- **Service Status**: `GET /service`
- **RabbitMQ Management**: http://localhost:15673
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 🚀 Deployment

### Kubernetes Deployment
```bash
kubectl apply -f infra/k8s/
```

### Production Considerations

- Configure proper CORS settings in production
- Set up SSL/TLS certificates
- Configure resource limits and scaling policies
- Set up monitoring and logging (Prometheus, Grafana, ELK stack)
- Configure backup strategies for MongoDB and Qdrant

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Legal Documents

The system comes pre-loaded with Tunisian accounting standards:
- NC 01-05: Tunisian Accounting Standards
- Legal framework documents
- Conceptual framework (Cadre Conceptuel)

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Replica Set Issues**
   ```bash
   docker-compose exec mongo1 mongo --eval "rs.initiate()"
   ```

2. **Qdrant Connection Issues**
   - Ensure Qdrant container is running: `docker ps | grep qdrant`
   - Check logs: `docker logs oratio-qdrant`

3. **RabbitMQ Connection Issues**
   - Verify RabbitMQ is accessible: http://localhost:15673
   - Default credentials: guest/guest

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for language model capabilities
- LangChain community for RAG frameworks
- Qdrant team for vector database solutions
- FastAPI and React communities for excellent frameworks

---

For more detailed documentation, please refer to the individual README files in each service directory.