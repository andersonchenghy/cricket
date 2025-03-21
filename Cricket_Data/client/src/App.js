import React, { useState, useEffect } from "react";
import "./App.css";
import { BarChart } from '@mui/x-charts';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

const App = () => {
  const [gameData, setGameData] = useState(null);
  const [allGamesData, setAllGamesData] = useState(null);
  const [selectedGame, setSelectedGame] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // First fetch games list
        const allgamesResponse = await fetch("http://localhost:8000/v1/games");
        const allgamesResult = await allgamesResponse.json();
        setAllGamesData(allgamesResult);
        // const gameDetailsResponse = await fetch("http://localhost:8000/v1/gamedetails?home_team=Huddersfield%20Heat&away_team=Doncaster%20Renegades");
        // const gameDetailsResult = await gameDetailsResponse.json();
        // setGameData(gameDetailsResult);
      } catch (error) {
        console.warn("Failed to fetch data:", error);
      }
    };

    fetchData();
  }, []);

  const handleGameChange = (event) => {
    setSelectedGame(event.target.value);
    // Split the value to get home and away teams
    const [homeTeam, awayTeam] = event.target.value.split('-');

    // Fetch new game details with selected teams
    fetch(`http://localhost:8000/v1/gamedetails?home_team=${encodeURIComponent(homeTeam)}&away_team=${encodeURIComponent(awayTeam)}`)
      .then((res) => res.json())
      .then(
        (result) => {
          setGameData(result);
        },
        (error) => {
          console.warn("Failed to fetch game details:", error);
        }
      );
  };

  return (
    <div className="App" style={{ backgroundColor: 'white', color: 'black' }}>
      <header className="App-header" style={{ backgroundColor: 'white', color: 'black' }}>
        {/* Games Select Dropdown */}
        {allGamesData && (
          <Box sx={{ minWidth: 300, marginBottom: 4 }}>
            <FormControl fullWidth>
              <InputLabel id="game-select-label">Select Game</InputLabel>
              <Select
                labelId="game-select-label"
                id="game-select"
                value={selectedGame}
                label="Select Game"
                onChange={handleGameChange}
              >
                {allGamesData.map((game, index) => (
                  <MenuItem key={index} value={`${game.home_team}-${game.away_team}`}>
                    {game.home_team} vs {game.away_team} - {game.date}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        )}

        {/* Only render chart when we have all required data */}
        {gameData && gameData.home_percentages && gameData.away_percentages && (
          <div>
            <h1>{gameData.home_team} vs {gameData.away_team}</h1>
            <h3>Home Team Win Percentage: {gameData.win_probability}%</h3>

            <h2>Simulation Results</h2>
            <BarChart
              width={1000}
              height={500}
              series={[
                {
                  data: gameData.home_percentages,
                  label: gameData.home_team,
                  valueFormatter: (value) => `${value}%`,
                  color: '#4CAF50'
                },
                {
                  data: gameData.away_percentages,
                  label: gameData.away_team,
                  valueFormatter: (value) => `${value}%`,
                  color: '#2196F3'
                }
              ]}
              xAxis={[{
                data: gameData.home_ranges,
                scaleType: 'band',
                label: 'Runs Scored',
                tickLabelStyle: {
                  angle: 45,
                  textAnchor: 'start',
                  fontSize: 14,
                  fill: '#666'
                },
                labelStyle: {
                  fontSize: 16,
                  fill: '#666',
                  transform: 'translateY(60px)'
                }
              }]}
              yAxis={[{
                label: 'Percentage of Matches',
                valueFormatter: (value) => `${value}%`,
                tickLabelStyle: {
                  fill: '#666'
                },
                labelStyle: {
                  fontSize: 16,
                  fill: '#666',  // Dark grey text
                  transform: 'translate(-280px, 120px) rotate(-90deg)'
                }
              }]}
              legend={{
                position: { vertical: 'top', horizontal: 'right' },
                padding: 20,
                itemMarkWidth: 20,
                itemMarkHeight: 20,
                markGap: 10,
                itemGap: 30,
                fontSize: 16,
                labelStyle: {
                  fill: '#000'
                },
                style: {
                  fill: '#000'
                }
              }}
              margin={{
                top: 50,
                right: 100,
                bottom: 100,
                left: 100
              }}
              tooltip={{
                trigger: 'axis'
              }}
              grid={{
                vertical: true,
                horizontal: true
              }}
            />
          </div>
        )}
        {!gameData && <p>Please Select a Game...</p>}
      </header>
    </div>
  );
};

export default App;
