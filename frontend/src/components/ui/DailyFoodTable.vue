<template>
    <div class="table-section">
      <h3 v-if="title">{{ title }}</h3>
      
      <div v-if="loading" class="loading">
        Gegevens laden...
      </div>
  
      <div v-else-if="!entries || entries.length === 0" class="empty-state">
        <p>Nog geen items toegevoegd voor deze dag.</p>
      </div>
  
      <div v-else class="table-container">
        <table class="entries-table">
          <thead>
            <tr>
              <th>Item</th>
              <th>Hoeveelheid</th>
              <th>Energie</th>
              <th>Eiwitten</th>
              <th>Vetten</th>
              <th>Koolhydraten</th>
              <th>Suikers</th>
              <th>Vezels</th>
              <th v-if="showActions">Acties</th>
            </tr>
          </thead>
          <tbody>
            <DailyFoodEntryItem
              v-for="entry in entries"
              :key="entry.id"
              :entry="entry"
              :show-actions="showActions"
              @edit="$emit('edit', entry)"
              @delete="$emit('delete', entry)"
            />
          </tbody>
          <tfoot v-if="entries.length > 0">
            <tr class="totals-row">
              <td class="totals-label"><strong>Totaal</strong></td>
              <td>-</td>
              <td class="totals-value"><strong>{{ Math.round(totalNutrition.energy_kcal) }} kcal</strong></td>
              <td class="totals-value"><strong>{{ formatValue(totalNutrition.proteins) }}g</strong></td>
              <td class="totals-value"><strong>{{ formatValue(totalNutrition.fats) }}g</strong></td>
              <td class="totals-value"><strong>{{ formatValue(totalNutrition.carbohydrates) }}g</strong></td>
              <td class="totals-value"><strong>{{ formatValue(totalNutrition.sugars) }}g</strong></td>
              <td class="totals-value"><strong>{{ formatValue(totalNutrition.fibers) }}g</strong></td>
              <td v-if="showActions">-</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import DailyFoodEntryItem from './DailyFoodEntryItem.vue';
  
  export default {
    name: 'DailyFoodTable',
    components: {
      DailyFoodEntryItem
    },
    emits: ['edit', 'delete'],
    props: {
      entries: {
        type: Array,
        default: () => []
      },
      loading: {
        type: Boolean,
        default: false
      },
      title: {
        type: String,
        default: null
      },
      showActions: {
        type: Boolean,
        default: true
      }
    },
    setup(props) {
      const totalNutrition = computed(() => {
        if (!props.entries || props.entries.length === 0) {
          return { energy_kcal: 0, proteins: 0, fats: 0, carbohydrates: 0, sugars: 0, fibers: 0 };
        }
  
        return props.entries.reduce((totals, entry) => {
          const nutrition = entry.calculateNutrition();
          totals.energy_kcal += nutrition.energy_kcal;
          totals.proteins += nutrition.proteins;
          totals.carbohydrates += nutrition.carbohydrates;
          totals.sugars += nutrition.sugars;
          totals.fats += nutrition.fats;
          totals.fibers += nutrition.fibers;
          return totals;
        }, {
          energy_kcal: 0,
          proteins: 0,
          carbohydrates: 0,
          sugars: 0,
          fats: 0,
          fibers: 0
        });
      });
  
      const formatValue = (value) => {
        return Math.round(value * 10) / 10;
      };
  
      return {
        totalNutrition,
        formatValue
      };
    }
  }
  </script>
  
  <style scoped>
  .table-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
  }
  
  .table-section h3 {
    margin: 0 0 20px 0;
    color: #1f2937;
  }
  
  .loading, .empty-state {
    text-align: center;
    padding: 40px;
    color: #6b7280;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .entries-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
  }
  
  .entries-table th {
    background-color: #f9fafb;
    padding: 12px 8px;
    text-align: center;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #e5e7eb;
    font-size: 14px;
  }
  
  .entries-table th:first-child {
    text-align: left;
    padding-left: 16px;
  }
  
  .totals-row {
    background-color: #f9fafb;
    border-top: 2px solid #e5e7eb;
  }
  
  .totals-label {
    padding: 12px 16px;
    color: #1f2937;
  }
  
  .totals-value {
    padding: 12px 8px;
    text-align: center;
    color: #1f2937;
  }
  
  @media (max-width: 768px) {
    .entries-table th:nth-child(n+4) {
      display: none;
    }
    
    .entries-table {
      font-size: 14px;
    }
  }
  </style>