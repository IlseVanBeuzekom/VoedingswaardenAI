<template>
    <div class="product-edit">
      <div v-if="productStore.loading" class="loading">
        Product laden...
      </div>
  
      <div v-else-if="productStore.error" class="error">
        {{ productStore.error }}
        <BaseButton 
          @click="$router.push('/products')"
          variant="secondary"
        >
          Terug naar overzicht
        </BaseButton>
      </div>
  
      <ProductForm
        v-else-if="productStore.currentProduct"
        :loading="productStore.loading"
        :error="productStore.error"
        :initial-data="productStore.currentProduct"
        @submit="handleProductUpdate"
        @cancel="$router.push('/products')"
        mode="edit"
      />
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useProductStore } from '../stores/productStore.js';
  import ProductForm from '../components/forms/ProductForm.vue';
  import BaseButton from '../components/ui/BaseButton.vue';
  
  export default {
    name: 'ProductEdit',
    components: {
      ProductForm,
      BaseButton
    },
    setup() {
      const route = useRoute();
      const router = useRouter();
      const productStore = useProductStore();
  
      const productId = parseInt(route.params.id);
  
      onMounted(async () => {
        try {
          await productStore.fetchProductById(productId);
        } catch (error) {
          console.error('Error loading product:', error);
        }
      });
  
      const handleProductUpdate = async (productData) => {
        try {
          await productStore.updateProduct(productId, productData);
          router.push('/products');
        } catch (error) {
          console.error('Error updating product:', error);
        }
      };
  
      return {
        productStore,
        handleProductUpdate
      };
    }
  }
  </script>
  
  <style scoped>
  .product-edit {
    padding: 24px;
  }
  
  .loading, .error {
    text-align: center;
    padding: 48px 24px;
  }
  
  .error {
    color: #dc2626;
    background-color: #fef2f2;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
  </style>
  