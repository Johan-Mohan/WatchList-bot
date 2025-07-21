// frontend/src/App.js

import React, { useState, useEffect } from 'react';

// Mock Telegram Web App object for development in a standard browser
const mockTelegram = {
  WebApp: {
    initDataUnsafe: {
      user: {
        id: 12345678,
        first_name: 'John',
        last_name: 'Doe',
        username: 'johndoe',
      },
    },
    ready: () => {},
    expand: () => {},
  },
};

// Use the mock object if window.Telegram is not available
const Telegram = window.Telegram || mockTelegram;

function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState('home'); // home, search, profile

  useEffect(() => {
    // Initialize the Telegram Web App SDK
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();
    
    // Get user data from Telegram
    const initData = Telegram.WebApp.initDataUnsafe;
    if (initData && initData.user) {
      setUser(initData.user);
    }
  }, []);

  const renderPage = () => {
    switch (page) {
      case 'search':
        return <SearchPage />;
      case 'profile':
        return <ProfilePage user={user} />;
      case 'home':
      default:
        return <HomePage user={user} />;
    }
  };

  return (
    <div className="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white min-h-screen font-sans">
      <div className="container mx-auto p-4">
        <header className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Movie Tracker</h1>
          <nav>
            <button onClick={() => setPage('home')} className={`mr-2 px-3 py-1 rounded ${page === 'home' ? 'bg-blue-500 text-white' : ''}`}>Home</button>
            <button onClick={() => setPage('search')} className={`mr-2 px-3 py-1 rounded ${page === 'search' ? 'bg-blue-500 text-white' : ''}`}>Search</button>
            <button onClick={() => setPage('profile')} className={`px-3 py-1 rounded ${page === 'profile' ? 'bg-blue-500 text-white' : ''}`}>Profile</button>
          </nav>
        </header>
        
        <main>
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

const HomePage = ({ user }) => (
  <div>
    <h2 className="text-xl font-semibold mb-2">Welcome, {user ? user.first_name : 'Guest'}!</h2>
    <p>This is your watched list. (Functionality to be implemented)</p>
  </div>
);

const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query) return;
        setLoading(true);
        try {
            const response = await fetch(`/api/movies/search?query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setResults(data);
        } catch (error) {
            console.error("Search failed:", error);
            // Here you would show an error message to the user
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2 className="text-xl font-semibold mb-2">Search for a Movie</h2>
            <form onSubmit={handleSearch} className="flex mb-4">
                <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g., The Matrix" 
                    className="flex-grow p-2 rounded-l-md text-black"
                />
                <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-r-md">Search</button>
            </form>
            {loading && <p>Loading...</p>}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {results.map(movie => (
                    <div key={movie.tmdb_id} className="bg-gray-200 dark:bg-gray-800 rounded-lg overflow-hidden">
                        {movie.poster_path ? (
                           <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={`${movie.title} poster`} className="w-full h-auto" />
                        ) : (
                            <div className="w-full h-48 bg-gray-300 dark:bg-gray-700 flex items-center justify-center">No Image</div>
                        )}
                        <div className="p-2">
                            <h3 className="font-bold text-sm">{movie.title}</h3>
                            <p className="text-xs text-gray-600 dark:text-gray-400">{movie.release_date}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};


const ProfilePage = ({ user }) => (
  <div>
    <h2 className="text-xl font-semibold mb-2">Profile</h2>
    {user && (
      <div>
        <p><strong>ID:</strong> {user.id}</p>
        <p><strong>Username:</strong> @{user.username}</p>
        <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
      </div>
    )}
    <div className="mt-4">
        <h3 className="text-lg font-semibold">My Lists</h3>
        <p>(Your custom lists will appear here)</p>
    </div>
  </div>
);


export default App;
