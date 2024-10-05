import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode'; // To decode the token
import Footer from './Footer';
import '../App.css';

const BookingPage = () => {
  const { name } = useParams();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone_number: '',
    service_name: name || '',
    date: '',
    time: '',
    additional_info: '',
    subcategory: [], // Changed to an array for multiple selections
    price: 0,
    county: '',
    town: '',
    street: '',
  });
  const [loading, setLoading] = useState(false);
  const [servicePricing, setServicePricing] = useState({});
  const [subcategories, setSubcategories] = useState([]);
  const [error, setError] = useState('');
  const [locationFetching, setLocationFetching] = useState(false);
  const navigate = useNavigate();
  const GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY';

  // Fetch user ID from access token
  const getUserIdFromToken = () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('No token found');
      
      const decodedToken = jwtDecode(token);
      
      return decodedToken.sub; 
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  };
    
  

  const fetchServicePricing = async (selectedSubcategoryId) => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/pricing?service_id=${formData.service_name}&subcategory_id=${selectedSubcategoryId}`);
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error fetching pricing:', errorData);
        throw new Error('Failed to fetch pricing info');
      }
      const data = await response.json();
      return data.price || 0;
    } catch (err) {
      console.error(err.message);
      return 0;
    } finally {
      setLoading(false);
    }
  };

  const fetchSubcategories = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/subcategories?service_name=${formData.service_name}`);
      if (!response.ok) throw new Error('Failed to fetch subcategories');
      const data = await response.json();
      setSubcategories(data);
    } catch (err) {
      console.error(err.message);
    }finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (formData.service_name) {
      fetchSubcategories();
    }
  }, [formData.service_name]);

  useEffect(() => {
    const totalPrice = formData.subcategory.reduce((total, subcatId) => {
      return total + (servicePricing[subcatId] || 0);
    }, 0);
    setFormData((prevData) => ({
      ...prevData,
      price: totalPrice,
    }));
  }, [formData.subcategory, servicePricing]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          setLocationFetching(true);

          try {
            const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`);
            const data = await response.json();
            const addressComponents = data.results[0]?.address_components || [];

            const county = addressComponents.find(comp => comp.types.includes('administrative_area_level_2'))?.long_name || '';
            const town = addressComponents.find(comp => comp.types.includes('locality'))?.long_name || '';
            const street = addressComponents.find(comp => comp.types.includes('route'))?.long_name || '';

            setFormData((prevData) => ({
              ...prevData,
              county,
              town,
              street,
            }));
          } catch (error) {
            console.error('Error fetching address:', error);
          } finally {
            setLocationFetching(false);
          }
        },
        (error) => {
          console.error('Error fetching location:', error);
          setLocationFetching(false);
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0,
        }
      );
    } else {
      console.error('Geolocation is not supported by this browser.');
    }
  }, []);

  const handleChange = async (e) => {
    const { name, value } = e.target;

    if (name === 'subcategory') {
        const selectedValue = value;
        setFormData((prevData) => {
            const updatedSubcategory = prevData.subcategory.includes(selectedValue)
                ? prevData.subcategory.filter((id) => id !== selectedValue)
                : [...prevData.subcategory, selectedValue];

            return { ...prevData, subcategory: updatedSubcategory };
        });

        const price = await fetchServicePricing(selectedValue);
        setServicePricing((prevPricing) => ({
            ...prevPricing,
            [selectedValue]: parseFloat(price), // Ensure price is a number
        }));
    } else {
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    }
};


  const validateDateAndTime = () => {
    const selectedDate = new Date(formData.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate < today) {
      return 'You cannot book a past date.';
    }

    if (selectedDate.getTime() === today.getTime()) {
      return 'You cannot book for today. Please choose a future date.';
    }

    const selectedTime = formData.time;
    const selectedHours = parseInt(selectedTime.split(':')[0], 10);

    if (selectedHours < 7 || selectedHours >= 19) {
      return 'Booking is only allowed between 7:00 AM and 7:00 PM.';
    }

    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const validationError = validateDateAndTime();
    if (validationError) {
      setError(validationError);
      return;
    }
  
    const bookingData = {
      name: formData.name,
      email: formData.email,
      phone_number: formData.phone_number,
      service_name: formData.service_name,
      date: formData.date,
      time: formData.time,
      additional_info: formData.additional_info,
      subcategory: formData.subcategory.join(','),
      price: formData.price,
      county: formData.county,
      town: formData.town,
      street: formData.street,
    };
  
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('User not authenticated');
        return;
    }
      const response = await fetch('http://127.0.0.1:5000/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Pass token in header
        },
        body: JSON.stringify(bookingData),
      });
  
      if (!response.ok) {
        throw new Error('Failed to submit booking.');
      }
  
      localStorage.setItem('booking_price', formData.price);
      navigate('/booked-service');
    } catch (error) {
      console.error('Error submitting booking:', error);
      setError('Failed to submit booking. Please try again.');
    } finally {
      setLoading(false); 
    }
  };
  

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <div className="flex-grow container mx-auto px-4 py-8">
      {loading && (
          <div className="flex justify-center items-center">
            <div className="loader">Loading...</div>
          </div>
        )}
        {!loading && (
          <>
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">Book {formData.service_name}</h1>
        <form className="max-w-lg mx-auto bg-white p-8 rounded-lg shadow-lg border border-gray-200" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-100 text-red-800 p-4 rounded-lg mb-4">
              {error}
            </div>
          )}
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="name">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="phone_number">
              Phone Number
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="county">
              County
            </label>
            <input
              type="text"
              id="county"
              name="county"
              value={formData.county}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
            <div className="mb-6">
              <label className="required block text-gray-700 text-sm font-semibold mb-1">Town</label>
              <input
                type="text"
                id="town"
                name="town"
                value={formData.town}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              />
            </div>
            <div className="mb-6">
              <label className="required block text-gray-700 text-sm font-semibold mb-1">Street</label>
              <input
                type="text"
                id="street"
                name="street"
                value={formData.street}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              />
            </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="date">
              Date
            </label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="time">
              Time
            </label>
            <input
              type="time"
              id="time"
              name="time"
              value={formData.time}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="service name">
              Service Name
            </label>
            <input
              type="text"
              id="service name"
              name="service name"
              value={formData.service_name}
              readOnly
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              required
            />
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="subcategory">
              Select Subcategories (Please select categories related to your service ONLY!!)
            </label>
            <select
              id="subcategory"
              name="subcategory"
              multiple
              value={formData.subcategory}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
            >
              {subcategories.map((subcat) => (
                <option key={subcat.name} value={subcat.name}>
                  {subcat.name}
                </option>
              ))}
            </select>
            <div className="mt-2 text-gray-600">
              Selected: {formData.subcategory.join(', ')}
            </div>
          </div>
          <div className="mb-6">
            <label className="required block text-gray-700 text-sm font-semibold mb-2" htmlFor="additionalInfo">
              Additional Information ( Please explain service needed in detail )
            </label>
            <textarea
              id="additional_info"
              name="additional_info"
              value={formData.additional_info}
              onChange={handleChange}
              rows="3"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 text-xl font-semibold mb-2" htmlFor="price">
              Total Price: {formData.price} Ksh
            </label>
          </div>
          <button
  type="submit"
  disabled={loading} // Disable button while loading
  className={`w-full py-3 text-white font-semibold rounded-lg shadow-md transition duration-300 ${
    loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
  }`}
>
  {loading ? (
    <div className="flex items-center justify-center">
      <span className="loader mr-2">Loading...</span> 
      Booking...
    </div>
  ) : (
    'Book Service'
  )}
</button>

        </form>
        </>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default BookingPage;

