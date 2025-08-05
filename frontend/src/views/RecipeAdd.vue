<template>
    <div class="recipe-add">
      <h1>Nieuw Recept</h1>
      
      <form @submit.prevent="handleSubmit" class="recipe-form">
        <!-- Basic Recipe Info -->
        <div class="recipe-header">
          <div class="form-group">
            <label for="name">Receptnaam*</label>
            <input
              v-model="recipe.name"
              type="text"
              id="name"
              required
              class="form-input"
              placeholder="Bijv. Spaghetti Bolognese"
            />
          </div>
  
          <div class="header-row">
            <div class="form-group">
              <label for="servings">Aantal personen*</label>
              <input
                v-model.number="recipe.servings"
                type="number"
                id="servings"
                min="1"
                required
                class="form-input"
              />
            </div>
  
            <div class="form-group">
              <label for="prep_time">Bereidingstijd (minuten)*</label>
              <input
                v-model.number="recipe.preparation_time"
                type="number"
                id="prep_time"
                min="1"
                required
                class="form-input"
              />
            </div>
          </div>
        </div>
  
        <!-- Two Column Layout -->
        <div class="recipe-content">
          <!-- Left Column - Ingredients -->
          <div class="ingredients-section">
            <h3>Ingrediënten</h3>
            
            <div class="ingredients-list">
              <div 
                v-for="(ingredient, index) in recipe.ingredients" 
                :key="index"
                class="ingredient-row"
              >
                <div class="ingredient-inputs">
                  <input
                    v-model.number="ingredient.amount"
                    type="number"
                    step="0.1"
                    min="0"
                    placeholder="Aantal"
                    class="amount-input"
                  />
                  
                  <select v-model="ingredient.unit" aria-label='unit' class="unit-select">
                    <option value="gram">gram</option>
                    <option value="kg">kg</option>
                    <option value="ml">ml</option>
                    <option value="liter">liter</option>
                    <option value="stuk">stuk</option>
                    <option value="el">eetlepel</option>
                    <option value="tl">theelepel</option>
                    <option value="kopje">kopje</option>
                  </select>
  
                  <select 
                    v-model="ingredient.product_id" 
                    aria-label = "product"
                    class="product-select"
                    required
                  >
                    <option value="">Kies product</option>
                    <option 
                      v-for="product in availableProducts" 
                      :key="product.id" 
                      :value="product.id"
                    >
                      {{ product.name }}
                    </option>
                  </select>
                </div>
                
                <button 
                  @click="removeIngredient(index)"
                  type="button" 
                  class="remove-btn"
                  title="Verwijder ingrediënt"
                >
                  ❌
                </button>
              </div>
            </div>
  
            <BaseButton 
              @click="addIngredient"
              type="button"
              variant="secondary"
              size="small"
            >
              + Ingrediënt toevoegen
            </BaseButton>
          </div>
  
          <!-- Right Column - Instructions -->
          <div class="instructions-section">
            <h3>Bereidingswijze</h3>
            <textarea
              v-model="recipe.instructions"
              class="instructions-textarea"
              placeholder="Beschrijf hier stap voor stap hoe het recept wordt bereid..."
              required
            ></textarea>
          </div>
        </div>
  
        <!-- Submit Button -->
        <div class="form-actions">
          <BaseButton 
            type="submit"
            :disabled="!isFormValid || recipeStore.loading"
            variant="primary"
          >
            {{ recipeStore.loading ? 'Bezig met opslaan...' : 'Recept Opslaan' }}
          </BaseButton>
          
          <BaseButton 
            @click="$router.push('/')"
            variant="secondary"
            type="button"
          >
            Annuleren
          </BaseButton>
        </div>
  
        <div v-if="recipeStore.error" class="error-message">
          {{ recipeStore.error }}
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRecipeStore } from '../stores/recipeStore.js';
  import { useProductStore } from '../stores/productStore.js';
  import { Recipe } from '../models/Recipe.js';
  import BaseButton from '../components/ui/BaseButton.vue';
  
  export default {
    name: 'RecipeAdd',
    components: {
      BaseButton
    },
    setup() {
      const router = useRouter();
      const recipeStore = useRecipeStore();
      const productStore = useProductStore();
      
      const recipe = ref(new Recipe());
  
      const availableProducts = computed(() => productStore.products);
  
      const isFormValid = computed(() => {
        return recipe.value.name.trim().length > 0 &&
               recipe.value.servings > 0 &&
               recipe.value.preparation_time > 0 &&
               recipe.value.instructions.trim().length > 0 &&
               recipe.value.ingredients.length > 0 &&
               recipe.value.ingredients.every(ing => 
                 ing.product_id && ing.amount > 0 && ing.unit.trim().length > 0
               );
      });
  
      const addIngredient = () => {
        recipe.value.addIngredient();
      };
  
      const removeIngredient = (index) => {
        recipe.value.removeIngredient(index);
      };
  
      const handleSubmit = async () => {
        if (!isFormValid.value) return;
        
        try {
          await recipeStore.createRecipe(recipe.value.toAPI());
          router.push('/recipes');
        } catch (error) {
          console.error('Error creating recipe:', error);
        }
      };
  
      // Load products on mount
      onMounted(async () => {
        try {
          await productStore.fetchProducts();
          // Start with one empty ingredient
          addIngredient();
        } catch (error) {
          console.error('Error loading products:', error);
        }
      });
  
      return {
        recipe,
        recipeStore,
        availableProducts,
        isFormValid,
        addIngredient,
        removeIngredient,
        handleSubmit
      };
    }
  }
  </script>
  
  <style scoped>
  .recipe-add {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .recipe-add h1 {
    text-align: center;
    margin-bottom: 32px;
    color: #1f2937;
  }
  
  .recipe-form {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }
  
  .recipe-header {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .header-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  
  .recipe-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    min-height: 400px;
  }
  
  .ingredients-section h3,
  .instructions-section h3 {
    margin-bottom: 16px;
    color: #1f2937;
  }
  
  .ingredients-list {
    margin-bottom: 16px;
  }
  
  .ingredient-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding: 12px;
    background: #f9fafb;
    border-radius: 6px;
  }
  
  .ingredient-inputs {
    display: flex;
    gap: 8px;
    flex: 1;
  }
  
  .amount-input {
    width: 80px;
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
  }
  
  .unit-select {
    width: 100px;
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
  }
  
  .product-select {
    flex: 1;
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
  }
  
  .remove-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    padding: 4px;
    border-radius: 4px;
    transition: background-color 0.2s;
  }
  
  .remove-btn:hover {
    background-color: #fee2e2;
  }
  
  .instructions-textarea {
    width: 100%;
    height: 300px;
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-family: inherit;
    font-size: 14px;
    line-height: 1.5;
    resize: vertical;
  }
  
  .instructions-textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .form-group {
    margin-bottom: 16px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
    color: #374151;
  }
  
  .form-input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.2s ease;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .form-actions {
    display: flex;
    gap: 16px;
    justify-content: center;
    margin-top: 24px;
  }
  
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    text-align: center;
  }
  
  @media (max-width: 768px) {
    .recipe-content {
      grid-template-columns: 1fr;
      gap: 24px;
    }
    
    .header-row {
      grid-template-columns: 1fr;
    }
    
    .ingredient-inputs {
      flex-direction: column;
    }
    
    .amount-input,
    .unit-select,
    .product-select {
      width: 100%;
    }
    
    .form-actions {
      flex-direction: column;
    }
  }
  </style>