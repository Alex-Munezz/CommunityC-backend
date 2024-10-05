import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../images/logo.png';
import { useAuth } from './AuthContext'; // Ensure the path is correct

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, logout, userRole } = useAuth(); // Use the auth context

  const handleSignOut = () => {
    logout();
  };

  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/">
          <img src={logo} alt="logo" className="h-14" />
        </Link>
        <div className="hidden md:flex space-x-4">
          <Link to="/" className="text-gray-300 hover:text-white">Home</Link>
          <Link to="/about" className="text-gray-300 hover:text-white">About Us</Link>
          <Link to="/contacts" className="text-gray-300 hover:text-white">Contact Us</Link>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="text-gray-300 hover:text-white">My Dashboard</Link>
              {userRole === 'admin' && (
                <Link to="/admin" className="text-gray-300 hover:text-white">Admin</Link>
              )}
              <button onClick={handleSignOut} className="text-gray-300 hover:text-white">Sign Out</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-300 hover:text-white">Login</Link>
              <Link to="/signup" className="text-gray-300 hover:text-white">Sign Up</Link>
            </>
          )}
        </div>
        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)} className="text-white focus:outline-none">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16m-7 6h7"} />
            </svg>
          </button>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden bg-gray-700 p-4 space-y-4">
          <Link to="/" className="block text-gray-300 hover:text-white">Home</Link>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="block text-gray-300 hover:text-white">My Dashboard</Link>
              {/* Conditionally render the Admin link in mobile view if the user is an admin */}
              {userRole === 'admin' && (
                <Link to="/admin" className="block text-gray-300 hover:text-white">Admin</Link>
              )}
              <button onClick={handleSignOut} className="block text-gray-300 hover:text-white">Sign Out</button>
            </>
          ) : (
            <>
              <Link to="/login" className="block text-gray-300 hover:text-white">Login</Link>
              <Link to="/signup" className="block text-gray-300 hover:text-white">Sign Up</Link>
            </>
          )}
          <Link to="/about" className="block text-gray-300 hover:text-white">About Us</Link>
          <Link to="/contacts" className="block text-gray-300 hover:text-white">Contact Us</Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
