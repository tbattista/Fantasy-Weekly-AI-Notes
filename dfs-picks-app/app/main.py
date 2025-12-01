"""FastAPI application for DFS/Props Picks."""

import os
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .ai_client import generate_picks, save_picks, load_picks, render_prompt
from .config import settings
from .models import WeeklyPicksModel

# Initialize FastAPI app
app = FastAPI(
    title="DFS/Props Picks Generator",
    description="AI-powered weekly NFL DFS and prop betting recommendations",
    version="1.0.0"
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Main dashboard displaying the weekly picks.
    
    Loads current_picks.json and renders it with the dashboard template.
    """
    try:
        # Try to load existing picks
        picks = load_picks()
        picks_data = picks.model_dump()
    except FileNotFoundError:
        # No picks generated yet
        picks_data = None
    except Exception as e:
        # Error loading picks
        picks_data = None
        print(f"Error loading picks: {e}")
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "picks": picks_data,
            "settings": settings
        }
    )


@app.get("/api/picks")
async def get_picks():
    """
    API endpoint to get current picks as JSON.
    
    Returns:
        JSON response with picks data or error message.
    """
    try:
        picks = load_picks()
        return JSONResponse(content=picks.model_dump())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No picks generated yet. Visit /admin to generate picks.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading picks: {str(e)}")


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """
    Admin page for configuring variables and triggering pick generation.
    """
    # Get current prompt preview
    try:
        prompt_preview = render_prompt()
    except Exception as e:
        prompt_preview = f"Error rendering prompt: {str(e)}"
    
    # Try to load current picks for display
    try:
        picks = load_picks()
        picks_json = picks.model_dump_json(indent=2)
    except:
        picks_json = None
    
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "settings": settings,
            "prompt_preview": prompt_preview,
            "picks_json": picks_json
        }
    )


@app.post("/admin/run")
async def run_generation(
    year: int = Form(...),
    week_number: int = Form(...),
    date: str = Form(...),
    slate_description: str = Form(...),
    note: str = Form(...),
    focus_games: str = Form(...),
    min_articles_for_sentiment: int = Form(...),
    include_long_shots: bool = Form(False)
):
    """
    Trigger AI generation of weekly picks with provided configuration.
    
    Updates settings, calls OpenAI, saves results, and redirects to dashboard.
    """
    try:
        # Update settings with form values
        settings.year = year
        settings.week_number = week_number
        settings.date = date
        settings.slate_description = slate_description
        settings.note = note
        settings.focus_games = focus_games
        settings.min_articles_for_sentiment = min_articles_for_sentiment
        settings.include_long_shots = include_long_shots
        
        # Generate picks using OpenAI structured outputs
        picks = generate_picks()
        
        # Save to file
        save_picks(picks)
        
        # Redirect to dashboard to view results
        return RedirectResponse(url="/?success=true", status_code=303)
        
    except Exception as e:
        # Return to admin page with error
        return RedirectResponse(url=f"/admin?error={str(e)}", status_code=303)


@app.get("/api/config")
async def get_config():
    """
    Get current configuration settings.
    
    Returns:
        JSON response with current settings.
    """
    return JSONResponse(content={
        "year": settings.year,
        "week_number": settings.week_number,
        "date": settings.date,
        "slate_description": settings.slate_description,
        "note": settings.note,
        "focus_games": settings.focus_games,
        "min_articles_for_sentiment": settings.min_articles_for_sentiment,
        "include_long_shots": settings.include_long_shots
    })


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        JSON response with status.
    """
    return JSONResponse(content={"status": "healthy", "version": "1.0.0"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)