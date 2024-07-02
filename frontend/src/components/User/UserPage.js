import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import Navbar from '../Base/Navbar';
import Hero from '../Base/Hero';
import Products from '../Product';
import Footer from '../Base/Footer';

const HOST = process.env.REACT_APP_HOST;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;

const UserPage = () => {
  const { publicId } = useParams();
  const [products, setProducts] = useState([]);

  useEffect(() => {
      fetch(`http://${HOST}:${BACKEND_PORT}/api/product/by_user/${publicId}/`)
      .then(response => response.json())
      .then(data => {
        setProducts(data);
      })
      .catch(error => console.error('Error:', error));
  }, [ publicId ]);

  return (
    <div className="UserPage">
      <Navbar />
      <Hero />
      <Products products={products} />
      <Footer />
    </div>
  );
};

export default UserPage;