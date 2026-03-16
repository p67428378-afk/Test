import React, { useState } from 'react';
import './App.css';
import PersonalInformationForm from './components/PersonalInformationForm';
import EmploymentDetailsForm from './components/EmploymentDetailsForm';

function App() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    fullName: '',
    dob: '',
    ssn: '',
    address: '',
    contactInfo: '',
    citizenshipStatus: '',
    hasPendingLegalCases: false,
    employerName: '',
    employerAddress: '',
    jobTitle: '',
    annualIncome: '',
    employmentHistory: '',
    loanPurpose: '',
    loanAmount: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const nextStep = () => {
    setStep((prevStep) => prevStep + 1);
  };

  const prevStep = () => {
    setStep((prevStep) => prevStep - 1);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <PersonalInformationForm
            formData={formData}
            handleChange={handleChange}
            nextStep={nextStep}
          />
        );
      case 2:
        return (
          <EmploymentDetailsForm
            formData={formData}
            handleChange={handleChange}
            nextStep={nextStep}
            prevStep={prevStep}
          />
        );
      case 3:
        return (
          <div className="container">
            <h2 className="text-center">Loan Request</h2>
            <p>Loan request form will go here.</p>
            <div className="button-group">
              <button className="secondary" onClick={prevStep}>Back</button>
              <button className="primary" onClick={nextStep}>Next</button>
            </div>
          </div>
        );
      case 4:
        return (
          <div className="container">
            <h2 className="text-center">Review and Submit</h2>
            <p>Review and submit form will go here.</p>
            <div className="button-group">
              <button className="secondary" onClick={prevStep}>Back</button>
              <button className="primary" onClick={nextStep}>Submit</button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <div className="step-navigation">
        <button className={step === 1 ? 'active' : ''}>Personal Info</button>
        <button className={step === 2 ? 'active' : ''}>Employment</button>
        <button className={step === 3 ? 'active' : ''}>Loan Request</button>
        <button className={step === 4 ? 'active' : ''}>Review & Submit</button>
      </div>
      {renderStep()}
    </div>
  );
}

export default App;
