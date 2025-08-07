import { defineStore } from 'pinia';
import shoppingListService from '../services/shoppingListService.js';

export const useShoppingListStore = defineStore('shoppingList', {
  state: () => ({
    items: [],
    loading: false,
    error: null,
    currentMenuId: null
  }),

  getters: {
    checkedItems: (state) => state.items.filter(item => item.checked),
    uncheckedItems: (state) => state.items.filter(item => !item.checked),
    totalItems: (state) => state.items.length,
    checkedCount: (state) => state.items.filter(item => item.checked).length
  },

  actions: {
    async fetchShoppingList(menuId) {
      this.loading = true;
      this.error = null;
      this.currentMenuId = menuId;
      
      try {
        this.items = await shoppingListService.getShoppingList(menuId);
        // Add checked property if not present
        this.items.forEach(item => {
          if (item.checked === undefined) {
            item.checked = false;
          }
        });
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    toggleItem(item) {
      const index = this.items.findIndex(i => 
        i.product_id === item.product_id && i.unit === item.unit
      );
      if (index !== -1) {
        this.items[index].checked = !this.items[index].checked;
      }
    },

    toggleAll(checked) {
      this.items.forEach(item => {
        item.checked = checked;
      });
    },

    clearList() {
      this.items = [];
      this.currentMenuId = null;
      this.error = null;
    }
  }
});