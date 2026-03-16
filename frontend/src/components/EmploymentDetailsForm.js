import React, { useState } from 'react';

const EmploymentDetailsForm = ({ formData, handleChange, nextStep, prevStep }) => {
  const [errors, setErrors] = useState({});

  const validate = () => {
    let tempErrors = {};
    if (!formData.employerName) tempErrors.employerName = "Employer Name is required.";
    if (!formData.employerAddress) tempErrors.employerAddress = "Employer Address is required.";
    if (!formData.jobTitle) tempErrors.jobTitle = "Job Title is required.";
    if (!formData.annualIncome) tempErrors.annualIncome = "Annual Income is required.";
    else if (isNaN(formData.annualIncome) || parseFloat(formData.annualIncome) <= 0) tempErrors.annualIncome = "Annual Income must be a positive number.";
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
      <h2 className="text-center">Employment Details</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Employer Name:</label>
          <input type="text" name="employerName" value={formData.employerName} onChange={handleChange} />
          {errors.employerName && <p className="error-message">{errors.employerName}</p>}
        </div>
        <div className="form-group">
          <label>Employer Address:</label>
          <input type="text" name="employerAddress" value={formData.employerAddress} onChange={handleChange} />
          {errors.employerAddress && <p className="error-message">{errors.employerAddress}</p>}
        </div>
        <div className="form-group">
          <label>Job Title:</label>
          <input type="text" name="jobTitle" value={formData.jobTitle} onChange={handleChange} />
          {errors.jobTitle && <p className="error-message">{errors.jobTitle}</p>}
        </div>
        <div className="form-group">
          <label>Annual Income:</label>
          <input type="number" name="annualIncome" value={formData.annualIncome} onChange={handleChange} />
          {errors.annualIncome && <p className="error-message">{errors.annualIncome}</p>}
        </div>
        <div className="form-group">
          <label>Employment History (last 2 years):</label>
          <textarea name="employmentHistory" value={formData.employmentHistory} onChange={handleChange} rows="4"></textarea>
        </div>
        <div className="button-group">
          <button type="button" className="secondary" onClick={prevStep}>Back</button>
          <button type="submit" className="primary">Next</button>
        </div>
      </form>
    </div>
  );
};

export default EmploymentDetailsForm;
