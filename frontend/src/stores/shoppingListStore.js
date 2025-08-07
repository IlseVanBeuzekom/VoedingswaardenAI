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
    },

    updateItemAmount(item, newAmount) {
      const index = this.items.findIndex(i => 
        i.product_id === item.product_id && i.unit === item.unit && i.product_name === item.product_name
      );
      if (index !== -1) {
        this.items[index].amount = newAmount;
      }
    },
    
    updateItemUnit(item, newUnit) {
      const index = this.items.findIndex(i => 
        i.product_id === item.product_id && i.unit === item.unit && i.product_name === item.product_name
      );
      if (index !== -1) {
        this.items[index].unit = newUnit;
      }
    },
    
    removeItem(item) {
      this.items = this.items.filter(i => 
        !(i.product_id === item.product_id && i.unit === item.unit && i.product_name === item.product_name)
      );
    },
    
    addCustomItem(itemData) {
      // Generate unique product_id for custom items
      const customId = `custom_${Date.now()}`;
      this.items.push({
        ...itemData,
        product_id: customId
      });
    },

    exportToTxt() {
      const uncheckedItems = this.items.filter(item => !item.checked);
      
      if (uncheckedItems.length === 0) {
        return 'Geen items om te exporteren.';
      }
    
      let content = `Boodschappenlijst\n`;
      content += `Gegenereerd op: ${new Date().toLocaleDateString('nl-NL')}\n\n`;
      
      uncheckedItems.forEach(item => {
        content += `- ${item.amount} ${item.unit} ${item.product_name}\n`;
      });
      
      // Download bestand
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `boodschappenlijst-${new Date().toISOString().split('T')[0]}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  }
});