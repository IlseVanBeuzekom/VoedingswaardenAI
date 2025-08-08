<template>
    <div class="energy-chart">
      <div v-if="hasData" class="bar-chart">
        <div class="chart-bars">
          <div
            v-for="(item, index) in chartData"
            :key="index"
            class="bar-item"
          >
            <div class="bar-container">
              <div 
                class="bar"
                :style="{ height: `${item.percentage}%` }"
              ></div>
            </div>
            <div class="bar-label">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-value">{{ item.calories }} kcal</div>
            </div>
          </div>
        </div>
        
        <div class="chart-stats">
          <div class="stat-item">
            <span class="stat-label">Totaal:</span>
            <span class="stat-value">{{ totalCalories }} kcal</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Gemiddeld per item:</span>
            <span class="stat-value">{{ avgCalories }} kcal</span>
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
    name: 'EnergyChart',
    props: {
      entries: {
        type: Array,
        required: true
      }
    },
    setup(props) {
      const hasData = computed(() => {
        return props.entries && props.entries.length > 0;
      });
  
      const chartData = computed(() => {
        if (!hasData.value) return [];
  
        const data = props.entries.map(entry => {
          const nutrition = entry.calculateNutrition();
          return {
            name: entry.getName(),
            calories: Math.round(nutrition.energy_kcal),
            type: entry.getType()
          };
        });
  
        // Sort by calories descending
        data.sort((a, b) => b.calories - a.calories);
  
        const maxCalories = Math.max(...data.map(item => item.calories));
  
        return data.map(item => ({
          ...item,
          percentage: maxCalories > 0 ? (item.calories / maxCalories) * 100 : 0
        }));
      });
  
      const totalCalories = computed(() => {
        if (!hasData.value) return 0;
        return chartData.value.reduce((sum, item) => sum + item.calories, 0);
      });
  
      const avgCalories = computed(() => {
        if (!hasData.value) return 0;
        return Math.round(totalCalories.value / chartData.value.length);
      });
  
      return {
        hasData,
        chartData,
        totalCalories,
        avgCalories
      };
    }
  }
  </script>
  
  <style scoped>
  .energy-chart {
    width: 100%;
  }
  
  .bar-chart {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .chart-bars {
    display: flex;
    align-items: end;
    gap: 12px;
    height: 200px;
    padding: 10px 0;
    overflow-x: auto;
  }
  
  .bar-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    min-width: 80px;
    flex-shrink: 0;
  }
  
  .bar-container {
    height: 150px;
    width: 40px;
    display: flex;
    align-items: end;
    position: relative;
  }
  
  .bar {
    width: 100%;
    background: linear-gradient(to top, #3b82f6, #60a5fa);
    border-radius: 4px 4px 0 0;
    transition: all 0.3s ease;
    min-height: 4px;
    position: relative;
  }
  
  .bar:hover {
    background: linear-gradient(to top, #2563eb, #3b82f6);
    transform: scale(1.05);
  }
  
  .bar-label {
    text-align: center;
    font-size: 12px;
    max-width: 80px;
  }
  
  .item-name {
    color: #374151;
    font-weight: 500;
    margin-bottom: 2px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
  }
  
  .item-value {
    color: #6b7280;
    font-weight: 600;
  }
  
  .chart-stats {
    display: flex;
    justify-content: space-around;
    padding: 16px;
    background: #f9fafb;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
  }
  
  .stat-item {
    text-align: center;
  }
  
  .stat-label {
    display: block;
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 4px;
  }
  
  .stat-value {
    display: block;
    font-size: 18px;
    font-weight: 700;
    color: #1f2937;
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
    .chart-bars {
      height: 150px;
    }
    
    .bar-container {
      height: 100px;
    }
    
    .chart-stats {
      flex-direction: column;
      gap: 12px;
    }
  }
  </style>