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
            :customServings="getCustomServings(dayDate)"
            :addToShoppingList="getAddToShoppingList(dayDate)"
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
        console.log('range: ', range)
        selectedStartDate.value = range.startDate;
        selectedEndDate.value = range.endDate;
        dayCount.value = range.dayCount;
        
        // Try to load existing week menu
        try {
          const existingMenu = await weekMenuStore.fetchWeekMenuByDateRange(
            range.startDate, 
            range.endDate
          );

          // Check on id, because an empty one will be given back when there is no page for the week menu
          if (existingMenu.id) {
            currentWeekMenu.value = existingMenu;
          } else {
            createNewWeekMenu(range);
          }
        } catch (error) {
          createNewWeekMenu(range);
        }
      };
      
      const createNewWeekMenu = (range) => {
        currentWeekMenu.value = new WeekMenu({
          start_date: range.startDate,
          end_date: range.endDate,
          days: dayDates.value.map(date => new MenuDay({ 
            date,
            add_to_shopping_list: true 
          }))
        });
      };
  
      const getSelectedRecipeId = (dateStr) => {
        const day = currentWeekMenu.value.getDayByDate(dateStr);
        return day?.recipe_id || null;
      };

      const getCustomServings = (dateStr) => {
        const day = currentWeekMenu.value.getDayByDate(dateStr);
        return day?.servings || null;
      }

      const getAddToShoppingList = (dateStr) => {
        const day = currentWeekMenu.value.getDayByDate(dateStr);
        return day?.add_to_shopping_list !== undefined ? day.add_to_shopping_list : true;
      }
  
      const onRecipeChange = (changeData) => {
        const day = currentWeekMenu.value.getDayByDate(changeData.date);
        if (day) {
          day.recipe_id = changeData.recipeId;
          day.servings = changeData.servings;
          day.add_to_shopping_list = changeData.addToShoppingList;
        } else {
          currentWeekMenu.value.addDay({
            date: changeData.date,
            recipe_id: changeData.recipeId,
            servings: changeData.servings,
            add_to_shopping_list: changeData.addToShoppingList
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
        createNewWeekMenu,
        getSelectedRecipeId,
        getCustomServings,
        getAddToShoppingList,
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