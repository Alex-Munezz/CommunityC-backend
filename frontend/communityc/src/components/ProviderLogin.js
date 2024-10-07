import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const ProviderLogin = () => {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(''); // Reset error message

        try {
            const response = await fetch('/service-provider/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, password }),
            });

            if (!response.ok) {
                throw new Error('Invalid credentials');
            }

            const data = await response.json();
            const { access_token, provider_id } = data;

            // Store the access token in local storage
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('provider_id', provider_id);

            // Navigate after successful login (optional)
            navigate('/provider-dashboard'); // Redirect to dashboard or another page

        } catch (error) {
            setError(error.message || 'An error occurred. Please try again later.');
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="w-full max-w-md bg-white p-8 rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold mb-6 text-gray-900">Service Provider Login</h2>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <form onSubmit={handleLogin}>
                    <div className="mb-4">
                        <label className="required block text-gray-700">Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded"
                            placeholder="Enter your name"
                            required
                        />
                    </div>
                    <div className="mb-6">
                        <label className="required block text-gray-700">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded"
                            placeholder="Enter your password"
                            required
                        />
                    </div>
                    <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
                        Login
                    </button>
                    <br /><br />
                    <p className="text-gray-600">Don't have an account?
                        <Link to='/signup' className="text-blue-500 hover:text-blue-700 font-semibold ml-1">Sign Up</Link>
                    </p>
                    <br />
                    <p className="text-gray-600">Already a user?
                        <Link to='/login' className="text-blue-500 hover:text-blue-700 font-semibold ml-1">Log in here</Link>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default ProviderLogin;
