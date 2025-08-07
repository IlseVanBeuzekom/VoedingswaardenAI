<template>
    <div class="shopping-item" :class="{ 'checked': item.checked }">
      <label class="item-checkbox">
        <input
          v-model="item.checked"
          type="checkbox"
          @change="$emit('toggle', item)"
        />
        <span class="checkmark"></span>
      </label>
      
      <div class="item-details">
        <span class="item-amount">{{ formatAmount(item.amount) }} {{ item.unit }}</span>
        <span class="item-name">{{ item.product_name }}</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ShoppingListItem',
    emits: ['toggle'],
    props: {
      item: {
        type: Object,
        required: true
      }
    },
    setup() {
      const formatAmount = (amount) => {
        // Round to 1 decimal place and remove trailing zeros
        return parseFloat(amount.toFixed(1));
      };
  
      return {
        formatAmount
      };
    }
  }
  </script>
  
  <style scoped>
  .shopping-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    transition: all 0.2s ease;
  }
  
  .shopping-item:hover {
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .shopping-item.checked {
    background-color: #f9fafb;
    opacity: 0.7;
  }
  
  .shopping-item.checked .item-name {
    text-decoration: line-through;
    color: #6b7280;
  }
  
  .item-checkbox {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  
  .item-checkbox input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }
  
  .checkmark {
    height: 20px;
    width: 20px;
    background-color: #fff;
    border: 2px solid #d1d5db;
    border-radius: 4px;
    position: relative;
    transition: all 0.2s ease;
  }
  
  .item-checkbox:hover input ~ .checkmark {
    border-color: #3b82f6;
  }
  
  .item-checkbox input:checked ~ .checkmark {
    background-color: #3b82f6;
    border-color: #3b82f6;
  }
  
  .checkmark:after {
    content: "";
    position: absolute;
    display: none;
  }
  
  .item-checkbox input:checked ~ .checkmark:after {
    display: block;
  }
  
  .item-checkbox .checkmark:after {
    left: 6px;
    top: 2px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }
  
  .item-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
  }
  
  .item-amount {
    font-size: 14px;
    color: #6b7280;
    font-weight: 500;
  }
  
  .item-name {
    font-size: 16px;
    color: #1f2937;
    font-weight: 500;
  }
  
  @media (max-width: 768px) {
    .shopping-item {
      padding: 10px 12px;
    }
    
    .item-details {
      gap: 0;
    }
  }
  </style>