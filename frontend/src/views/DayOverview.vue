<template>
    <div class="day-overview">
      <div class="page-header">
        <h1>Dag Overzicht</h1>
        <p>Bekijk en beheer wat je op een specifieke dag hebt gegeten</p>
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
            @click="goToAnalysis"
            variant="primary"
            size="small"
            :disabled="!selectedDate"
          >
            Analyse bekijken
          </BaseButton>
        </div>
        
        <div v-if="selectedDate" class="selected-date-display">
          {{ formatDisplayDate(selectedDate) }}
        </div>
      </div>
  
      <!-- Add Entry Form -->
      <DailyFoodEntryForm
        v-if="!editingEntry"
        :products="availableProducts"
        :recipes="availableRecipes"
        @submit="handleAddEntry"
      />
  
      <!-- Edit Entry Form -->
      <DailyFoodEntryForm
        v-if="editingEntry"
        :products="availableProducts"
        :recipes="availableRecipes"
        :initial-data="editingEntry"
        mode="edit"
        @submit="handleUpdateEntry"
        @cancel="cancelEdit"
      />
  
      <!-- Daily Log Table -->
      <div v-if="dailyLog" class="daily-log-section">
        <h2>Gegeten op {{ formatDisplayDate(selectedDate) }}</h2>
        
        <div v-if="loading" class="loading">
          Gegevens laden...
        </div>
  
        <div v-else-if="dailyLog.entries.length === 0" class="empty-state">
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
                <th>Acties</th>
              </tr>
            </thead>
            <tbody>
              <DailyFoodEntryItem
                v-for="entry in dailyLog.entries"
                :key="entry.id"
                :entry="entry"
                @edit="startEdit"
                @delete="handleDeleteEntry"
              />
            </tbody>
            <tfoot v-if="dailyLog.entries.length > 0">
              <tr class="totals-row">
                <td class="totals-label"><strong>Totaal</strong></td>
                <td>-</td>
                <td class="totals-value"><strong>{{ Math.round(totalNutrition.energy_kcal) }} kcal</strong></td>
                <td class="totals-value"><strong>{{ formatValue(totalNutrition.proteins) }}g</strong></td>
                <td class="totals-value"><strong>{{ formatValue(totalNutrition.fats) }}g</strong></td>
                <td class="totals-value"><strong>{{ formatValue(totalNutrition.carbohydrates) }}g</strong></td>
                <td class="totals-value"><strong>{{ formatValue(totalNutrition.sugars) }}g</strong></td>
                <td class="totals-value"><strong>{{ formatValue(totalNutrition.fibers) }}g</strong></td>
                <td>-</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted, watch } from 'vue';
  import { useProductStore } from '../stores/productStore.js';
  import { useRecipeStore } from '../stores/recipeStore.js';
  import dailyFoodService from '../services/dailyFoodService.js';
  import DailyFoodEntryForm from '../components/forms/DailyFoodEntryForm.vue';
  import DailyFoodEntryItem from '../components/ui/DailyFoodEntryItem.vue';
  import BaseButton from '../components/ui/BaseButton.vue';
  import { useRoute, useRouter } from 'vue-router';

  
  export default {
    name: 'DayOverview',
    components: {
      DailyFoodEntryForm,
      DailyFoodEntryItem,
      BaseButton
    },
    setup() {
      const productStore = useProductStore();
      const recipeStore = useRecipeStore();
  
      const selectedDate = ref('');
      const dailyLog = ref(null);
      const editingEntry = ref(null);
      const loading = ref(false);
      const error = ref(null);
  
      const availableProducts = computed(() => productStore.products);
      const availableRecipes = computed(() => recipeStore.recipes);

      const router = useRouter();
      const route = useRoute();
  
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
  
      const handleAddEntry = async (entryData) => {
        try {
          const newEntry = await dailyFoodService.addEntry(selectedDate.value, entryData);
          
          // Refresh the daily log
          await loadDailyLog();
          
          error.value = null;
        } catch (err) {
          error.value = 'Fout bij het toevoegen van item';
          console.error('Error adding entry:', err);
        }
      };
  
      const handleUpdateEntry = async (entryData) => {
        if (!editingEntry.value) return;
  
        try {
          await dailyFoodService.updateEntry(editingEntry.value.id, entryData);
          
          // Refresh the daily log
          await loadDailyLog();
          
          editingEntry.value = null;
          error.value = null;
        } catch (err) {
          error.value = 'Fout bij het bijwerken van item';
          console.error('Error updating entry:', err);
        }
      };
  
      const handleDeleteEntry = async (entry) => {
        if (!confirm(`Weet je zeker dat je "${entry.getName()}" wilt verwijderen?`)) {
          return;
        }
  
        try {
          await dailyFoodService.deleteEntry(entry.id);
          
          // Refresh the daily log
          await loadDailyLog();
          
          error.value = null;
        } catch (err) {
          error.value = 'Fout bij het verwijderen van item';
          console.error('Error deleting entry:', err);
        }
      };
  
      const startEdit = (entry) => {
        editingEntry.value = entry;
      };
  
      const cancelEdit = () => {
        editingEntry.value = null;
      };

      const goToAnalysis = () => {
        router.push({ name: 'DayAnalysis', query: { date: selectedDate.value } });
      };
  
      // Initialize with today's date
      onMounted(async () => {
        setToday();
        
        // Check if date is passed via query params
        if (route.query.date) {
            selectedDate.value = route.query.date;
          } else {
            setToday();
          }

        // Load products and recipes
        try {
          await Promise.all([
            productStore.fetchProducts(),
            recipeStore.fetchRecipes()
          ]);
        } catch (err) {
          console.error('Error loading data:', err);
        }
      });
  
      return {
        selectedDate,
        dailyLog,
        editingEntry,
        loading,
        error,
        availableProducts,
        availableRecipes,
        totalNutrition,
        setToday,
        formatDisplayDate,
        formatValue,
        loadDailyLog,
        handleAddEntry,
        handleUpdateEntry,
        handleDeleteEntry,
        startEdit,
        cancelEdit,
        goToAnalysis
      };
    }
  }
  </script>
  
  <style scoped>
  .day-overview {
    max-width: 1200px;
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
  
  .date-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .selected-date-display {
    font-size: 18px;
    font-weight: 500;
    color: #1f2937;
  }
  
  .daily-log-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
  }
  
  .daily-log-section h2 {
    margin: 0 0 20px 0;
    color: #1f2937;
  }
  
  .loading {
    text-align: center;
    padding: 40px;
    color: #6b7280;
  }
  
  .empty-state {
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
  
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    margin-top: 16px;
    text-align: center;
  }
  
  @media (max-width: 768px) {
    .date-input-group {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .entries-table th:nth-child(n+4) {
      display: none;
    }
    
    .entries-table {
      font-size: 14px;
    }
  }
  </style>