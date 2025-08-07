<template>
    <div class="shopping-list">
      <div class="header">
        <h1>Boodschappenlijst</h1>
        
        <BaseButton 
          @click="$router.back()"
          variant="secondary"
          size="small"
        >
          ← Terug
        </BaseButton>
      </div>
  
      <div v-if="shoppingStore.loading" class="loading">
        Boodschappenlijst laden...
      </div>
  
      <div v-else-if="shoppingStore.error" class="error-message">
        {{ shoppingStore.error }}
      </div>
  
      <div v-else-if="shoppingStore.items.length === 0" class="empty-state">
        <h2>Geen items gevonden</h2>
        <p>Er staan geen recepten met ingrediënten in het geselecteerde weekmenu.</p>
      </div>
  
      <div v-else class="shopping-content">
        <div class="list-controls">
          <div class="progress-info">
            <span class="progress-text">
              {{ shoppingStore.checkedCount }} van {{ shoppingStore.totalItems }} afgevinkt
            </span>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
          </div>
  
          <div class="toggle-controls">
            <BaseButton 
              @click="shoppingStore.toggleAll(false)"
              variant="secondary"
              size="small"
            >
              Alles uit
            </BaseButton>
            <BaseButton 
              @click="shoppingStore.toggleAll(true)"
              variant="secondary"
              size="small"
            >
              Alles aan
            </BaseButton>
            <BaseButton 
              @click="shoppingStore.exportToTxt"
              variant="primary"
              size="small"
              :disabled="shoppingStore.uncheckedItems.length === 0"
            >
              📄 Exporteer
            </BaseButton>
          </div>
        </div>
  
        <AddItemForm @addItem="shoppingStore.addCustomItem" />

        <div class="shopping-sections">
          <!-- Unchecked items -->
          <div v-if="shoppingStore.uncheckedItems.length > 0" class="section">
            <h3>Te kopen ({{ shoppingStore.uncheckedItems.length }})</h3>
            <div class="items-grid">
              <ShoppingListItem
                v-for="item in shoppingStore.uncheckedItems"
                :key="`${item.product_id}_${item.unit}`"
                :item="item"
                @toggle="shoppingStore.toggleItem"
                @remove="shoppingStore.removeItem"
                @updateAmount="shoppingStore.updateItemAmount"
                @updateUnit="shoppingStore.updateItemUnit"
              />
            </div>
          </div>
  
          <!-- Checked items -->
          <div v-if="shoppingStore.checkedItems.length > 0" class="section checked-section">
            <h3>Afgevinkt ({{ shoppingStore.checkedItems.length }})</h3>
            <div class="items-grid">
              <ShoppingListItem
                v-for="item in shoppingStore.checkedItems"
                :key="`${item.product_id}_${item.unit}`"
                :item="item"
                @toggle="shoppingStore.toggleItem"
                @remove="shoppingStore.removeItem"
                @updateAmount="shoppingStore.updateItemAmount"
                @updateUnit="shoppingStore.updateItemUnit"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { computed, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useShoppingListStore } from '../stores/shoppingListStore.js';
  import ShoppingListItem from '../components/ui/ShoppingListItem.vue';
  import BaseButton from '../components/ui/BaseButton.vue';
  import AddItemForm from '../components/ui/AddItemForm.vue'
  
  export default {
    name: 'ShoppingList',
    components: {
      ShoppingListItem,
      BaseButton,
      AddItemForm
    },
    setup() {
      const route = useRoute();
      const router = useRouter();
      const shoppingStore = useShoppingListStore();
  
      const progressPercentage = computed(() => {
        if (shoppingStore.totalItems === 0) return 0;
        return Math.round((shoppingStore.checkedCount / shoppingStore.totalItems) * 100);
      });
  
      onMounted(async () => {
        const menuId = route.params.menuId;
        if (menuId) {
          try {
            await shoppingStore.fetchShoppingList(parseInt(menuId));
          } catch (error) {
            console.error('Error loading shopping list:', error);
          }
        } else {
          router.push('/weekmenu');
        }
      });
  
      return {
        shoppingStore,
        progressPercentage
      };
    }
  }
  </script>
  
  <style scoped>
  .shopping-list {
    max-width: 800px;
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
  
  .loading {
    text-align: center;
    padding: 48px 24px;
    color: #6b7280;
  }
  
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    text-align: center;
  }
  
  .empty-state {
    text-align: center;
    padding: 48px 24px;
    color: #6b7280;
  }
  
  .empty-state h2 {
    color: #1f2937;
    margin-bottom: 8px;
  }
  
  .list-controls {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }
  
  .progress-info {
    flex: 1;
  }
  
  .progress-text {
    display: block;
    font-size: 14px;
    color: #374151;
    margin-bottom: 8px;
    font-weight: 500;
  }
  
  .progress-bar {
    width: 100%;
    height: 8px;
    background-color: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
  }
  
  .progress-fill {
    height: 100%;
    background-color: #10b981;
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  
  .toggle-controls {
    display: flex;
    gap: 8px;
  }
  
  .shopping-sections {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .section h3 {
    color: #1f2937;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e5e7eb;
  }
  
  .checked-section h3 {
    color: #6b7280;
    border-bottom-color: #d1d5db;
  }
  
  .items-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      align-items: stretch;
      gap: 16px;
    }
  
    .header h1 {
      text-align: center;
    }
  
    .list-controls {
      flex-direction: column;
      align-items: stretch;
      gap: 16px;
    }
  
    .toggle-controls {
      justify-content: center;
    }
  }
  </style>