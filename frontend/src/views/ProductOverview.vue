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
        <div class="card-actions">
          <button 
            @click="editProduct(product.id)"
            class="action-btn edit-btn"
            title="Product bewerken"
          >
            ✏️
          </button>
          <button 
            @click="deleteProduct(product.id)"
            class="action-btn delete-btn"
            title="Product verwijderen"
          >
            ❌
          </button>
        </div>

        <h3>{{ product.name }}</h3>
        <div class="serving-info">
          <span class="serving-size">Per {{ product.getServingDisplay() }}</span>
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
        <div class="per-100g" v-if="product.serving_unit !== 'gram' || product.serving_amount !== 100">
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
import { useRouter } from 'vue-router';
import { useProductStore } from '../stores/productStore.js';
import BaseButton from '../components/ui/BaseButton.vue';

export default {
  name: 'ProductOverview',
  components: {
    BaseButton
  },
  setup() {
    const productStore = useProductStore();
    const router = useRouter();

    onMounted(async () => {
      await productStore.fetchProducts();
    });

    const getPer100gDisplay = (product) => {
      if (product.serving_unit === 'stuk') {
        return 'Niet beschikbaar voor stuks';
      }
      
      const per100g = product.getPer100g();
      return `${per100g.energy_kcal} kcal, ${per100g.fats}g vet, ${per100g.carbohydrates}g kh, ${per100g.proteins}g eiw`;
    };

    const editProduct = (productId) => {
      router.push(`/products/edit/${productId}`);
    };

    const deleteProduct = async (productId) => {
      const product = productStore.products.find(p => p.id === productId);
      if (confirm(`Weet je zeker dat je "${product?.name}" wilt verwijderen?`)) {
        try {
          await productStore.deleteProduct(productId);
        } catch (error) {
          console.error('Error deleting product:', error);
        }
      }
    };

    return {
      productStore,
      getPer100gDisplay,
      editProduct,
      deleteProduct
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

.card-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.edit-btn:hover {
  border-color: #3b82f6;
}

.delete-btn:hover {
  border-color: #ef4444;
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
  position: relative;
}

.product-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.product-card h3 {
  margin: 0 0 8px 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.serving-info {
  margin-bottom: 16px;
}

.serving-size {
  display: inline-block;
  background: #f3f4f6;
  color: #374151;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.nutrition-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
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

.per-100g {
  border-top: 1px solid #e5e7eb;
  padding-top: 12px;
}

.per-100g h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6b7280;
  font-weight: 600;
}

.nutrition-compact {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.4;
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