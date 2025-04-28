from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.answer import answer_router



def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    app = FastAPI(
        title="LawGPT API",
        description="API for LawGPT - A Legal Question Answering System",
        version="1.0.0",
    )
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Restrict this in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )


    # Register startup event
    # app.add_event_handler("startup", startup_event)

    # Include routers
    app.include_router(answer_router)

    return app

def setup_routes(app: FastAPI):
    """
    Setup basic application routes.
    
    Args:
        app (FastAPI): The FastAPI application instance
    """
    @app.get("/service")
    async def root():
        """Root endpoint providing API information."""
        return {
            "message": "Welcome to LawGPT API",
            "docs": "/docs",
            "version": "1.0.0"
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

# Create the FastAPI application
app = create_app()

# Setup basic routes
setup_routes(app)
