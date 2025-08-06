<template>
  <div class="menu-day-selector">
    <div class="day-info">
      <h4>{{ formatDayName(date) }}</h4>
      <span class="date-display">{{ formatDate(date) }}</span>
    </div>
    
    <div class="recipe-selector">
      <select 
        v-model="selectedRecipeId" 
        class="recipe-select"
        @change="onRecipeChange"
      >
        <option value="">Geen recept</option>
        <option 
          v-for="recipe in availableRecipes" 
          :key="recipe.id" 
          :value="recipe.id"
        >
          {{ recipe.name }} ({{ recipe.servings }} pers, {{ recipe.preparation_time }} min)
        </option>
      </select>
      
      <div v-if="selectedRecipe" class="selected-recipe-info">
        <span class="recipe-name">{{ selectedRecipe.name }}</span>
        <div class="recipe-meta">
          <span>👥 {{ selectedRecipe.servings }} personen</span>
          <span>⏱️ {{ selectedRecipe.preparation_time }} min</span>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import { computed, ref, watch } from 'vue';
  
  export default {
    name: 'MenuDaySelector',
    emits: ['recipeChange'],
    props: {
      date: {
        type: String,
        required: true
      },
      selectedRecipeId: {
        type: [Number, String],
        default: null
      },
      availableRecipes: {
        type: Array,
        default: () => []
      }
    },
    setup(props, { emit }) {
      const selectedRecipeId = ref(props.selectedRecipeId || '');
  
      const selectedRecipe = computed(() => {
        if (!selectedRecipeId.value) return null;
        return props.availableRecipes.find(r => r.id == selectedRecipeId.value);
      });
  
      const formatDayName = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('nl-NL', { weekday: 'long' });
      };
  
      const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('nl-NL', { 
          day: 'numeric', 
          month: 'short' 
        });
      };
  
      const onRecipeChange = () => {
        emit('recipeChange', {
          date: props.date,
          recipeId: selectedRecipeId.value || null
        });
      };
  
      // Watch for prop changes
      watch(() => props.selectedRecipeId, (newVal) => {
        selectedRecipeId.value = newVal || '';
      });
  
      return {
        selectedRecipeId,
        selectedRecipe,
        formatDayName,
        formatDate,
        onRecipeChange
      };
    }
  }
  </script>
  
  <style scoped>
  .menu-day-selector {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    transition: box-shadow 0.2s ease;
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 24px;
  }
  
  .menu-day-selector:hover {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .day-header {
    min-width: 140px;
    text-align: left;
  }
  
  .day-header h4 {
    margin: 0 0 4px 0;
    color: #1f2937;
    font-size: 1.1rem;
    text-transform: capitalize;
    font-weight: 600
  }
  
  .date-display {
    color: #6b7280;
    font-size: 14px;
  }
  
  .recipe-select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    background: white;
  }
  
  .recipe-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .selected-recipe-info {
    margin-top: 8px;
    padding: 8px 12px;
    background-color: #f0f9ff;
    border-radius: 6px;
  }
  
  .recipe-name {
    display: block;
    font-weight: 500;
    color: #1f2937;
    margin-bottom: 4px;
  }
  
  .recipe-meta {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: #6b7280;
  }

  .recipe-selector {
    flex: 1;
  }

  .day-info {
    min-width: 140px;
    text-align: left;
  }

  .day-info h4 {
    margin: 0 0 4px 0;
    color: #1f2937;
    font-size: 1.1rem;
    text-transform: capitalize;
    font-weight: 600;
  }
  </style>