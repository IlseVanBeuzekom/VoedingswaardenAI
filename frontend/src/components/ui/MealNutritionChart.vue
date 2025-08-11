<template>
    <div class="meal-nutrition-chart">
      <div v-if="hasData" class="chart-container">
        <div class="meal-bars">
          <div
            v-for="meal in mealData"
            :key="meal.type"
            class="meal-bar"
          >
            <div class="bar-container">
              <div 
                class="energy-bar"
                :style="{ 
                  height: `${meal.percentage}%`,
                  backgroundColor: meal.color
                }"
              ></div>
              <div class="calories-label">{{ meal.calories }}</div>
            </div>
            <div class="meal-info">
              <div class="meal-icon">{{ meal.icon }}</div>
              <div class="meal-name">{{ meal.displayName }}</div>
            </div>
          </div>
        </div>
        
        <div class="chart-legend">
          <div class="legend-item" v-for="meal in mealData" :key="meal.type">
            <span class="legend-dot" :style="{ backgroundColor: meal.color }"></span>
            <span class="legend-text">
              {{ meal.displayName }}: {{ meal.calories }} kcal 
              ({{ Math.round((meal.calories / totalCalories) * 100) }}%)
            </span>
          </div>
        </div>
      </div>
      
      <div v-else class="no-data">
        Geen data beschikbaar
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  
  export default {
    name: 'MealNutritionChart',
    props: {
      entries: {
        type: Array,
        required: true
      }
    },
    setup(props) {
      const mealConfig = {
        ontbijt: { displayName: 'Ontbijt', icon: '🍳', color: '#f59e0b' },
        lunch: { displayName: 'Lunch', icon: '🥪', color: '#10b981' },
        diner: { displayName: 'Diner', icon: '🍽️', color: '#3b82f6' },
        tussendoortje: { displayName: 'Tussendoortje', icon: '🍎', color: '#8b5cf6' }
      };
  
      const hasData = computed(() => {
        return props.entries && props.entries.length > 0;
      });
  
      const mealTotals = computed(() => {
        if (!hasData.value) return {};
  
        const totals = {};
        
        props.entries.forEach(entry => {
          const mealType = entry.meal_type || 'tussendoortje';
          const nutrition = entry.calculateNutrition();
          
          if (!totals[mealType]) {
            totals[mealType] = { energy_kcal: 0, count: 0 };
          }
          
          totals[mealType].energy_kcal += nutrition.energy_kcal;
          totals[mealType].count += 1;
        });
  
        return totals;
      });
  
      const totalCalories = computed(() => {
        return Object.values(mealTotals.value).reduce((sum, meal) => sum + meal.energy_kcal, 0);
      });
  
      const mealData = computed(() => {
        if (!hasData.value) return [];
  
        const maxCalories = Math.max(...Object.values(mealTotals.value).map(m => m.energy_kcal));
  
        return Object.entries(mealTotals.value).map(([type, data]) => ({
          type,
          calories: Math.round(data.energy_kcal),
          percentage: maxCalories > 0 ? (data.energy_kcal / maxCalories) * 100 : 0,
          count: data.count,
          ...mealConfig[type]
        })).sort((a, b) => b.calories - a.calories);
      });
  
      return {
        hasData,
        mealData,
        totalCalories
      };
    }
  }
  </script>
  
  <style scoped>
  .meal-nutrition-chart {
    width: 100%;
  }
  
  .chart-container {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .meal-bars {
    display: flex;
    justify-content: space-around;
    align-items: end;
    height: 200px;
    padding: 20px 0;
    border-bottom: 2px solid #e5e7eb;
  }
  
  .meal-bar {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    min-width: 80px;
  }
  
  .bar-container {
    height: 150px;
    width: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: end;
    position: relative;
  }
  
  .energy-bar {
    width: 100%;
    border-radius: 6px 6px 0 0;
    transition: all 0.3s ease;
    min-height: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .energy-bar:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .calories-label {
    position: absolute;
    top: -25px;
    font-size: 12px;
    font-weight: 600;
    color: #374151;
    background: white;
    padding: 2px 4px;
    border-radius: 4px;
    border: 1px solid #e5e7eb;
  }
  
  .meal-info {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  
  .meal-icon {
    font-size: 1.5rem;
  }
  
  .meal-name {
    font-size: 13px;
    font-weight: 500;
    color: #374151;
  }
  
  .chart-legend {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    padding: 16px;
    background: #f9fafb;
    border-radius: 8px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
  }
  
  .legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  
  .legend-text {
    color: #374151;
    font-weight: 500;
  }
  
  .no-data {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #6b7280;
    font-style: italic;
  }
  
  @media (max-width: 768px) {
    .chart-legend {
      grid-template-columns: 1fr;
    }
    
    .meal-bars {
      height: 150px;
    }
    
    .bar-container {
      height: 100px;
    }
  }</style>