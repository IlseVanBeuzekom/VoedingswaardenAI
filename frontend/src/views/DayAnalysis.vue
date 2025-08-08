<template>
    <div class="day-analysis">
      <div class="page-header">
        <h1>Voedingsanalyse</h1>
        <p>Gedetailleerde analyse van je voeding voor een specifieke dag</p>
      </div>
  
      <!-- Date Selector -->
      <div class="date-selector">
        <div class="date-input-group">
          <label for="selected-date">Selecteer datum:</label>
          <input
            id="selected-date"
            v-model="selectedDate"
            type="date"
            class="date-input"
            @change="loadDailyLog"
          />
          <BaseButton 
            @click="setToday"
            variant="secondary"
            size="small"
          >
            Vandaag
          </BaseButton>
          <BaseButton 
            @click="goToDayOverview"
            variant="primary"
            size="small"
          >
            Bewerken
          </BaseButton>
        </div>
        
        <div v-if="selectedDate" class="selected-date-display">
          {{ formatDisplayDate(selectedDate) }}
        </div>
      </div>
  
      <div v-if="loading" class="loading">
        Gegevens laden...
      </div>
  
      <div v-else-if="!dailyLog || dailyLog.entries.length === 0" class="empty-state">
        <p>Geen data beschikbaar voor deze dag.</p>
      </div>
  
      <div v-else class="analysis-content">
        <!-- Nutrition Tiles -->
        <div class="nutrition-tiles">
          <NutritionTile 
            title="Energie" 
            :value="Math.round(totalNutrition.energy_kcal)" 
            unit="kcal"
            color="blue"
          />
          <NutritionTile 
            title="Eiwitten" 
            :value="formatValue(totalNutrition.proteins)" 
            unit="g"
            color="red"
          />
          <NutritionTile 
            title="Koolhydraten" 
            :value="formatValue(totalNutrition.carbohydrates)" 
            unit="g"
            color="yellow"
          />
          <NutritionTile 
            title="Vetten" 
            :value="formatValue(totalNutrition.fats)" 
            unit="g"
            color="green"
          />
        </div>
  
        <!-- Charts Section -->
        <div class="charts-section">
          <div class="chart-container">
            <h3>Macronutriënten verdeling</h3>
            <MacronutrientChart :nutrition="totalNutrition" />
          </div>
          
          <div class="chart-container">
            <h3>Energie per maaltijd</h3>
            <EnergyChart :entries="dailyLog.entries" />
          </div>
        </div>
  
        <!-- Detailed Table -->
        <div class="table-section">
          <h3>Gedetailleerd overzicht</h3>
          <div class="table-container">
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
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in dailyLog.entries" :key="entry.id" class="entry-row">
                  <td class="name-cell">
                    <div class="item-info">
                      <span class="item-name">{{ entry.getName() }}</span>
                      <span class="item-type">{{ entry.getType() === 'product' ? 'Product' : 'Recept' }}</span>
                    </div>
                  </td>
                  <td class="amount-cell">{{ formatValue(entry.amount) }} {{ entry.unit }}</td>
                  <td class="nutrition-cell">{{ Math.round(entry.calculateNutrition().energy_kcal) }} kcal</td>
                  <td class="nutrition-cell">{{ formatValue(entry.calculateNutrition().proteins) }}g</td>
                  <td class="nutrition-cell">{{ formatValue(entry.calculateNutrition().fats) }}g</td>
                  <td class="nutrition-cell">{{ formatValue(entry.calculateNutrition().carbohydrates) }}g</td>
                  <td class="nutrition-cell">{{ formatValue(entry.calculateNutrition().sugars) }}g</td>
                  <td class="nutrition-cell">{{ formatValue(entry.calculateNutrition().fibers) }}g</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="totals-row">
                  <td class="totals-label"><strong>Totaal</strong></td>
                  <td>-</td>
                  <td class="totals-value"><strong>{{ Math.round(totalNutrition.energy_kcal) }} kcal</strong></td>
                  <td class="totals-value"><strong>{{ formatValue(totalNutrition.proteins) }}g</strong></td>
                  <td class="totals-value"><strong>{{ formatValue(totalNutrition.fats) }}g</strong></td>
                  <td class="totals-value"><strong>{{ formatValue(totalNutrition.carbohydrates) }}g</strong></td>
                  <td class="totals-value"><strong>{{ formatValue(totalNutrition.sugars) }}g</strong></td>
                  <td class="totals-value"><strong>{{ formatValue(totalNutrition.fibers) }}g</strong></td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import dailyFoodService from '../services/dailyFoodService.js';
  import BaseButton from '../components/ui/BaseButton.vue';
  import NutritionTile from '../components/ui/NutritionTile.vue';
  import MacronutrientChart from '../components/ui/MacronutrientChart.vue';
  import EnergyChart from '../components/ui/EnergyChart.vue';
  
  export default {
    name: 'DayAnalysis',
    components: {
      BaseButton,
      NutritionTile,
      MacronutrientChart,
      EnergyChart
    },
    setup() {
      const router = useRouter();
      const route = useRoute();
  
      const selectedDate = ref('');
      const dailyLog = ref(null);
      const loading = ref(false);
      const error = ref(null);
  
      const totalNutrition = computed(() => {
        if (!dailyLog.value) return { energy_kcal: 0, proteins: 0, fats: 0, carbohydrates: 0, sugars: 0, fibers: 0 };
        return dailyLog.value.calculateTotalNutrition();
      });
  
      const setToday = () => {
        const today = new Date();
        selectedDate.value = today.toISOString().split('T')[0];
        loadDailyLog();
      };
  
      const formatDisplayDate = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleDateString('nl-NL', { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        });
      };
  
      const formatValue = (value) => {
        return Math.round(value * 10) / 10;
      };
  
      const loadDailyLog = async () => {
        if (!selectedDate.value) return;
  
        loading.value = true;
        error.value = null;
  
        try {
          dailyLog.value = await dailyFoodService.getDailyLog(selectedDate.value);
        } catch (err) {
          error.value = 'Fout bij het laden van daggegevens';
          console.error('Error loading daily log:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const goToDayOverview = () => {
        router.push({ name: 'DayOverview', query: { date: selectedDate.value } });
      };
  
      onMounted(() => {
        // Check if date is passed via query params
        if (route.query.date) {
          selectedDate.value = route.query.date;
          loadDailyLog();
        } else {
          setToday();
        }
      });
  
      return {
        selectedDate,
        dailyLog,
        loading,
        error,
        totalNutrition,
        setToday,
        formatDisplayDate,
        formatValue,
        loadDailyLog,
        goToDayOverview
      };
    }
  }
  </script>
  
  <style scoped>
  .day-analysis {
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .page-header {
    text-align: center;
    margin-bottom: 32px;
  }
  
  .page-header h1 {
    color: #1f2937;
    margin-bottom: 8px;
  }
  
  .page-header p {
    color: #6b7280;
  }
  
  .date-selector {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
  }
  
  .date-input-group {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-bottom: 12px;
  }
  
  .date-input-group label {
    font-weight: 500;
    color: #374151;
  }
  
  .date-input {
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
  }
  
  .selected-date-display {
    font-size: 18px;
    font-weight: 500;
    color: #1f2937;
  }
  
  .loading, .empty-state {
    text-align: center;
    padding: 40px;
    color: #6b7280;
  }
  
  .analysis-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }
  
  .nutrition-tiles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .charts-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  
  .chart-container {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
  }
  
  .chart-container h3 {
    margin: 0 0 20px 0;
    color: #1f2937;
    text-align: center;
  }
  
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
  
  .table-container {
    overflow-x: auto;
  }
  
  .entries-table {
    width: 100%;
    border-collapse: collapse;
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
  
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    text-align: center;
  }
  
  @media (max-width: 1024px) {
    .charts-section {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 768px) {
    .nutrition-tiles {
      grid-template-columns: 1fr;
    }
    
    .date-input-group {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .entries-table th:nth-child(n+4) {
      display: none;
    }
  }
  </style>