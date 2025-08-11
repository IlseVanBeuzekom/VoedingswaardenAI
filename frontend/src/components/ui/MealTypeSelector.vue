<template>
    <div class="meal-type-selector">
      <label class="selector-label">Eetmoment</label>
      <select 
        :value="modelValue" 
        @input="$emit('update:modelValue', $event.target.value)"
        class="meal-select"
        required
      >
        <option value="">Kies eetmoment</option>
        <option value="ontbijt">🍳 Ontbijt</option>
        <option value="lunch">🥪 Lunch</option>
        <option value="diner">🍽️ Diner</option>
        <option value="tussendoortje">🍎 Tussendoortje</option>
      </select>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MealTypeSelector',
    emits: ['update:modelValue'],
    props: {
      modelValue: {
        type: String,
        default: ''
      }
    }
  }
  </script>
  
  <style scoped>
  .meal-type-selector {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .selector-label {
    font-size: 14px;
    font-weight: 500;
    color: #374151;
  }
  
  .meal-select {
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    background: white;
  }
  
  .meal-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  </style>