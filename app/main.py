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
from .espn_scraper import scrape_espn_schedule, format_games_for_prompt, group_games_by_time_slot
from typing import List

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


@app.get("/api/picks/list")
async def list_picks_files():
    """
    List all available picks JSON files.
    
    Returns:
        JSON response with list of available files and their metadata.
    """
    try:
        data_dir = Path("app/data")
        json_files = []
        
        # Find all JSON files except current_picks.json
        for file in data_dir.glob("*.json"):
            if file.name == "current_picks.json":
                continue
                
            # Try to extract metadata from filename
            # Format: week_{week_number}_{date}.json
            try:
                parts = file.stem.split("_")
                if len(parts) >= 3 and parts[0] == "week":
                    week_num = parts[1]
                    date_str = "_".join(parts[2:])  # Handle dates with underscores
                    
                    json_files.append({
                        "filename": file.name,
                        "week": int(week_num),
                        "date": date_str,
                        "display_name": f"Week {week_num} - {date_str}"
                    })
            except:
                # If parsing fails, just add the filename
                json_files.append({
                    "filename": file.name,
                    "display_name": file.stem
                })
        
        # Sort by week number (descending) and date (descending)
        json_files.sort(key=lambda x: (x.get("week", 0), x.get("date", "")), reverse=True)
        
        # Add current_picks.json at the top if it exists
        current_picks_path = data_dir / "current_picks.json"
        if current_picks_path.exists():
            json_files.insert(0, {
                "filename": "current_picks.json",
                "display_name": "Current Week (Latest)"
            })
        
        return JSONResponse(content={"files": json_files})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing picks files: {str(e)}")


@app.get("/api/picks/{filename}")
async def get_picks_by_filename(filename: str):
    """
    Get picks from a specific JSON file.
    
    Args:
        filename: Name of the JSON file to load.
        
    Returns:
        JSON response with picks data.
    """
    try:
        # Security: Only allow files in app/data directory
        filepath = Path("app/data") / filename
        
        # Prevent directory traversal
        if not filepath.resolve().is_relative_to(Path("app/data").resolve()):
            raise HTTPException(status_code=403, detail="Access denied")
        
        picks = load_picks(str(filepath))
        return JSONResponse(content=picks.model_dump())
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
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
    espn_game_data_link: str = Form(...),
    slate_description: str = Form(...),
    note: str = Form(...),
    focus_games: str = Form(...),
    prop_focus: str = Form(...),
    min_articles_for_sentiment: int = Form(...),
    include_long_shots: bool = Form(False)
):
    """
    Trigger AI generation of weekly picks with provided configuration.
    
    Updates settings, calls OpenAI, saves results, and redirects to dashboard.
    """
    try:
        # Update settings with form values
        settings.espn_game_data_link = espn_game_data_link
        settings.slate_description = slate_description
        settings.note = note
        settings.focus_games = focus_games
        settings.prop_focus = prop_focus
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


@app.post("/admin/update-config")
async def update_config(
    espn_game_data_link: str = Form(...),
    slate_description: str = Form(...),
    note: str = Form(...),
    focus_games: str = Form(...),
    prop_focus: str = Form(...),
    min_articles_for_sentiment: int = Form(...),
    include_long_shots: bool = Form(False)
):
    """
    Update configuration settings without generating picks.
    
    Updates settings and returns JSON response for AJAX call.
    """
    try:
        # Update settings with form values
        settings.espn_game_data_link = espn_game_data_link
        settings.slate_description = slate_description
        settings.note = note
        settings.focus_games = focus_games
        settings.prop_focus = prop_focus
        settings.min_articles_for_sentiment = min_articles_for_sentiment
        settings.include_long_shots = include_long_shots
        
        return JSONResponse(content={
            "success": True,
            "message": "Configuration updated successfully"
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.post("/admin/save-prompt")
async def save_prompt(prompt_content: str = Form(...)):
    """
    Save edited prompt content to the template file.
    
    Args:
        prompt_content: The edited prompt content to save.
        
    Returns:
        Redirect back to admin page with success/error message.
    """
    try:
        # Save to the prompt template file
        prompt_path = Path(__file__).parent / "prompts" / "weekly_picks.txt"
        
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        
        # Redirect to admin page with success message
        return RedirectResponse(url="/admin?prompt_saved=true", status_code=303)
        
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
        "espn_game_data_link": settings.espn_game_data_link,
        "slate_description": settings.slate_description,
        "note": settings.note,
        "focus_games": settings.focus_games,
        "prop_focus": settings.prop_focus,
        "min_articles_for_sentiment": settings.min_articles_for_sentiment,
        "include_long_shots": settings.include_long_shots
    })


@app.get("/api/prompt-template")
async def get_prompt_template():
    """
    Get the raw prompt template content.
    
    Returns:
        JSON response with the template content.
    """
    try:
        prompt_path = Path(__file__).parent / "prompts" / "weekly_picks.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        return JSONResponse(content={"template": template})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading template: {str(e)}")


@app.get("/api/prompt-preview")
async def get_prompt_preview():
    """
    Get the fully rendered prompt with current settings and selected games.
    
    Returns:
        JSON response with the rendered prompt.
    """
    try:
        prompt = render_prompt()
        return JSONResponse(content={"prompt": prompt})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering prompt: {str(e)}")


@app.get("/api/games")
async def get_games():
    """
    Fetch and return live game data from ESPN with time slot grouping.
    
    Returns:
        JSON response with scraped game data grouped by time slots.
    """
    try:
        games, metadata = scrape_espn_schedule(settings.espn_game_data_link)
        game_list = [game.to_dict() for game in games]
        
        # Group games by time slot
        grouped = group_games_by_time_slot(games)
        time_slots = {
            slot: [game.to_dict() for game in games_in_slot]
            for slot, games_in_slot in grouped.items()
        }
        
        return JSONResponse(content={
            "metadata": metadata,
            "games": game_list,
            "time_slots": time_slots,
            "formatted": format_games_for_prompt(games, settings.focus_games, settings.selected_game_ids if settings.use_game_selection else None)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching games: {str(e)}")


@app.post("/api/games/select")
async def select_games(request: Request):
    """
    Store selected game IDs for prompt generation.
    
    Expects JSON body with:
        {
            "game_ids": ["game_id_1", "game_id_2", ...]
        }
    
    Returns:
        JSON response with success status and selected games.
    """
    try:
        data = await request.json()
        game_ids = data.get("game_ids", [])
        
        # Validate that game_ids is a list
        if not isinstance(game_ids, list):
            raise HTTPException(status_code=400, detail="game_ids must be a list")
        
        # Update settings
        settings.selected_game_ids = game_ids
        settings.use_game_selection = True
        
        return JSONResponse(content={
            "success": True,
            "selected_count": len(game_ids),
            "selected_game_ids": game_ids
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting games: {str(e)}")


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