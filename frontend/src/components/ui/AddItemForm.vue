<template>
    <div class="add-item-form">
      <h4>Nieuw item toevoegen</h4>
      <form @submit.prevent="handleSubmit" class="form">
        <input
          v-model.number="form.amount"
          type="number"
          step="0.1"
          min="0.1"
          placeholder="Aantal"
          required
          class="amount-input"
        />
        
        <select v-model="form.unit" required class="unit-select">
          <option value="gram">gram</option>
          <option value="kg">kg</option>
          <option value="ml">ml</option>
          <option value="liter">liter</option>
          <option value="stuk">stuk</option>
          <option value="el">eetlepel</option>
          <option value="tl">theelepel</option>
          <option value="kopje">kopje</option>
        </select>
  
        <input
          v-model="form.product_name"
          type="text"
          placeholder="Productnaam"
          required
          class="product-input"
        />
  
        <BaseButton type="submit" variant="primary" size="small">
          Toevoegen
        </BaseButton>
      </form>
    </div>
  </template>
  
  <script>
  import { reactive } from 'vue';
  import BaseButton from './BaseButton.vue';
  
  export default {
    name: 'AddItemForm',
    components: { BaseButton },
    emits: ['addItem'],
    setup(props, { emit }) {
      const form = reactive({
        amount: null,
        unit: 'gram',
        product_name: ''
      });
  
      const handleSubmit = () => {
        if (form.amount > 0 && form.product_name.trim()) {
          emit('addItem', {
            product_id: null,
            product_name: form.product_name.trim(),
            amount: form.amount,
            unit: form.unit,
            checked: false
          });
          
          // Reset form
          form.amount = null;
          form.product_name = '';
          form.unit = 'gram';
        }
      };
  
      return {
        form,
        handleSubmit
      };
    }
  }
  </script>
  
  <style scoped>
  .add-item-form {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
  }
  
  .add-item-form h4 {
    margin: 0 0 12px 0;
    color: #374151;
    font-size: 14px;
  }
  
  .form {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .amount-input, .unit-select, .product-input {
    padding: 6px 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .amount-input {
    width: 80px;
  }
  
  .unit-select {
    width: 100px;
    background: white;
  }
  
  .product-input {
    flex: 1;
    min-width: 150px;
  }
  </style>