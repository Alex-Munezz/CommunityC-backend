import React, { useEffect, useState } from 'react';

const AdminDashboard = () => {
    const [bookings, setBookings] = useState([]);
    const [users, setUsers] = useState([]);
    const [feedback, setFeedback] = useState([]);
    const [showBookings, setShowBookings] = useState(false);
    const [showUsers, setShowUsers] = useState(false);
    const [showFeedback, setShowFeedback] = useState(false);
    const [selectedBooking, setSelectedBooking] = useState(null);
    const [updatedData, setUpdatedData] = useState({});
    const [showProviders, setShowProviders] = useState(false);
    const [serviceProviders, setServiceProviders] = useState([]);
    
    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/bookings');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setBookings(Array.isArray(data.bookings) ? data.bookings : []);
            } catch (error) {
                console.error('Fetch bookings error:', error);
            }
        };

        const fetchUsers = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/users');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setUsers(data);
            } catch (error) {
                console.error('Fetch users error:', error);
            }
        };

        const fetchFeedback = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/feedback');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setFeedback(data);
            } catch (error) {
                console.error('Fetch feedback error:', error);
            }
        };

        const fetchServiceProviders = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/service-providers');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setServiceProviders(data); // Set the service providers data
            } catch (error) {
                console.error('Fetch service providers error:', error);
            }
        };

        // Fetch data when component mounts
        fetchBookings();
        fetchUsers();
        fetchFeedback();
        fetchServiceProviders();
    }, []);

    const handleDeleteBooking = async (bookingId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/bookings/${bookingId}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Network response was not ok');
            setBookings(bookings.filter(booking => booking.id !== bookingId));
        } catch (error) {
            console.error('Delete booking error:', error);
        }
    };

    const handleDeleteFeedback = async (feedbackId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/feedback/${feedbackId}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Network response was not ok');
            setFeedback(feedback.filter(item => item.id !== feedbackId)); // Update feedback state
        } catch (error) {
            console.error('Delete feedback error:', error);
        }
    };

    const handleUpdateBooking = async (bookingId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/bookings/${bookingId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedData),
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const updatedBooking = await response.json();
            setBookings(bookings.map(booking => booking.id === bookingId ? updatedBooking : booking));
            setSelectedBooking(null);
            setUpdatedData({});
        } catch (error) {
            console.error('Update booking error:', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUpdatedData(prevData => ({
            ...prevData,
            [name]: value,
        }));
    };

    

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            <h1 className="text-3xl font-bold mb-4">Admin Dashboard</h1>
            
            {/* Bookings Card */}
            <section className="mb-6">
                <div className="grid gap-4 md:grid-cols-2">
                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-bold">Total Bookings</h3>
                        <p className="text-lg">{bookings.length}</p>
                        <button 
                            onClick={() => setShowBookings(!showBookings)}
                            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            {showBookings ? 'Hide Bookings' : 'View Bookings'}
                        </button>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-bold">Total Users</h3>
                        <p className="text-lg">{users.length}</p>
                        <button 
                            onClick={() => setShowUsers(!showUsers)}
                            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            {showUsers ? 'Hide Users' : 'View Users'}
                        </button>
                    </div>

                    {/* Feedback Card */}
                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-bold">Total Feedback</h3>
                        <p className="text-lg">{feedback.length}</p>
                        <button 
                            onClick={() => setShowFeedback(!showFeedback)}
                            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            {showFeedback ? 'Hide Feedback' : 'View Feedback'}
                        </button>
                    </div>
                    {/* Service Providers Card */}
                 <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-xl font-bold">Total Service Providers</h3>
                    <p className="text-lg">{serviceProviders.length}</p>
                    <button onClick={() => setShowProviders(!showProviders)} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {showProviders ? 'Hide Providers' : 'View Providers'}
                    </button>
                </div>
                </div>
            </section>

            {/* Bookings List */}
            {showProviders && (
                <section className="mb-6">
                    <h2 className="text-2xl font-semibold mb-4">All Service Providers</h2>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {serviceProviders.map(provider => (
                            <div key={provider.id} className="bg-white p-4 rounded-lg shadow-md">
                                <div className="text-lg font-semibold">Provider Name: {provider.name}</div>
                                <div>Email: {provider.email}</div>
                                <div>Phone: {provider.phone_number}</div>
                                <div>Service ID: {provider.service_id}</div>
                                <div>Provider Location: {provider.location} </div>
                            </div>
                        ))}
                    </div>
                </section>
            )}
            {showBookings && (
                <section className="mb-6">
                    <h2 className="text-2xl font-semibold mb-4">All Bookings</h2>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {bookings.map(booking => (
                            <div key={booking.id} className="bg-white p-4 rounded-lg shadow-md">
                                <div className="text-lg font-semibold">Booking ID: {booking.id}</div>
                                <div>Service Name: {booking.service_name}</div>
                                <div>Booked By: {booking.name}</div>
                                <div>Email: {booking.email}</div>
                                <div>Phone Number: {booking.phone_number}</div>
                                <div>Location: {booking.county}, {booking.town}, {booking.street}</div>
                                <div>Booking Subcategory: {booking.subcategory}</div>
                                <div>Price: {booking.price}</div>
                                <div>Booking Date: {booking.date} at {booking.time}</div>
                                
                                <button 
                                    onClick={() => handleDeleteBooking(booking.id)} 
                                    className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                >
                                    Delete
                                </button>
                                <button 
                                    onClick={() => {
                                        setSelectedBooking(booking);
                                        setUpdatedData({});
                                    }} 
                                    className="mt-2 ml-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                                >
                                    Update
                                </button>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            {/* Feedback List */}
            {showFeedback && (
                <section className="mb-6">
                    <h2 className="text-2xl font-semibold mb-4">All Feedback</h2>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {feedback.map(item => (
                            <div key={item.id} className="bg-white p-4 rounded-lg shadow-md">
                                <div className="text-lg font-semibold">Feedback ID: {item.id}</div>
                                <div>Name: {item.name}</div>
                                <div>Email: {item.email}</div>
                                <div>Subject: {item.subject}</div>
                                <div>Message: {item.message}</div>
                                <button 
                                    onClick={() => handleDeleteFeedback(item.id)} 
                                    className="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                >
                                    Delete
                                </button>
                            </div>
                        ))}
                    </div>
                </section>
            )}
            {showUsers && (
                <section>
                    <h2 className="text-2xl font-semibold mb-4">All Users</h2>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {users.map(user => (
                            <div key={user.id} className="bg-white p-4 rounded-lg shadow-md">
                                <div className="text-lg font-semibold">Username: {user.username}</div>
                                <div>Email: {user.email}</div>
                                <div>Phone: {user.phone_number}</div>
                                <div>Name: {user.firstname} {user.lastname}</div>
                                <div>Location: {user.location}</div>
                            </div>
                        ))}
                    </div>
                </section>
            )}
            {selectedBooking && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h2 className="text-2xl font-semibold mb-4">Update Booking ID: {selectedBooking.id}</h2>
                        <label className="block mb-2">Service Name:</label>
                        <input 
                            type="text" 
                            name="service_name" 
                            value={updatedData.service_name || selectedBooking.service_name} 
                            onChange={handleInputChange} 
                            className="border p-2 mb-4 w-full"
                        />
                        <label className="block mb-2">Price:</label>
                        <input 
                            type="number" 
                            name="price" 
                            value={updatedData.price || selectedBooking.price} 
                            onChange={handleInputChange} 
                            className="border p-2 mb-4 w-full"
                        />
                        {/* Add more fields as needed */}
                        <button 
                            onClick={() => handleUpdateBooking(selectedBooking.id)} 
                            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            Save Changes
                        </button>
                        <button 
                            onClick={() => setSelectedBooking(null)} 
                            className="mt-2 ml-2 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;
