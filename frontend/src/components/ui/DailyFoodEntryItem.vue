<template>
    <tr class="entry-row">
      <td class="name-cell">
        <div class="item-info">
          <span class="item-name">{{ entry.getName() }}</span>
          <span class="item-type">{{ entry.getType() === 'product' ? 'Product' : 'Recept' }}</span>
        </div>
      </td>
      <td class="amount-cell">
        {{ formatValue(entry.amount) }} {{ entry.unit }}
      </td>
      <td class="nutrition-cell">
        {{ Math.round(nutrition.energy_kcal) }} kcal
      </td>
      <td class="nutrition-cell">
        {{ formatValue(nutrition.proteins) }}g
      </td>
      <td class="nutrition-cell">
        {{ formatValue(nutrition.fats) }}g
      </td>
      <td class="nutrition-cell">
        {{ formatValue(nutrition.carbohydrates) }}g
      </td>
      <td class="nutrition-cell">
        {{ formatValue(nutrition.sugars) }}g
      </td>
      <td class="nutrition-cell">
        {{ formatValue(nutrition.fibers) }}g
      </td>
      <td v-if="showActions" class="actions-cell">
        <button 
          @click="$emit('edit', entry)"
          class="action-btn edit-btn"
          title="Bewerken"
        >
          ✏️
        </button>
        <button 
          @click="$emit('delete', entry)"
          class="action-btn delete-btn"
          title="Verwijderen"
        >
          ❌
        </button>
      </td>
    </tr>
  </template>
  
  <script>
  import { computed } from 'vue';
  
  export default {
    name: 'DailyFoodEntryItem',
    emits: ['edit', 'delete'],
    props: {
      entry: {
        type: Object,
        required: true
      },
      showActions: {
        type: Boolean,
        default: true
      }
    },
    setup(props) {
      const nutrition = computed(() => {
        return props.entry.calculateNutrition();
      });
  
      const formatValue = (value) => {
        return Math.round(value * 10) / 10;
      };
  
      return {
        nutrition,
        formatValue
      };
    }
  }
  </script>
  
  <style scoped>
  .entry-row {
    border-bottom: 1px solid #e5e7eb;
  }
  
  .entry-row:hover {
    background-color: #f9fafb;
  }
  
  .name-cell {
    padding: 12px 16px;
  }
  
  .item-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .item-name {
    font-weight: 500;
    color: #1f2937;
  }
  
  .item-type {
    font-size: 12px;
    color: #6b7280;
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    align-self: flex-start;
  }
  
  .amount-cell,
  .nutrition-cell {
    padding: 12px 8px;
    text-align: center;
    font-size: 14px;
    color: #374151;
  }
  
  .actions-cell {
    padding: 12px 16px;
    text-align: center;
  }
  
  .action-btn {
    background: none;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    width: 28px;
    height: 28px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 12px;
    margin: 0 2px;
    transition: all 0.2s ease;
  }
  
  .action-btn:hover {
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .edit-btn:hover {
    border-color: #3b82f6;
  }
  
  .delete-btn:hover {
    border-color: #ef4444;
  }
  
  @media (max-width: 768px) {
    .nutrition-cell {
      display: none;
    }
    
    .amount-cell {
      font-size: 12px;
    }
  }
  </style>