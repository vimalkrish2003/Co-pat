import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import axios from 'axios';
import FormControlLabel from '@mui/material/FormControlLabel';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import './Settings.css';

function Settings() {
  const [uniqueString, setUniqueString] = useState('');
  const [expirationTime, setExpirationTime] = useState('');
  const [timeLeft, setTimeLeft] = useState('');
  const [remindGuardian, setRemindGuardian] = useState(false);
  const [remindPatient, setRemindPatient] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/guardian/notification/status/');
        setRemindGuardian(response.data.remindGuardian);
        setRemindPatient(response.data.remindPatient);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }
    , []);

  useEffect(() => {
    if (expirationTime) {
      const interval = setInterval(() => {
        const now = new Date();
        const expirationDate = new Date(expirationTime);
        const difference = expirationDate - now;
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        setTimeLeft(`${minutes}m ${seconds}s`);

        if (difference < 0) {
          clearInterval(interval);
          setTimeLeft('Unique String Expired');
          setUniqueString('');
        }
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [expirationTime]);

  const getUniqueString = async () => {
    try {
      const response = await axios.get('/telegram/unique_string/');
      setUniqueString(response.data.uniqueString);
      setExpirationTime(response.data.expirationTime);
    } catch (error) {
      console.log(error);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(uniqueString).then(() => { });
  };

  const handleRemindGuardianChange = async (event) => {
    const newValue = event.target.checked;
    if (newValue && !remindPatient) {
      setError('You should enable remind patient before getting notifications as guardian');
      return;
    }
    setRemindGuardian(newValue);
    try {
      await axios.post('/guardian/notification/status/set/', { remindGuardian: newValue, remindPatient: remindPatient });
    } catch (error) {
      console.log(error);
    }
  };

  const handleRemindPatientChange = async (event) => {
    const newValue = event.target.checked;
    setRemindPatient(newValue);
    try {
      if (newValue) {
        await axios.post('/guardian/notification/status/set/', { remindPatient: newValue, remindGuardian: remindGuardian });
      } 
      else {
        setRemindGuardian(newValue);
        await axios.post('/guardian/notification/status/set/', { remindPatient: newValue, remindGuardian: newValue });
      }
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <Container fluid className="settings-container-fluid">
      <Row className="settings-row">
        <Col className="settings-col">
          <FormControlLabel
            value="start"
            control={<Checkbox checked={remindPatient} onChange={handleRemindPatientChange} />}
            label="Do you want to send reminders to the patients"
            labelPlacement="start"
          />
        </Col>
      </Row>
      <Row className="settings-row">
        <Col className="settings-col">
          <FormControlLabel
            value="start"
            control={<Checkbox checked={remindGuardian} onChange={handleRemindGuardianChange} />}
            label="Do you want to receive notifications regarding patient's medication status"
            labelPlacement="start"
          />
        </Col>
      </Row>
      <Row className='settings-row'>
        <Col className='settings-col'>
          {error && (
            <div className="alert alert-danger" role="alert" style={{ padding: '5px 10px', margin: '10px 0' }}>
              {error}
            </div>
          )}
        </Col>
      </Row>
      <Container fluid className="settings-custom-container">
        <p className="settings-p">
          Steps to verify your telegram app to get notifications:<br />
          1. Go to <a href="https://t.me/Copaat_bot" target="_blank" rel="noopener noreferrer" className="settings-a">CoPat</a> bot and start the bot and click the start button if you are new or type /verify if you want to verify with a new telegram account<br />
          2. If asked to enter the Unique string click on the Get Unique String button and enter the string in the bot<br />
          3. Now follow the instructions in the bot to verify the telegram app
        </p>
        <Row className="settings-row">
          <Col className="settings-col">
            <Button variant="outlined" type="button" onClick={getUniqueString} className="settings-button">Get Unique String</Button>
            <TextField
              className='ms-3 settings-TextField'
              disabled
              id="outlined-disabled"
              label="Unique String"
              value={uniqueString}
            />
            <IconButton onClick={copyToClipboard} aria-label="copy" className="settings-IconButton">
              <ContentCopyIcon />
            </IconButton>

          </Col>
        </Row>
        <Row className="settings-row">
          <Col className="settings-col">
            {timeLeft && <p className="settings-timer-display">Time left: {timeLeft}</p>}
          </Col>
        </Row>
      </Container>
      <Container fluid className="settings-custom-container">
        <p className="settings-p">
          Note:<br />
          1. If you have already verified you need not verify again <br />
          2. Connecting Patients to the bot is also done using the same Unique String
        </p>
      </Container>
    </Container>
  );
}

export default Settings;