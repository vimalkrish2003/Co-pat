import React, { useState } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { Row, Col } from 'react-bootstrap';
import {
    MDBRow,
    MDBCol,
    MDBInput,
    MDBBtn
} from 'mdb-react-ui-kit';

function PatientForm() {
    const [name, setName] = useState('');
    const [dateOfBirth, setDateOfBirth] = useState('');
    const [gender, setGender] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [bloodType, setBloodType] = useState('');
    const [error, setError] = useState({});

    const genderOptions = ['Male','Female','Other'];
    const bloodTypeOptions = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

    const validateForm = () => {
        let errors = {};
        let formIsValid = true;

        // Name validation
        if (!name) {
            formIsValid = false;
            errors["name"] = "*Please enter the name.";
        }

        // Date of Birth validation
        if (!dateOfBirth) {
            formIsValid = false;
            errors["dateOfBirth"] = "*Please enter the date of birth.";
        } else {
            const dob = new Date(dateOfBirth);
            const today = new Date();
            if (dob >= today) {
                formIsValid = false;
                errors["dateOfBirth"] = "*Date of birth must be in the past.";
            }
        }

        // Gender validation
        if (!gender) {
            formIsValid = false;
            errors["gender"] = "*Please enter the gender.";
        } else if (!['Male', 'Female', 'Other'].includes(gender)) {
            formIsValid = false;
            errors["gender"] = "*Gender must be 'Male', 'Female', or 'Other'.";
        }

        // Phone Number validation
        if (!phoneNumber) {
            formIsValid = false;
            errors["phoneNumber"] = "*Please enter the phone number.";
        } else if (!/^\+?\d{10,20}$/.test(phoneNumber)) {
            formIsValid = false;
            errors["phoneNumber"] = "*Please enter a valid phone number with 10 to 20 digits.";
        }

        // Blood Type validation
        if (!bloodType) {
            formIsValid = false;
            errors["bloodType"] = "*Please enter the blood type.";
        } else if (!['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].includes(bloodType.toUpperCase())) {
            formIsValid = false;
            errors["bloodType"] = "*Please enter a valid blood type (e.g., A+, O-).";
        }

        setError(errors);
        return formIsValid;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError({}); // Reset error messages before attempting to submit
        if (validateForm()) {
            const patientData = {
                name,
                dateOfBirth,
                gender,
                phoneNumber,
                bloodType,
            };

            try {
                const response = await axios.post('/patient/add/', patientData);
                console.log(response.data.message);
                // Reset form fields after successful submission
                setName('');
                setDateOfBirth('');
                setGender('');
                setPhoneNumber('');
                setBloodType('');
                setError({}); // Clear any errors
            } catch (err) {
                console.log(err);
            }
        }
    };
    return (
        <form onSubmit={handleSubmit}>
            <Row className="mb-3 mt-3">
                <Col>
                    <TextField
                        required
                        fullWidth
                        id="outlined-required"
                        label="Name"
                        defaultValue={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <TextField
                        required
                        fullWidth
                        id="outlined-required"
                        label="Date of Birth"
                        type="date"
                        defaultValue={dateOfBirth}
                        onChange={(e) => setDateOfBirth(e.target.value)}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Col>
                <Col>
                    <TextField
                        required
                        fullWidth
                        select
                        id="outlined-required"
                        label="Gender"
                        defaultValue={gender}
                        onChange={(e) => setGender(e.target.value)}
                    >
                        {genderOptions.map((option,index)=>{
                            return <MenuItem key={index} value={option}>{option}</MenuItem>
                        })}
                    </TextField>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <TextField
                        required
                        fullWidth
                        id="outlined-required"
                        label="Phone Number"
                        defaultValue={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                </Col>
                <Col>
                    <TextField
                        required
                        fullWidth
                        select
                        id="outlined-required"
                        label="Blood Type"
                        defaultValue={bloodType}
                        onChange={(e) => setBloodType(e.target.value)}
                    >
                        {bloodTypeOptions.map((option,index)=>{
                            return <MenuItem key={index} value={option}>{option}</MenuItem>
                        })}
                    </TextField>
                </Col>
            </Row>
            {error && Object.keys(error).length > 0 && (
                <div className="alert alert-danger" role="alert" style={{ padding: '5px 10px', margin: '10px 0' }}>
                    {Object.values(error).map((errorMessage, index) => (
                        <div key={index}>{errorMessage}</div>
                    ))}
                </div>
            )}
            <Row className="mb-3 text-center">
                <Col>
                    <button type="submit" className="btn btn-primary">Add Patient Details</button>
                </Col>
            </Row>

        </form>
    )
}

export default PatientForm;