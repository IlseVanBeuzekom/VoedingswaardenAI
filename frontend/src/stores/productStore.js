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
    },

    async fetchProductById(productId) {
      this.loading = true;
      this.error = null;
      
      try {
        this.currentProduct = await productService.getProductById(productId);
        return this.currentProduct;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Product niet gevonden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateProduct(productId, productData) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedProduct = await productService.updateProduct(productId, productData);
        
        // Update in local products array
        const index = this.products.findIndex(p => p.id === productId);
        if (index !== -1) {
          this.products[index] = updatedProduct;
        }
        
        this.currentProduct = updatedProduct;
        return updatedProduct;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteProduct(productId) {
      this.loading = true;
      this.error = null;
      
      try {
        await productService.deleteProduct(productId);
        
        // Remove from local products array
        this.products = this.products.filter(p => p.id !== productId);
        
        if (this.currentProduct?.id === productId) {
          this.currentProduct = null;
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
