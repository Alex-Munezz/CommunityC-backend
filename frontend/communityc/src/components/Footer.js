import React from 'react';

function Footer() {
  return (
    <footer className="bg-gray-800 text-white text-center py-6">
      <div className="container mx-auto px-4">
        <div className="mb-4">
          <p className="text-sm">&copy; 2024 CommunityCrafters. All rights reserved.</p>
        </div>
        <div className="mb-4">
          <p className="text-lg font-semibold">Contact Us</p>
          <p className="text-sm">
            Email: <a href="mailto:support@serviceprovider.com" className="hover:text-gray-400">support@communitycrafters.com</a><br />
            Phone: <a href="tel:+1234567890" className="hover:text-gray-400">+254768453442</a>
          </p>
        </div>
        <div className="mb-4">
          <p className="text-lg font-semibold">Follow Us</p>
          <div className="flex justify-center space-x-4 mt-2">
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">Facebook</a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">Twitter</a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">Instagram</a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">LinkedIn</a>
          </div>
        </div>
        <div className="mt-4">
          <a href="#" className="hover:text-gray-400">Privacy Policy</a>
          <span className="mx-2">|</span>
          <a href="#" className="hover:text-gray-400">Terms of Service</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
