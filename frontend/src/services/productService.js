import axios from 'axios';
import { Product } from '../models/Product.js';

const API_BASE_URL = 'http://localhost:8000/api';

class ProductService {
  async createProduct(productData) {
    const response = await axios.post(`${API_BASE_URL}/products/`, productData);
    return Product.fromAPI(response.data);
  }

  async getAllProducts() {
    const response = await axios.get(`${API_BASE_URL}/products/`);
    return response.data.map(product => Product.fromAPI(product));
  }

  async getProductById(productId) {
    const response = await axios.get(`${API_BASE_URL}/products/${productId}`);
    return Product.fromAPI(response.data);
  }

  async updateProduct(productId, productData) {
    const response = await axios.put(`${API_BASE_URL}/products/${productId}`, productData);
    return Product.fromAPI(response.data);
  }

  async deleteProduct(productId) {
    await axios.delete(`${API_BASE_URL}/products/${productId}`);
  }
}

export default new ProductService();
