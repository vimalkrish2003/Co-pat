import React, { useState, useEffect } from 'react';
import FrequencySelector from './FrequencySelector';
import { Row, Col, Container, Button } from 'react-bootstrap';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';

const MedicationForm = ({ medication, index, saveMedicationAtIndex }) => {
    const [MedicationName, setMedicationName] = useState(medication.MedicationName);
    const [Label, setLabel] = useState(medication.Label);
    const [Dosage, setDosage] = useState(medication.Dosage);
    const [NotificationTime, setNotificationTime] = useState(medication.NotificationTime);
    const [Frequency, setFrequency] = useState(medication.Frequency || []);
    const [StartDate, setStartDate] = useState(medication.StartDate);
    const [EndDate, setEndDate] = useState(medication.EndDate);
    const [error, setError] = useState({});
    const labelOptions = ['Before Food', 'After Food'];

    useEffect(() => {
        setMedicationName(medication.MedicationName);
        setLabel(medication.Label);
        setDosage(medication.Dosage);
        setNotificationTime(medication.NotificationTime);
        setFrequency(medication.Frequency);
        setStartDate(medication.StartDate);
        setEndDate(medication.EndDate);
    }, [medication]);

    const handleMedicationChange = (e) => {
        const { name, value } = e.target;
        switch (name) {
            case 'MedicationName':
                setMedicationName(value);
                break;
            case 'Label':
                setLabel(value);
                break;
            case 'Dosage':
                setDosage(value);
                break;
            case 'NotificationTime':
                setNotificationTime(value);
                break;
            case 'StartDate':
                setStartDate(value);
                break;
            case 'EndDate':
                setEndDate(value);
                break;
            default:
                break;
        }
    };

    const handleFrequencyChange = (newValue) => {
        setFrequency(newValue);
    };

    function validateMedicationForm({ MedicationName, Label, Dosage, NotificationTime, Frequency, StartDate, EndDate }) {
        let isValid = true;
        const formErrors = {};

        // Check for required fields
        if (!MedicationName) {
            formErrors.MedicationName = "Medication name is required.";
            isValid = false;
        }
        if (!Label) {
            formErrors.Label = "Label is required.";
            isValid = false;
        }
        if (!Dosage) {
            formErrors.Dosage = "Dosage is required.";
            isValid = false;
        }
        if (!NotificationTime) {
            formErrors.NotificationTime = "Notification time is required.";
            isValid = false;
        }
        if (!Frequency) {
            formErrors.Frequency = "Frequency is required.";
            isValid = false;
        }
        if (!StartDate) {
            formErrors.StartDate = "Start date is required.";
            isValid = false;
        }
        if (!EndDate) {
            formErrors.EndDate = "End date is required.";
            isValid = false;
        }

        // Validate Dosage is a positive number excluding zero
        if (Dosage && (isNaN(Number(Dosage)) || Number(Dosage) <= 0)) {
            formErrors.Dosage = "Dosage must be a positive number and cannot be zero.";
            isValid = false;
        }

        // Validate StartDate and EndDate
        const start = new Date(StartDate);
        const end = new Date(EndDate);
        if (start >= end) {
            formErrors.DateRange = "Start date must be before the end date.";
            isValid = false;
        }

        // Return both validation status and any errors
        setError(formErrors);
        return isValid;
    }

    const handleSaveMedication = () => {
        if (validateMedicationForm({ MedicationName, Label, Dosage, NotificationTime, Frequency, StartDate, EndDate })) {
            saveMedicationAtIndex(index, {
                MedicationName,
                Label,
                Dosage,
                NotificationTime,
                Frequency,
                StartDate,
                EndDate
            });
        }

    };


    return (
        <Container className='medication-container'>
            <Row className='mb-2 mt-2'>
                <Col>
                    <p><strong>Medication {index + 1}</strong></p>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <TextField
                        label="Medication Name"
                        type="text"
                        name="MedicationName"
                        value={MedicationName}
                        onChange={handleMedicationChange}
                        required
                        fullWidth
                        variant="outlined"
                    />
                </Col>
                <Col>
                    {/* TextField with select remains unchanged */}
                    <TextField
                        required
                        fullWidth
                        select
                        label="Label"
                        name="Label"
                        value={Label}
                        onChange={handleMedicationChange}
                        variant="outlined"
                    >
                        {labelOptions.map((option, index) => (
                            <MenuItem key={index} value={option}>{option}</MenuItem>
                        ))}
                    </TextField>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <TextField
                        id="outlined-number"
                        label="Dosage"
                        type="number"
                        name="Dosage"
                        value={Dosage}
                        onChange={handleMedicationChange}
                        required
                        fullWidth
                        variant="outlined"
                    />
                </Col>
                <Col>
                    <TextField
                        label="Notification Time"
                        type="time"
                        name="NotificationTime"
                        value={NotificationTime}
                        onChange={handleMedicationChange}
                        required
                        fullWidth
                        variant="outlined"
                    />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <FrequencySelector handleFrequencyChange={handleFrequencyChange} Frequency={Frequency} />
                </Col>
                <Col>
                    <TextField
                        label="Start Date"
                        type="date"
                        name="StartDate"
                        value={StartDate}
                        onChange={handleMedicationChange}
                        required
                        fullWidth
                        variant="outlined"
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Col>
                <Col>
                    <TextField
                        label="End Date"
                        type="date"
                        name="EndDate"
                        value={EndDate}
                        onChange={handleMedicationChange}
                        required
                        fullWidth
                        variant="outlined"
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Col>
            </Row>
            <Row>
                {error && Object.keys(error).length > 0 && (
                    <div className="alert alert-danger" role="alert" style={{ padding: '5px 10px', margin: '10px 0' }}>
                        {Object.values(error).map((errorMessage, index) => (
                            <div key={index}>{errorMessage}</div>
                        ))}
                    </div>
                )}
            </Row>
            <Row className="mb-3 text-center">
                <Col>
                    <Button onClick={handleSaveMedication} variant='secondary'>Save Medication</Button>
                </Col>
            </Row>
        </Container>
    );
}

export default MedicationForm;