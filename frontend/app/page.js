// frontend/app/page.js (Simplified UI with Polling and Delete)
'use client';

import { useState, useEffect, useCallback } from 'react';
// Import the deleteAudit helper
import { createAudit, fetchAudits, deleteAudit } from '../utils/api'; 

const POLLING_INTERVAL = 5000; // Poll every 5 seconds

export default function Dashboard() {
  const [url, setUrl] = useState('');
  const [audits, setAudits] = useState([]);
  const [isScanning, setIsScanning] = useState(false);
  const [validationError, setValidationError] = useState(null); // NEW: State for URL validation

  const loadAudits = useCallback(async () => {
    try {
      const data = await fetchAudits();
      setAudits(data);
      return data;
    } catch (error) {
      console.error("Failed to fetch audits:", error);
      return [];
    }
  }, []);

  // --- POLLING LOGIC ---
  useEffect(() => {
    loadAudits();
    
    let intervalId;

    if (isScanning && url) { 
        setValidationError(null); // Clear error when starting scan
        
        try {
            const submittedUrlBase = new URL(url).origin + new URL(url).pathname;
        
            intervalId = setInterval(async () => {
                const latestAudits = await loadAudits();
                
                const isNewRecordFound = latestAudits.some(audit => 
                    audit.url.startsWith(submittedUrlBase) && audit.title
                );
                
                if (isNewRecordFound) {
                    clearInterval(intervalId);
                    setIsScanning(false);
                }
            }, POLLING_INTERVAL); 
        } catch (e) {
            // This catches the 'Invalid URL' error during polling cleanup
            console.error("Polling stopped due to unexpected URL format:", e);
            setIsScanning(false);
        }
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isScanning, url, loadAudits]); 

  // --- DELETE HANDLER ---
  const handleDelete = async (id) => {
    // Call the API endpoint to delete the record
    await deleteAudit(id); 
    // Immediately refresh the local list to show the removal
    loadAudits(); 
  };

  // --- SUBMISSION HANDLER (Updated for Validation) ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setValidationError(null);

    // NEW: 2. Input Validation Check
    if (!url) {
        setValidationError("URL field cannot be empty.");
        return;
    }
    
    // Check if URL is valid before proceeding
    try {
        new URL(url);
    } catch (e) {
        setValidationError("Invalid URL. Please include http:// or https://");
        return;
    }
    
    // 3. Start Scan and Polling
    setIsScanning(true); 
    await createAudit(url);
    // Note: url state is kept for polling reference, cleared only when polling stops
  };
  
  // --- Rendering ---
  const statusText = isScanning ? "Scanning..." : "Start Scan";

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-2xl font-bold mb-4 text-center">Arcnetic Spider Interface</h1>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded shadow-md">
        <h2 className="text-lg font-semibold mb-3">Submit New URL</h2>
        <div className="flex space-x-2">
          <input
            type="text" // Changed to text to handle initial invalid input better
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL (e.g., https://playwright.dev/)"
            required
            className="flex-grow p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            disabled={isScanning}
          />
          <button
            type="submit"
            disabled={isScanning || !url}
            className={`px-4 py-2 rounded font-semibold transition duration-150 ${
              isScanning
                ? 'bg-yellow-500 text-white cursor-wait'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {statusText}
          </button>
        </div>
        
        {/* NEW: Validation Error Message */}
        {validationError && (
            <p className="mt-2 text-sm text-red-600 font-medium">{validationError}</p>
        )}
      </form>

      {/* History List */}
      <h2 className="text-lg font-semibold mb-3 border-t pt-4">Recent Scan History</h2>
      {audits.length === 0 ? (
        <p className="italic text-gray-500">No scan history found.</p>
      ) : (
        <ul className="list-none space-y-3">
          {audits.map((audit) => (
            <li key={audit.id} className="p-3 border rounded bg-gray-50 flex flex-col justify-between items-start break-words">
                {/* Top Row: ID, URL, Delete Button */}
                <div className="flex justify-between w-full items-center mb-2">
                    <div>
                        <span className="font-bold text-lg text-gray-900">ID {audit.id}:</span> 
                        <span className="text-sm text-lg text-gray-900">{audit.url}</span>
                    </div>
                    {/* Delete Button */}
                    <button
                        onClick={() => handleDelete(audit.id)}
                        className="ml-4 px-3 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600 transition"
                    >
                        Delete
                    </button>
                </div>

                {/* Screenshot Renderer (The Cool Part) */}
                {audit.screenshot_b64 ? (
                    <div className="mt-3 w-full">
                        <p className="text-xs text-gray-700 mb-1">Page Title: {audit.title || 'N/A'}</p>
                        <p className="text-xs font-medium mb-1">Screenshot Evidence:</p>
                        
                        {/* Core Rendering Logic */}
                        <img
                            src={`data:image/png;base64,${audit.screenshot_b64}`}
                            alt={`Screenshot of ${audit.url}`}
                            // Tailwind classes for display control
                            className="border rounded shadow-md max-w-full h-auto"
                        />
                    </div>
                ) : (
                    // Show processing status if the Base64 string is null (crawl is ongoing/failed)
                    <div className="text-xs text-gray-500 italic mt-2">Title: {audit.title || 'Processing...'} (Screenshot pending)</div>
                )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}