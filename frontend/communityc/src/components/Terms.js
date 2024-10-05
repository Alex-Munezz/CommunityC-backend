import React from 'react';

const TermsAndConditions = () => {
  return (
    <div className="terms-conditions-container p-4 bg-white rounded shadow-md">
      <h2 className="text-xl font-bold mb-4">Terms and Conditions</h2>
      <p className="mb-4">Welcome to CommunityCrafters! By using our website and services, you agree to the following terms and conditions:</p>
      <h3 className="text-lg font-semibold">1. Acceptance of Terms</h3>
      <p className="mb-4">
        By accessing or using CommunityCrafters, you agree to comply with and be bound by these terms and conditions. If you do not agree to these terms, please do not use our services.
      </p>
      <h3 className="text-lg font-semibold">2. User Responsibilities</h3>
      <p className="mb-4">
        You agree to use CommunityCrafters only for lawful purposes and in a manner that does not infringe the rights of, restrict, or inhibit anyone else's use and enjoyment of the website.
      </p>
      <h3 className="text-lg font-semibold">3. Account Security</h3>
      <p className="mb-4">
        You are responsible for maintaining the confidentiality of your account information and for all activities that occur under your account.
      </p>
      <h3 className="text-lg font-semibold">4. Changes to Terms</h3>
      <p className="mb-4">
        We may update these terms from time to time. We will notify you of any changes by posting the new terms on this page. You are advised to review these terms periodically for any changes.
      </p>
      <h3 className="text-lg font-semibold">5. Limitation of Liability</h3>
      <p className="mb-4">
        In no event shall CommunityCrafters be liable for any direct, indirect, incidental, special, or consequential damages arising out of or in any way connected with the use of our services.
      </p>
      <h3 className="text-lg font-semibold">6. Contact Us</h3>
      <p className="mb-4">
        If you have any questions about these terms, please contact us at <a href="mailto:support@communitycrafters.com" className="text-blue-500">support@communitycrafters.com</a>.
      </p>
      <p className="text-sm text-gray-600">
        Last updated: 17/09/2024
      </p>
    </div>
  );
};

export default TermsAndConditions;
