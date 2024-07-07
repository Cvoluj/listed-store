import React, { useState, useEffect } from 'react';
import jwtApi from '../../api/jwtApi';


const Hero = ({ public_id }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await jwtApi.get(`user/${public_id}/`);
                setUser(response.data);
                setLoading(false);
            } catch (error) {
              if (error.response && error.response.status === 401) {
                setError('You must be signed in to view other user\'s information.');
              } else {
                  setError('Error loading user data');
              }
                setLoading(false);
            }
        };

        fetchUserData();
    }, [public_id]);

    if (loading) return <div className="jumbotron text-center">Loading...</div>;
    if (error) return <div className="jumbotron text-center">{error}</div>;

    return (
        <div className="jumbotron text-center">
            <div className="container">
                <h1 className="display-4">{user.username}!</h1>
                <p className="lead">Name: {user.first_name} {user.last_name}</p>
                <p>Email: {user.email}</p>
                <p>Member since: {new Date(user.created).toLocaleDateString()}</p>
            </div>
        </div>
    );
};

export default Hero;
