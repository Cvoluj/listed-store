import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import Hero from './Hero';
import Products from '../Product';
import Footer from './Footer';
import jwtApi from '../../api/jwtApi';

const Content = () => {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchProductData = async () => {
    try{
      const response = await jwtApi.get(`product/?page=${page}`)
      setProducts(response.data.results);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error("Error", error);
    }
    }
    fetchProductData()
  }, [page]);

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  return (
    <div className="Content">
      <Navbar />
      <Hero />
      <Products products={products} />
      <Footer />
    </div>
  );
};

export default Content;