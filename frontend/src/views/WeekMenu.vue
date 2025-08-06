<template>
    <div class="week-menu">
      <h1>Weekmenu Planner</h1>
      
      <DateRangeSelector
        title="Selecteer periode voor weekmenu"
        @dateChange="onDateRangeChange"
        :initialStartDate="selectedStartDate"
        :initialEndDate="selectedEndDate"
      />
  
      <div v-if="showDaySelectors" class="menu-days">
        <h2>Recepten per dag</h2>
        
        <div v-if="weekMenuStore.loading" class="loading">
          Menu laden...
        </div>
        
        <div v-else class="days-grid">
          <MenuDaySelector
            v-for="dayDate in dayDates"
            :key="dayDate"
            :date="dayDate"
            :selectedRecipeId="getSelectedRecipeId(dayDate)"
            :availableRecipes="availableRecipes"
            @recipeChange="onRecipeChange"
          />
        </div>
        
        <div class="form-actions">
          <BaseButton 
            @click="saveWeekMenu"
            :disabled="weekMenuStore.loading"
            variant="primary"
          >
            {{ weekMenuStore.loading ? 'Bezig met opslaan...' : 'Weekmenu Opslaan' }}
          </BaseButton>
        </div>
      </div>
  
      <div v-if="weekMenuStore.error" class="error-message">
        {{ weekMenuStore.error }}
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useWeekMenuStore } from '../stores/weekMenuStore.js';
  import { useRecipeStore } from '../stores/recipeStore.js';
  import { WeekMenu, MenuDay } from '../models/WeekMenu.js';
  import DateRangeSelector from '../components/ui/DateRangeSelector.vue';
  import MenuDaySelector from '../components/ui/MenuDaySelector.vue';
  import BaseButton from '../components/ui/BaseButton.vue';
  
  export default {
    name: 'WeekMenu',
    components: {
      DateRangeSelector,
      MenuDaySelector,
      BaseButton
    },
    setup() {
      const router = useRouter();
      const weekMenuStore = useWeekMenuStore();
      const recipeStore = useRecipeStore();
      
      const selectedStartDate = ref('');
      const selectedEndDate = ref('');
      const dayCount = ref(0);
      const currentWeekMenu = ref(new WeekMenu());
  
      const showDaySelectors = computed(() => {
        return selectedStartDate.value && selectedEndDate.value && dayCount.value > 0;
      });
  
      const availableRecipes = computed(() => recipeStore.recipes);
  
      const dayDates = computed(() => {
        if (!selectedStartDate.value || !selectedEndDate.value) return [];
        
        const dates = [];
        const start = new Date(selectedStartDate.value);
        const end = new Date(selectedEndDate.value);
        
        for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
          dates.push(d.toISOString().split('T')[0]);
        }
        
        return dates;
      });
  
      const onDateRangeChange = async (range) => {
        selectedStartDate.value = range.startDate;
        selectedEndDate.value = range.endDate;
        dayCount.value = range.dayCount;
        
        // Try to load existing week menu
        try {
          const existingMenu = await weekMenuStore.fetchWeekMenuByDateRange(
            range.startDate, 
            range.endDate
          );
          
          if (existingMenu) {
            currentWeekMenu.value = existingMenu;
          } else {
            // Create new week menu structure
            currentWeekMenu.value = new WeekMenu({
              start_date: range.startDate,
              end_date: range.endDate,
              days: dayDates.value.map(date => new MenuDay({ date }))
            });
          }
        } catch (error) {
          // Create new if not found
          currentWeekMenu.value = new WeekMenu({
            start_date: range.startDate,
            end_date: range.endDate,
            days: dayDates.value.map(date => new MenuDay({ date }))
          });
        }
      };
  
      const getSelectedRecipeId = (dateStr) => {
        const day = currentWeekMenu.value.getDayByDate(dateStr);
        return day?.recipe_id || null;
      };
  
      const onRecipeChange = (changeData) => {
        const day = currentWeekMenu.value.getDayByDate(changeData.date);
        if (day) {
          day.recipe_id = changeData.recipeId;
        } else {
          currentWeekMenu.value.addDay({
            date: changeData.date,
            recipe_id: changeData.recipeId
          });
        }
      };
  
      const saveWeekMenu = async () => {
        try {
          if (currentWeekMenu.value.id) {
            await weekMenuStore.updateWeekMenu(currentWeekMenu.value.id, currentWeekMenu.value.toAPI());
          } else {
            const newMenu = await weekMenuStore.createWeekMenu(currentWeekMenu.value.toAPI());
            currentWeekMenu.value = newMenu;
          }
          
          // Show success message or redirect
          alert('Weekmenu succesvol opgeslagen!');
        } catch (error) {
          console.error('Error saving week menu:', error);
        }
      };
  
      // Load recipes on mount
      onMounted(async () => {
        try {
          await recipeStore.fetchRecipes();
        } catch (error) {
          console.error('Error loading recipes:', error);
        }
      });
  
      return {
        weekMenuStore,
        selectedStartDate,
        selectedEndDate,
        showDaySelectors,
        availableRecipes,
        dayDates,
        onDateRangeChange,
        getSelectedRecipeId,
        onRecipeChange,
        saveWeekMenu
      };
    }
  }
  </script>
  
  <style scoped>
  .week-menu {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .week-menu h1 {
    text-align: center;
    margin-bottom: 32px;
    color: #1f2937;
  }
  
  .menu-days h2 {
    margin-bottom: 24px;
    color: #1f2937;
  }
  
  .loading {
    text-align: center;
    padding: 48px 24px;
    color: #6b7280;
  }
  
  .days-grid {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 32px;
  }
  
  .form-actions {
    display: flex;
    justify-content: center;
    margin-top: 24px;
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
    .days-grid {
      grid-template-columns: 1fr;
    }
  }

  h2 {
    text-align: center;
  }
  </style>