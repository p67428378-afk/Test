import React, { useState } from 'react';

const LoanRequestForm = ({ formData, handleChange, nextStep, prevStep }) => {
  const [errors, setErrors] = useState({});

  const validate = () => {
    let tempErrors = {};
    if (!formData.loanPurpose) tempErrors.loanPurpose = "Loan Purpose is required.";
    if (!formData.loanAmount) tempErrors.loanAmount = "Loan Amount is required.";
    else if (isNaN(formData.loanAmount) || parseFloat(formData.loanAmount) < 1000 || parseFloat(formData.loanAmount) > 50000) {
      tempErrors.loanAmount = "Loan Amount must be between $1,000 and $50,000.";
    }
    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      nextStep();
    }
  };

  return (
    <div className="container">
      <h2 className="text-center">Loan Request Specification</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Purpose of Loan:</label>
          <select name="loanPurpose" value={formData.loanPurpose} onChange={handleChange}>
            <option value="">Select Purpose</option>
            <option value="debt_consolidation">Debt Consolidation</option>
            <option value="home_improvement">Home Improvement</option>
            <option value="medical_expenses">Medical Expenses</option>
            <option value="other">Other</option>
          </select>
          {errors.loanPurpose && <p className="error-message">{errors.loanPurpose}</p>}
        </div>
        <div className="form-group">
          <label>Desired Loan Amount ($1,000 - $50,000):</label>
          <input type="number" name="loanAmount" value={formData.loanAmount} onChange={handleChange} />
          {errors.loanAmount && <p className="error-message">{errors.loanAmount}</p>}
        </div>
        <div className="button-group">
          <button type="button" className="secondary" onClick={prevStep}>Back</button>
          <button type="submit" className="primary">Next</button>
        </div>
      </form>
    </div>
  );
};

export default LoanRequestForm;
