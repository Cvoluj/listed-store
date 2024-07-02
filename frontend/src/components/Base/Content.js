import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import Hero from './Hero';
import Products from './Product';
import Footer from './Footer';


const Content = () => {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/product/?page=${page}`)
      .then(response => response.json())
      .then(data => {
        setProducts(data.results);
        setTotalPages(data.total_pages);
      })
      .catch(error => console.error('Error:', error));
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