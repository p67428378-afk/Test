import React, { useState } from 'react';
import './App.css';
import PersonalInformationForm from './components/PersonalInformationForm';
import EmploymentDetailsForm from './components/EmploymentDetailsForm';
import LoanRequestForm from './components/LoanRequestForm';
import ReviewAndSubmitForm from './components/ReviewAndSubmitForm';

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

  const handleFinalSubmit = () => {
    alert('Application submitted successfully!');
    // Optionally reset form or navigate to a confirmation page
    setFormData({
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
    setStep(1);
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
          <LoanRequestForm
            formData={formData}
            handleChange={handleChange}
            nextStep={nextStep}
            prevStep={prevStep}
          />
        );
      case 4:
        return (
          <ReviewAndSubmitForm
            formData={formData}
            prevStep={prevStep}
            handleSubmit={handleFinalSubmit}
          />
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
