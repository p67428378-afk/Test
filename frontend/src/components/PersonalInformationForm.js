import React, { useState } from 'react';

const PersonalInformationForm = ({ formData, handleChange, nextStep }) => {
  const [errors, setErrors] = useState({});

  const validate = () => {
    let tempErrors = {};
    if (!formData.fullName) tempErrors.fullName = "Full Name is required.";
    if (!formData.dob) tempErrors.dob = "Date of Birth is required.";
    if (!formData.ssn) tempErrors.ssn = "SSN is required.";
    else if (!/^[0-9]{3}-[0-9]{2}-[0-9]{4}$/.test(formData.ssn)) tempErrors.ssn = "SSN must be in XXX-XX-XXXX format.";
    if (!formData.address) tempErrors.address = "Address is required.";
    if (!formData.contactInfo) tempErrors.contactInfo = "Contact Info is required.";
    else if (!/^[\w-]+(?:\.[\w-]+)*@(?:[\w-]+\.)+[a-zA-Z]{2,7}$/.test(formData.contactInfo)) tempErrors.contactInfo = "Invalid email format.";
    if (!formData.citizenshipStatus) tempErrors.citizenshipStatus = "Citizenship Status is required.";
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
      <h2 className="text-center">Personal Information</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name:</label>
          <input type="text" name="fullName" value={formData.fullName} onChange={handleChange} />
          {errors.fullName && <p className="error-message">{errors.fullName}</p>}
        </div>
        <div className="form-group">
          <label>Date of Birth:</label>
          <input type="date" name="dob" value={formData.dob} onChange={handleChange} />
          {errors.dob && <p className="error-message">{errors.dob}</p>}
        </div>
        <div className="form-group">
          <label>SSN (XXX-XX-XXXX):</label>
          <input type="text" name="ssn" value={formData.ssn} onChange={handleChange} placeholder="XXX-XX-XXXX" />
          {errors.ssn && <p className="error-message">{errors.ssn}</p>}
        </div>
        <div className="form-group">
          <label>Address:</label>
          <input type="text" name="address" value={formData.address} onChange={handleChange} />
          {errors.address && <p className="error-message">{errors.address}</p>}
        </div>
        <div className="form-group">
          <label>Contact Info (Email):</label>
          <input type="email" name="contactInfo" value={formData.contactInfo} onChange={handleChange} />
          {errors.contactInfo && <p className="error-message">{errors.contactInfo}</p>}
        </div>
        <div className="form-group">
          <label>Citizenship Status:</label>
          <input type="text" name="citizenshipStatus" value={formData.citizenshipStatus} onChange={handleChange} />
          {errors.citizenshipStatus && <p className="error-message">{errors.citizenshipStatus}</p>}
        </div>
        <div className="form-group">
          <label>
            <input type="checkbox" name="hasPendingLegalCases" checked={formData.hasPendingLegalCases} onChange={handleChange} />
            I have pending legal cases.
          </label>
        </div>
        <div className="button-group">
          <button type="submit" className="primary">Next</button>
        </div>
      </form>
    </div>
  );
};

export default PersonalInformationForm;
