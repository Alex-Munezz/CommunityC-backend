import React, { useEffect, useState } from 'react';

const ProviderBookings = () => {
    const [bookings, setBookings] = useState([]);
    const [error, setError] = useState('');
    
    useEffect(() => {
        const fetchBookings = async () => {
            const token = localStorage.getItem('access_token'); // Get token from local storage

            try {
                const response = await fetch('/service-provider/bookings', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`, // Include the token in the headers
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch bookings');
                }

                const data = await response.json();
                setBookings(data);
            } catch (error) {
                setError(error.message || 'An error occurred while fetching bookings.');
            }
        };

        fetchBookings();
    }, []);

    return (
        <div className="container mx-auto p-4">
            <h2 className="text-2xl font-bold mb-4">Your Bookings</h2>
            {error && <p className="text-red-500">{error}</p>}
            {bookings.length === 0 ? (
                <p>No bookings found.</p>
            ) : (
                <ul className="space-y-4">
                    {bookings.map((booking) => (
                        <li key={booking.id} className="border p-4 rounded shadow">
                            <h3 className="font-semibold">{booking.service_name}</h3>
                            <p><strong>Name:</strong> {booking.name}</p>
                            <p><strong>Email:</strong> {booking.email}</p>
                            <p><strong>Phone Number:</strong> {booking.phone_number}</p>
                            <p><strong>Location:</strong> {booking.street}, {booking.town}, {booking.county}</p>
                            <p><strong>Date:</strong> {booking.date}</p>
                            <p><strong>Time:</strong> {booking.time}</p>
                            <p><strong>Price:</strong> {booking.price} Kshs</p>
                            <p><strong>Additional Info:</strong> {booking.additional_info}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ProviderBookings;
