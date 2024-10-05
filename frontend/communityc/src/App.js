import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import SignUp from './components/SignUp';
import BookingPage from './components/BookingPage';
import BookedServicePage from './components/BookedServicePage';
import CheckOut from './components/Checkout';
import AboutUs from './components/AboutUs';
import ContactUs from './components/ContactUs';
import { useAuth } from './components/AuthContext'; 
import AdminDashboard from './components/AdminDashboard';
import UserDashboard from './components/UserDashboard';
import Terms from './components/Terms';

function App() {
  const { isAuthenticated } = useAuth();
  return (
     <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={!isAuthenticated ? <Login /> : <LandingPage />} />
            <Route path="/signup" element={!isAuthenticated ? <SignUp /> : <LandingPage />} />
            <Route path="/checkout" element={<CheckOut />} />
            <Route path="/about" element={<AboutUs />} />
            <Route path="/contacts" element={<ContactUs />} />
            <Route path="/book/:name" element={<BookingPage />} />
            <Route path="/booked-service" element={<BookedServicePage />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/dashboard" element={<UserDashboard />} />
            <Route path="/terms" element={<Terms />} />
          </Routes>
        </div>
        <Footer />
      </div>
    
  );
}

export default App;
