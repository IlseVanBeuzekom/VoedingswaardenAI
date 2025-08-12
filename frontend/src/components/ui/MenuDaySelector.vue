<template>
  <div class="menu-day-selector">
    <div class="day-info">
      <h4>{{ formatDayName(date) }}</h4>
      <span class="date-display">{{ formatDate(date) }}</span>
    </div>
    
    <div class="recipe-controls">
      <select 
        aria-label="Recept"
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
      <BaseButton 
        v-if="!selectedRecipe"
        @click="chooseRecipe"
        variant="secondary"
        size="small"
      >
        Kies recept
      </BaseButton>

      <div v-if="selectedRecipe" class="selected-recipe-display">
        <!-- <span class="recipe-name">{{ selectedRecipe.name }}</span> -->
        <BaseButton 
          @click="chooseRecipe"
          variant="secondary"
          size="small"
        >
          Wijzig recept
        </BaseButton>
      </div>

      <div v-if="selectedRecipe" class="recipe-options">
        <div class="servings-control">
          <label for="servings">Personen:</label>
          <input
            id="servings"
            v-model.number="customServings"
            type="number"
            min="1"
            max="20"
            class="servings-input"
            @change="onOptionsChange"
          />
        </div>
        
        <div class="shopping-list-control">
          <label class="checkbox-label">
            <input
              v-model="addToShoppingList"
              type="checkbox"
              @change="onOptionsChange"
            />
            Boodschappenlijst
          </label>
        </div>
      </div>
    </div>
    
    <div v-if="selectedRecipe" class="selected-recipe-info">
      <span class="recipe-name">{{ selectedRecipe.name }}</span>
      <div class="recipe-meta">
        <span>⏱️ {{ selectedRecipe.preparation_time }} min</span>
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
      customServings: {
        type: Number,
        default: null
      },
      addToShoppingList: {
        type: Boolean,
        default: true
      },
      availableRecipes: {
        type: Array,
        default: () => []
      }
    },
    setup(props, { emit }) {
      const selectedRecipeId = ref(props.selectedRecipeId || '');
      const customServings = ref(props.customServings);
      const addToShoppingList = ref(props.addToShoppingList);

      const chooseRecipe = () => {
        emit('chooseRecipe', {
          date: props.date,
          returnRoute: '/week-menu'
        });
      };

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
        if(selectedRecipeId.value){
          customServings.value = selectedRecipe.value?.servings || null;
        } else {
          customServings.value = null
        }

        emitChange()
      };

      const onOptionsChange = () => {
        emitChange()
      }

      const emitChange = () => {
        emit('recipeChange', {
          date: props.date,
          recipeId: selectedRecipeId.value || null,
          servings: customServings.value,
          addToShoppingList: addToShoppingList.value
        })
      };
  
      // Watch for prop changes
      watch(() => props.selectedRecipeId, (newVal) => {
        selectedRecipeId.value = newVal || '';
      });

      watch(() => props.customServings, (newVal) => {
        customServings.value = newVal;
      });

      watch(() => props.addToShoppingList, (newVal) => {
        addToShoppingList.value = newVal;
      })
  
      return {
        selectedRecipeId,
        customServings,
        addToShoppingList,
        selectedRecipe,
        formatDayName,
        formatDate,
        onRecipeChange,
        onOptionsChange, 
        chooseRecipe
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
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 140px 1fr auto;
    gap: 24px;
    align-items: start;
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

  .recipe-controls {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .recipe-select {
    flex: 1;
    min-width: 250px;
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
    text-align: right;
    min-width: 120px;
  }
  
  .recipe-name {
    display: block;
    font-weight: 500;
    color: #1f2937;
    margin-bottom: 4px;
    font-size: 14px;
  }
  
  .recipe-meta {
    font-size: 12px;
    color: #6b7280;
  }

  .recipe-selector {
    flex: 1;
  }

  .day-info {
    text-align: left;
  }

  .day-info h4 {
    margin: 0 0 4px 0;
    color: #1f2937;
    font-size: 1.1rem;
    text-transform: capitalize;
    font-weight: 600;
  }

  .recipe-options {
    display: flex;
    align-items: center;
    gap: 16px;
    white-space: nowrap;
  }

  .servings-control {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .servings-control label {
    font-size: 14px;
    font-weight: 500;
    color: #374151;
  }

  .servings-input {
    width: 50px;
    padding: 4px 6px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }

  .servings-note {
    font-size: 12px;
    color: #6b7280;
  }

  .shopping-list-control {
    display: flex;
    align-items: center;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    font-size: 14px;
    color: #374151;
  }

  .checkbox-label input[type="checkbox"] {
    margin: 0;
  }

  .checkmark {
    position: relative;
  }

  @media (max-width: 768px) {
  .menu-day-selector {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .recipe-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .recipe-options {
    justify-content: space-between;
  }
  
  .selected-recipe-info {
    text-align: left;
  }
}
  </style>