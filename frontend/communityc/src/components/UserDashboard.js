import React, { useEffect, useState } from 'react';
import { useAuth } from './AuthContext'; // Ensure the path is correct
import { jwtDecode } from 'jwt-decode'; // To decode the JWT token

const UserDashboard = () => {
    const [userDetails, setUserDetails] = useState(null);
    const [bookings, setBookings] = useState([]);
    const [showBookings, setShowBookings] = useState(false);
    const [isEditingUser, setIsEditingUser] = useState(false); // State to manage editing user details
    const [updatedDetails, setUpdatedDetails] = useState({}); // State for updated user details
    const [isEditingBooking, setIsEditingBooking] = useState(null); // State to manage editing booking
    const [updatedBookingDetails, setUpdatedBookingDetails] = useState({}); // State for updated booking details
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                const decodedToken = jwtDecode(token);
                const userId = decodedToken.sub.id;

                await fetchUserDetails(userId);
                await fetchUserBookings(userId);
            }
        };
        if (isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated]);

    const fetchUserDetails = async (userId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/users/${userId}`); // Fetch user details
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            setUserDetails(data);
            setUpdatedDetails(data); // Initialize updatedDetails with fetched data
        } catch (error) {
            console.error('Fetch user details error:', error);
        }
    };
    
    const fetchUserBookings = async (userId) => {
        try {
            const token = localStorage.getItem('access_token'); // Get token to send with request
            const response = await fetch(`http://127.0.0.1:5000/bookings/user/${userId}`, {
                headers: { 
                    'Authorization': `Bearer ${token}` // Include the token
                }
            }); 
            
            if (!response.ok) {
                const errorData = await response.json();
                console.error('Fetch user bookings error:', errorData); // Log error details
                return; // Exit the function if unauthorized
            }
    
            const data = await response.json();
            setBookings(data.bookings || []); // Assuming data.bookings is the correct structure
        } catch (error) {
            console.error('Fetch user bookings error:', error);
        }
    };
    
    
    const handleUpdateUserDetails = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const userId = updatedDetails.id; // Assume userDetails has an id
            const response = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Include the token
                },
                body: JSON.stringify(updatedDetails), // Update with updatedDetails data
            });
            if (!response.ok) throw new Error('Network response was not ok');
            fetchUserDetails(userId); // Refresh user details after update
            setIsEditingUser(false); // Close editing mode
        } catch (error) {
            console.error('Update user details error:', error);
        }
    };

    const handleUpdateBooking = async (bookingId) => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`http://127.0.0.1:5000/bookings/${bookingId}`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Include the token
                },
                body: JSON.stringify(updatedBookingDetails), // Update with updatedBookingDetails data
            });
            if (!response.ok) throw new Error('Network response was not ok');
            fetchUserBookings(); // Refresh bookings after update
            setIsEditingBooking(null); // Close editing mode
        } catch (error) {
            console.error('Update booking error:', error);
        }
    };

    const handleDeleteBooking = async (bookingId) => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`http://127.0.0.1:5000/bookings/${bookingId}`, { 
                method: 'DELETE',
                headers: { 
                    'Authorization': `Bearer ${token}`, // Include the token
                },
            });
            if (!response.ok) throw new Error('Network response was not ok');
            setBookings(bookings.filter(booking => booking.id !== bookingId)); // Update bookings list
        } catch (error) {
            console.error('Delete booking error:', error);
        }
    };

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
            {userDetails && (
                <div className="bg-white p-4 rounded-lg shadow-md mb-6">
                    <h2 className="text-2xl font-semibold">Your Details</h2>
                    {isEditingUser ? (
                        <div>
                            <input
                                type="text"
                                value={updatedDetails.firstname}
                                onChange={(e) => setUpdatedDetails({ ...updatedDetails, firstname: e.target.value })}
                                className="border p-2 rounded mb-2 w-full"
                                placeholder="First Name"
                            />
                            <input
                                type="text"
                                value={updatedDetails.lastname}
                                onChange={(e) => setUpdatedDetails({ ...updatedDetails, lastname: e.target.value })}
                                className="border p-2 rounded mb-2 w-full"
                                placeholder="Last Name"
                            />
                            <input
                                type="email"
                                value={updatedDetails.email}
                                onChange={(e) => setUpdatedDetails({ ...updatedDetails, email: e.target.value })}
                                className="border p-2 rounded mb-2 w-full"
                                placeholder="Email"
                            />
                            <input
                                type="text"
                                value={updatedDetails.phone_number}
                                onChange={(e) => setUpdatedDetails({ ...updatedDetails, phone_number: e.target.value })}
                                className="border p-2 rounded mb-2 w-full"
                                placeholder="Phone Number"
                            />
                            <input
                                type="text"
                                value={updatedDetails.location}
                                onChange={(e) => setUpdatedDetails({ ...updatedDetails, location: e.target.value })}
                                className="border p-2 rounded mb-2 w-full"
                                placeholder="Location"
                            />
                            <button 
                                onClick={handleUpdateUserDetails}
                                className="mt-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                            >
                                Save Changes
                            </button>
                            <button 
                                onClick={() => setIsEditingUser(false)}
                                className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                            >
                                Cancel
                            </button>
                        </div>
                    ) : (
                        <div>
                            <p>Name: {userDetails.firstname} {userDetails.lastname}</p>
                            <p>Email: {userDetails.email}</p>
                            <p>Phone: {userDetails.phone_number}</p>
                            <p>Location: {userDetails.location}</p>
                            <button 
                                onClick={() => setIsEditingUser(true)}
                                className="mt-2 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                            >
                                Edit Details
                            </button>
                        </div>
                    )}
                </div>
            )}
            <button 
                onClick={() => setShowBookings(!showBookings)}
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
                {showBookings ? 'Hide My Bookings' : 'View My Bookings'}
            </button>

            {showBookings && (
                <section className="mt-6">
                    <h2 className="text-2xl font-semibold mb-4">My Bookings</h2>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {bookings.map(booking => (
                            <div key={booking.id} className="bg-white p-4 rounded-lg shadow-md">
                                {isEditingBooking === booking.id ? (
                                    <div>
                                        <div className='p-1'>Service Name : {booking.service_name}</div>
                                        <div className='p-1'>Price : {booking.price}</div>
                                         <input
                                            type="text"
                                            value={updatedBookingDetails.county || booking.county}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, county: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                            placeholder="County"
                                        />
                                         <input
                                            type="text"
                                            value={updatedBookingDetails.town || booking.town}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, town: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                            placeholder="Town"
                                        />
                                        <input
                                            type="text"
                                            value={updatedBookingDetails.street || booking.street}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, street: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                            placeholder="Street"
                                        />
                                         <input
                                            type="text"
                                            value={updatedBookingDetails.subcategory || booking.subcategory}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, subcategory: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                            placeholder="Subcategory"
                                        />
                                        <input
                                            type="date"
                                            value={updatedBookingDetails.date || booking.date}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, date: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                            placeholder="Date"
                                        />
                                        <input
                                            type="time"
                                            value={updatedBookingDetails.time || booking.time}
                                            onChange={(e) => setUpdatedBookingDetails({ ...updatedBookingDetails, time: e.target.value })}
                                            className="border p-2 rounded mb-2 w-full"
                                        />
                                        <button 
                                            onClick={() => handleUpdateBooking(booking.id)}
                                            className="mt-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                                        >
                                            Save Changes
                                        </button>
                                        <button 
                                            onClick={() => setIsEditingBooking(null)}
                                            className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                ) : (
                                    <div>
                                        <div className="text-lg font-semibold">Booking ID: {booking.id}</div>
                                        <div>Service Name: {booking.service_name}</div>
                                        <div>Subcategory: {booking.subcategory}</div>
                                        <div>Price: {booking.price}</div>
                                        <div>Booking Date: {booking.date} at {booking.time}</div>
                                        <div>Your Location: {booking.county}, {booking.town}, {booking.street}</div>
                                        <button 
                                            onClick={() => {
                                                setIsEditingBooking(booking.id);
                                                setUpdatedBookingDetails(booking); // Pre-fill the fields with current booking details
                                            }} 
                                            className="mt-2 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                                        >
                                            Update
                                        </button>
                                        <button 
                                            onClick={() => handleDeleteBooking(booking.id)} 
                                            className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
};

export default UserDashboard;
