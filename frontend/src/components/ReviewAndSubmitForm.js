import React, { useState } from 'react';

const ReviewAndSubmitForm = ({ formData, prevStep, handleSubmit }) => {
  const [submissionStatus, setSubmissionStatus] = useState(null); // null, 'submitting', 'success', 'error'
  const [submissionError, setSubmissionError] = useState(null);

  const onSubmit = async () => {
    setSubmissionStatus('submitting');
    setSubmissionError(null);
    try {
      // First, create the customer
      const customerResponse = await fetch('http://localhost:5000/customers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: formData.fullName,
          dob: formData.dob,
          ssn: formData.ssn,
          address: formData.address,
          contact_info: formData.contactInfo,
          citizenship_status: formData.citizenshipStatus,
          has_pending_legal_cases: formData.hasPendingLegalCases,
        }),
      });

      if (!customerResponse.ok) {
        const errorData = await customerResponse.json();
        throw new Error(errorData.error || 'Failed to create customer');
      }
      const customerData = await customerResponse.json();
      const customerId = customerData.customer_id;

      // Then, add employment details
      const employmentResponse = await fetch(`http://localhost:5000/customers/${customerId}/employment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employer_name: formData.employerName,
          employer_address: formData.employerAddress,
          job_title: formData.jobTitle,
          annual_income: formData.annualIncome,
          employment_history: formData.employmentHistory,
        }),
      });

      if (!employmentResponse.ok) {
        const errorData = await employmentResponse.json();
        throw new Error(errorData.error || 'Failed to add employment details');
      }

      // Finally, create loan application
      const loanApplicationResponse = await fetch(`http://localhost:5000/customers/${customerId}/loan-applications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          purpose: formData.loanPurpose,
          loan_amount: parseFloat(formData.loanAmount),
        }),
      });

      if (!loanApplicationResponse.ok) {
        const errorData = await loanApplicationResponse.json();
        throw new Error(errorData.error || 'Failed to create loan application');
      }

      setSubmissionStatus('success');
      // Optionally, call the parent handleSubmit to reset form or navigate
      if (handleSubmit) handleSubmit();

    } catch (error) {
      console.error('Submission error:', error);
      setSubmissionError(error.message);
      setSubmissionStatus('error');
    }
  };

  return (
    <div className="container">
      <h2 className="text-center">Review Your Application</h2>
      <div>
        <h3>Personal Information</h3>
        <p><strong>Full Name:</strong> {formData.fullName}</p>
        <p><strong>Date of Birth:</strong> {formData.dob}</p>
        <p><strong>SSN:</strong> {formData.ssn}</p>
        <p><strong>Address:</strong> {formData.address}</p>
        <p><strong>Contact Info:</strong> {formData.contactInfo}</p>
        <p><strong>Citizenship Status:</strong> {formData.citizenshipStatus}</p>
        <p><strong>Pending Legal Cases:</strong> {formData.hasPendingLegalCases ? 'Yes' : 'No'}</p>

        <h3>Employment Details</h3>
        <p><strong>Employer Name:</strong> {formData.employerName}</p>
        <p><strong>Employer Address:</strong> {formData.employerAddress}</p>
        <p><strong>Job Title:</strong> {formData.jobTitle}</p>
        <p><strong>Annual Income:</strong> {formData.annualIncome}</p>
        <p><strong>Employment History:</strong> {formData.employmentHistory || 'N/A'}</p>

        <h3>Loan Request</h3>
        <p><strong>Loan Purpose:</strong> {formData.loanPurpose}</p>
        <p><strong>Loan Amount:</strong> ${formData.loanAmount}</p>
      </div>

      <div className="button-group">
        <button type="button" className="secondary" onClick={prevStep}>Back</button>
        <button type="button" className="primary" onClick={onSubmit} disabled={submissionStatus === 'submitting'}>
          {submissionStatus === 'submitting' ? 'Submitting...' : 'Submit Application'}
        </button>
      </div>

      {submissionStatus === 'success' && (
        <p className="success-message">Application submitted successfully!</p>
      )}
      {submissionStatus === 'error' && (
        <p className="error-message">Error submitting application: {submissionError}</p>
      )}
    </div>
  );
};

export default ReviewAndSubmitForm;
