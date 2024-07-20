import React, { useState, useEffect } from 'react';
import { MDBRow, MDBCol, MDBInput, MDBBtn, MDBContainer } from 'mdb-react-ui-kit';
import MedicationForm from './MedicationForm'; // Update the import path as necessary

const PrescriptionForm = ({ prescription, index, savePrescriptionAtIndex }) => {
    const [DoctorName, setDoctorName] = useState(prescription.DoctorName);
    const [Condition, setCondition] = useState(prescription.Condition);
    const [Medications, setMedications] = useState(prescription.Medications || []);
    const [selectedMedication, setSelectedMedication] = useState(0);
    const [isMedicationExpanded, setIsMedicationExpanded] = useState(true);
    const [error, setError] = useState({});

    useEffect(() => {
        setDoctorName(prescription.DoctorName);
        setCondition(prescription.Condition);
        setMedications(prescription.Medications || []);
    }, [prescription]);

    const handlePrescriptionChange = (e) => {
        const { name, value } = e.target;
        if (name === "DoctorName") {
            setDoctorName(value);
        } else if (name === "Condition") {
            setCondition(value);
        }
    };

    const validatePrescription = () => {
        let isValid = true;
        const newError = {};

        if (!DoctorName.trim()) {
            newError.DoctorName = "Doctor Name is required.";
            isValid = false;
        }

        if (!Condition.trim()) {
            newError.Condition = "Condition is required.";
            isValid = false;
        }
        //check if the first medicationName is empty
        if (Medications.length > 0 && Medications[0].MedicationName.trim() === '') {
            newError.MedicationName = "Medication is required.";
            isValid = false;
        }

        //check if DoctorName and condition is string
        if (DoctorName.trim() && !/^[a-zA-Z ]+$/.test(DoctorName)) {
            newError.DoctorName = "Doctor Name must contain only alphabets and spaces.";
            isValid = false;
        }
        if (Condition.trim() && !/^[a-zA-Z ]+$/.test(Condition)) {
            newError.Condition = "Condition must contain only alphabets and spaces.";
            isValid = false;
        }
        setError(newError);
        return isValid;
    }


    const handleSavePrescription = (e) => {
        e.preventDefault();
        if (validatePrescription()) {
            savePrescriptionAtIndex(index, {
                Condition,
                DoctorName,
                Medications
            });
        }
    }

    const expandMedication = (index) => {
        setSelectedMedication(index);
        setIsMedicationExpanded(true);
    }

    const saveMedicationAtIndex = (index, medication) => {
        setMedications(Medications.map((item, i) => {
            if (i === index) {
                return medication;
            }
            return item;
        }));
        setIsMedicationExpanded(false);
    };

    const handleAddMedication = (e) => {
        e.preventDefault();
        const lastMedication = Medications[Medications.length - 1];
        const isLastMedicationFilled = lastMedication && lastMedication.MedicationName.trim() !== '';

        if (isLastMedicationFilled || Medications.length === 0) {
            console.log('Adding new medication');
            setMedications([...Medications, {
                MedicationName: '',
                Label: '',
                Dosage: '',
                NotificationTime: '00:00',
                Frequency: [],
                StartDate: '',
                EndDate: ''
            }]);
            setSelectedMedication(Medications.length);
            setIsMedicationExpanded(true);
        } else {
            alert('Please fill out the last medication before adding a new one.');
            console.log('Please fill out the last medication before adding a new one.');
        }
    };

    return (
        <MDBContainer className='mt-3 prescription-container'>
            <MDBRow className='mt-2 mb-2'>
                <MDBCol>
                    <h6><strong>Prescription {index + 1}</strong></h6>
                </MDBCol>
            </MDBRow>
            <MDBRow className="mb-3">
                <MDBCol>
                    <MDBInput label="Condition" type="text" name="Condition" value={Condition} onChange={handlePrescriptionChange} required />
                </MDBCol>
            </MDBRow>
            <MDBRow className='mb-3'>
                <MDBCol>
                    <MDBInput label="Doctor Name" type="text" name="DoctorName" value={DoctorName} onChange={handlePrescriptionChange} required />
                </MDBCol>
            </MDBRow>

            {Medications.map((medication, index) => (
                index === selectedMedication && isMedicationExpanded ? <MedicationForm key={index} medication={medication} index={index} saveMedicationAtIndex={saveMedicationAtIndex} /> :
                    <MDBRow key={index} className='mb-3'>
                        <MDBCol>
                            <span onClick={() => expandMedication(index)}>
                                {medication.MedicationName ? medication.MedicationName : 'No Medication'} →
                            </span>
                        </MDBCol>
                    </MDBRow>
            ))}
            <MDBRow>
                <MDBCol className='d-flex justify-content-end'>
                    <MDBBtn className='mb-3' size='sm' color='teritiary' onClick={handleAddMedication}>Add Medication</MDBBtn>
                </MDBCol>
            </MDBRow>
            <MDBRow>
                {error && Object.keys(error).length > 0 && (
                    <div className="alert alert-danger" role="alert" style={{ padding: '5px 10px', margin: '10px 0' }}>
                        {Object.values(error).map((errorMessage, index) => (
                            <div key={index}>{errorMessage}</div>
                        ))}
                    </div>
                )}
            </MDBRow>
            <MDBRow className="mb-3 text-center">
                <MDBCol>
                    <MDBBtn onClick={handleSavePrescription} color='secondary'>Save Prescription</MDBBtn>
                </MDBCol>
            </MDBRow>
        </MDBContainer>
    );
};

export default PrescriptionForm;