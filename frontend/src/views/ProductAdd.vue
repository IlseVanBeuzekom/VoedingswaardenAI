<template>
    <div class="product-add">
      <ProductForm
        :loading="productStore.loading"
        :error="productStore.error"
        @submit="handleProductSubmit"
        @cancel="$router.push('/')"
      />
    </div>
  </template>
  
  <script>
  import { useProductStore } from '../stores/productStore.js';
  import { useRouter } from 'vue-router';
  import ProductForm from '../components/forms/ProductForm.vue';
  
  export default {
    name: 'ProductAdd',
    components: {
      ProductForm
    },
    setup() {
      const productStore = useProductStore();
      const router = useRouter();
  
      const handleProductSubmit = async (productData) => {
        try {
          await productStore.createProduct(productData);
          router.push('/products');
        } catch (error) {
          console.error('Error creating product:', error);
        }
      };
  
      return {
        productStore,
        handleProductSubmit
      };
    }
  }
  </script>
  
  <style scoped>
  .product-add {
    padding: 24px;
  }
  </style>