import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import Navbar from '../Base/Navbar';
import Hero from './Hero';
import Products from '../Product';
import Footer from '../Base/Footer';
import jwtApi from '../../api/jwtApi';

const UserPage = () => {
  const { publicId } = useParams();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProductByUser = async () => {
      try {
        const response = await jwtApi.get(`product/by_user/${publicId}/`)
        setProducts(response.data);
      } catch(error) { 
        console.error('Error:', error);
      }
    };

    fetchProductByUser();
  }, [ publicId ]);

  return (
    <div className="UserPage">
      <Navbar />
      <Hero public_id={publicId}/>
      <Products products={products} />
      <Footer />
    </div>
  );
};

export default UserPage;