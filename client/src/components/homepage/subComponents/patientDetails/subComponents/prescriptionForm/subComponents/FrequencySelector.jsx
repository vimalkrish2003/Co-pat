import React, { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { ListItemText } from '@mui/material';

export default function FrequencySelector({handleFrequencyChange,Frequency}) {
  const daysOfWeek = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
  ];

  const handleSelectionChange = (event, newValue) => {
    // Check if the length of newValue is less than selectedDays, indicating removal
    if (newValue.length < Frequency.length) {
      handleFrequencyChange(newValue);
    }
  };
  const handleOptionClick = (event, option) => {
    event.stopPropagation();
    // Check if the day is already selected
    const selectedIndex = Frequency.indexOf(option);
    let newSelectedDays = [];

    if (selectedIndex === -1) {
      // If not selected, add it to the selectedDays array
      newSelectedDays = [...Frequency, option];
    }
    handleFrequencyChange(newSelectedDays);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Autocomplete
        multiple
        fullWidth
        id="frequency-select"
        options={daysOfWeek}
        getOptionLabel={(option) => option}
        filterSelectedOptions
        value={Frequency}
        onChange={handleSelectionChange}
        renderOption={(props, option, { selected }) => (
          <li {...props} fullWidth>
            <ListItemText  primary={option} onClick={(event) => handleOptionClick(event, option)} />
          </li>
        )}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="outlined"
            label="Frequency"
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <React.Fragment>
                  {params.InputProps.endAdornment}
                </React.Fragment>
              ),
            }}
          />
        )}
      />
    </Box>
  );
}