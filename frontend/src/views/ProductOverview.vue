<template>
    <div class="product-overview">
      <div class="header">
        <h1>Product Overzicht</h1>
        <BaseButton 
          @click="$router.push('/products/add')"
          variant="primary"
        >
          Nieuw Product
        </BaseButton>
      </div>
  
      <div v-if="productStore.loading" class="loading">
        Producten laden...
      </div>
  
      <div v-else-if="productStore.error" class="error">
        {{ productStore.error }}
      </div>
  
      <div v-else-if="productStore.products.length === 0" class="empty-state">
        <p>Nog geen producten toegevoegd.</p>
        <BaseButton 
          @click="$router.push('/products/add')"
          variant="primary"
        >
          Voeg je eerste product toe
        </BaseButton>
      </div>
  
      <div v-else class="products-grid">
        <div 
          v-for="product in productStore.products" 
          :key="product.id"
          class="product-card"
        >
          <h3>{{ product.name }}</h3>
          <div class="serving-info">
            <span class="serving-size">Per {{ product.serving_size }}g</span>
          </div>
          <div class="nutrition-info">
            <div class="nutrition-row">
              <span>Energie:</span>
              <span>{{ product.energy_kcal }} kcal</span>
            </div>
            <div class="nutrition-row">
              <span>Vetten:</span>
              <span>{{ product.fats }}g</span>
            </div>
            <div class="nutrition-row">
              <span>Koolhydraten:</span>
              <span>{{ product.carbohydrates }}g</span>
            </div>
            <div class="nutrition-row">
              <span>Eiwitten:</span>
              <span>{{ product.proteins }}g</span>
            </div>
          </div>
          <div class="per-100g" v-if="product.serving_size !== 100">
            <h4>Per 100g:</h4>
            <div class="nutrition-compact">
              {{ getPer100gDisplay(product) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  import { useProductStore } from '../stores/productStore.js';
  import BaseButton from '../components/ui/BaseButton.vue';
  
  export default {
    name: 'ProductOverview',
    components: {
      BaseButton
    },
    setup() {
      const productStore = useProductStore();
  
      onMounted(async () => {
        await productStore.fetchProducts();
      });

      const getPer100gDisplay = (product) => {
        const per100g = product.getPer100g();
        return `${per100g.energy_kcal} kcal, ${per100g.fats}g vet, ${per100g.carbohydrates}g kh, ${per100g.proteins}g eiw`;
      };
  
      return {
        productStore,
        getPer100gDisplay
      };
    }
  }
  </script>
  
  <style scoped>
  .product-overview {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }
  
  .header h1 {
    color: #1f2937;
    margin: 0;
  }
  
  .loading, .error, .empty-state {
    text-align: center;
    padding: 48px 24px;
  }
  
  .error {
    color: #dc2626;
    background-color: #fef2f2;
    border-radius: 8px;
  }
  
  .empty-state p {
    color: #6b7280;
    margin-bottom: 24px;
  }
  
  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
  }
  
  .product-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    transition: box-shadow 0.2s ease;
  }
  
  .product-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  
  .product-card h3 {
    margin: 0 0 16px 0;
    color: #1f2937;
    font-size: 1.25rem;
  }
  
  .nutrition-info {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .nutrition-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .nutrition-row span:first-child {
    color: #6b7280;
  }
  
  .nutrition-row span:last-child {
    font-weight: 500;
    color: #1f2937;
  }
  
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
    
    .products-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>
  