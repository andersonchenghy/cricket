from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.connector import database
import pandas as pd
from typing import List

router = APIRouter()

@router.get("/v1/games")
def get_all_games():
    """
    Get a list of all cricket matches with team details
    """
    try:
        games = database.query_get(
            """
            SELECT 
                games.home_team,
                games.away_team,
                games.date,
                venues.venue_name
            FROM games
            JOIN venues ON games.venue_id = venues.venue_id
            ORDER BY games.date
            """
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=jsonable_encoder(games)
        )
    except Exception as e:
        print(f"Error in get_all_games: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )

@router.get("/v1/gamedetails")
def get_game_details(home_team: str, away_team: str):
    """
    Get a list of all cricket matches with team details
    """
    try:
        Home_team_sim = database.query_get(
            """
            SELECT 
                simulations.team,
                simulations.simulation_run,
                simulations.results
            FROM simulations
            WHERE simulations.team = %s
            """,
            (home_team,)  # Pass parameters
        )

        Away_team_sim = database.query_get(
            """
            SELECT 
                simulations.team,
                simulations.simulation_run,
                simulations.results
            FROM simulations
            WHERE simulations.team = %s
            """,
            (away_team,)  # Pass parameters
        )
     
        Home_team_sim_df = pd.DataFrame(Home_team_sim)
        Away_team_sim_df = pd.DataFrame(Away_team_sim)

        Home_team_sim_df['team'] = home_team
        Away_team_sim_df['team'] = away_team

        # Count how many times the home team wins compared to the away team, one to one comparison
        win_probability = int((Home_team_sim_df['results'].astype(int) > 
                         Away_team_sim_df['results'].astype(int)).sum())

        home_results = Home_team_sim_df['results'].astype(int)
        away_results = Away_team_sim_df['results'].astype(int)
        
        max_value = max(home_results.max(), away_results.max())
        
        # Create bins for both teams
        home_bins = [0, 100] + list(range(110, max_value + 1, 10))
        away_bins = [0, 100] + list(range(110, max_value + 1, 10))
        
        # Count the occurrences in each bin from home team
        home_counts = pd.cut(home_results, bins=home_bins).value_counts().sort_index()

        total_home_results = home_counts.sum()

        # Calculate percentages for home team
        home_percentages = (home_counts / total_home_results * 100).round().astype(float).tolist()

        # Make range labels for home team
        home_ranges = ['0-100'] + [f"{home_bins[i]}-{home_bins[i+1]}" for i in range(1, len(home_bins)-1)]

        # Count the occurrences in each bin for away team
        away_counts = pd.cut(away_results, bins=away_bins).value_counts().sort_index()

        total_away_results = away_counts.sum()

        # Calculate percentages for away team
        away_percentages = (away_counts / total_away_results * 100).round().astype(float).tolist()

        # Make range labels for home team
        away_ranges = ['0-100'] + [f"{away_bins[i]}-{away_bins[i+1]}" for i in range(1, len(away_bins)-1)]

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=jsonable_encoder({
                "home_team": home_team,
                "away_team": away_team,
                "win_probability": win_probability,
                "home_percentages": home_percentages,
                "home_ranges": home_ranges,
                "away_percentages": away_percentages,
                "away_ranges": away_ranges
            })
        )
    except Exception as e:
        print(f"Error in get_game_details: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )