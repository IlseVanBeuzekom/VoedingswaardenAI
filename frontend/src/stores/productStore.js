import { defineStore } from 'pinia';
import productService from '../services/productService.js';
import { Product } from '../models/Product.js';

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    loading: false,
    error: null
  }),

  actions: {
    async createProduct(productData) {
      this.loading = true;
      this.error = null;
      
      try {
        const newProduct = await productService.createProduct(productData);
        this.products.push(newProduct);
        return newProduct;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchProducts() {
      this.loading = true;
      this.error = null;
      
      try {
        this.products = await productService.getAllProducts();
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
