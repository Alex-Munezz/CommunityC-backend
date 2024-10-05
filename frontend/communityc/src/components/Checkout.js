import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CheckoutPage = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [price, setPrice] = useState(null); // State for the price
  const [error, setError] = useState(null); // State for error handling
  const navigate = useNavigate();

  // Fetch the price from localStorage when the component mounts
  useEffect(() => {
    const fetchedPrice = localStorage.getItem('booking_price');
    if (fetchedPrice) {
      setPrice(parseFloat(fetchedPrice));
    } else {
      setError('Price not found. Please try again.');
    }
  }, []);

  const handlePhoneNumberChange = (e) => {
    setPhoneNumber(e.target.value);
  };

  const handlePay = async () => {
    if (!phoneNumber) {
      setError('Please enter your phone number.');
      return;
    }

    if (!price) {
      setError('Price is not available.');
      return;
    }

    setIsProcessing(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/process-payment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phoneNumber,
          amount: price,
        }),
      });

      if (!response.ok) {
        throw new Error('Payment request failed');
      }

      const data = await response.json();

      if (data.status === 'success') {
        navigate('/booked-service');
      } else {
        throw new Error(data.message || 'Payment failed');
      }
    } catch (error) {
      console.error('Payment failed', error);
      setError(error.message || 'Payment failed. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Form submit handler
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent form submission
    handlePay(); // Call payment handler
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-bold text-blue-600 mb-6 text-center">Checkout</h1>
        <p className="text-gray-700 mb-6 text-center">
          Please enter your phone number to proceed with payment via M-Pesa.
        </p>
        {error && (
          <div className="bg-red-100 text-red-800 p-4 rounded-lg mb-4">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="phoneNumber" className="block text-gray-600 mb-2">Phone Number</label>
            <input
              type="text"
              id="phoneNumber"
              value={phoneNumber}
              onChange={handlePhoneNumberChange}
              placeholder="e.g., 0701234567"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>
          <div className="mb-6">
            <label htmlFor="price" className="block text-gray-600 mb-2">Price (Kshs)</label>
            <input
              type="text"
              id="price"
              value={price ? price.toFixed(2) : 'Loading...'} // Display price or loading
              readOnly
              className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
            />
          </div>
          <button
            type="submit"
            className={`w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-300 ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isProcessing}
          >
            {isProcessing ? 'Processing...' : 'Pay with M-Pesa'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CheckoutPage;
