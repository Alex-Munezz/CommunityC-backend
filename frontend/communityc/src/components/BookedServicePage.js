import React from 'react';
import { useNavigate } from 'react-router-dom';

const ConfirmationPage = () => {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-3xl font-extrabold text-green-600 mb-6 text-center">Booking Submitted</h1>
        <p className="text-gray-700 mb-6 text-center">
          Your booking has been successfully submitted. A booking confirmation email will be sent to you shortly. If there is a change in price you will also be notified along with the email and the payment details. 
          Thank you for choosing CommunityCrafters.
        </p>
        <button
          onClick={handleGoBack}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300"
        >
          Go Back to Home Page
        </button>
      </div>
    </div>
  );
};

export default ConfirmationPage;
