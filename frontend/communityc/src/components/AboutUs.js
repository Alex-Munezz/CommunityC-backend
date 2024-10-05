import React from 'react';

const AboutUs = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">About Us</h1>
      <section className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
        <p className="text-gray-700 mb-4">
          At CommunityCrafters, our mission is to connect people with high-quality, trusted local service providers to meet their everyday needs. We are dedicated to providing a platform where you can easily find and book professional services, ensuring convenience, reliability, and satisfaction.
        </p>
        <p className="text-gray-700">
          Our team is committed to curating the best service providers in various fields, including plumbing, electrical work, personal grooming, and more. We strive to make your experience seamless and enjoyable, and our customer support team is always here to assist you with any questions or concerns.
        </p>
      </section>
      <section className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold mb-4">Our Team</h2>
        <p className="text-gray-700">
          Our team comprises experienced professionals who are passionate about delivering top-notch service. We work tirelessly to ensure that each service provider meets our high standards of quality and reliability. Get to know more about our team and their dedication to excellence.
        </p>
      </section>
    </div>
  );
};

export default AboutUs;
