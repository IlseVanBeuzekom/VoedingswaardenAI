<template>
    <div class="recipe-form-container">
      <h1>{{ mode === 'edit' ? 'Recept Bewerken' : 'Nieuw Recept' }}</h1>
      <div class="image-section">
        <div class="image-preview" v-if="form.image_url || imagePreview">
          <img 
            :src="imagePreview || `http://localhost:8000${form.image_url}`" 
            alt="Recipe image"
            class="recipe-image"
          />
          <button 
            @click="removeImage" 
            type="button" 
            class="remove-image-btn"
            title="Afbeelding verwijderen"
          >
            ❌
          </button>
        </div>
        
        <div class="image-upload" v-else>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleImageSelect"
            style="display: none"
          />
          <button 
            @click="$refs.fileInput.click()"
            type="button"
            class="upload-btn"
          >
            📷 Afbeelding toevoegen
          </button>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="recipe-form">
        <!-- Basic Recipe Info -->
        <div class="recipe-header">
          <div class="form-group">
            <label for="name">Receptnaam*</label>
            <input
              v-model="form.name"
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
                v-model.number="form.servings"
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
                v-model.number="form.preparation_time"
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
                v-for="(ingredient, index) in form.ingredients" 
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
                  
                  <select v-model="ingredient.unit" class="unit-select">
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
              v-model="form.instructions"
              class="instructions-textarea"
              placeholder="Beschrijf hier stap voor stap hoe het recept wordt bereid..."
              required
            ></textarea>
          </div>
        </div>

        <NutritionSummary 
          v-if="form.ingredients.length > 0" 
          :nutritionData="recipeNutrition" 
        />
  
        <!-- Submit Button -->
        <div class="form-actions">
          <BaseButton 
            type="submit"
            :disabled="!isFormValid || loading"
            variant="primary"
          >
            {{ loading ? 'Bezig met opslaan...' : (mode === 'edit' ? 'Recept Bijwerken' : 'Recept Opslaan') }}
          </BaseButton>
          
          <BaseButton 
            @click="$emit('cancel')"
            variant="secondary"
            type="button"
          >
            Annuleren
          </BaseButton>
        </div>
  
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { reactive, ref, computed, watch, onMounted } from 'vue';
  import { useProductStore } from '../../stores/productStore.js';
  import { Recipe } from '../../models/Recipe.js';
  import BaseButton from '../ui/BaseButton.vue';
  import NutritionSummary from '../ui/NutritionSummary.vue';
  import recipeService from '../../services/recipeService.js';
  
  export default {
    name: 'RecipeForm',
    components: {
      BaseButton,
      NutritionSummary
    },
    emits: ['submit', 'cancel'],
    props: {
      loading: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: null
      },
      initialData: {
        type: Object,
        default: null
      },
      mode: {
        type: String,
        default: 'create',
        validator: value => ['create', 'edit'].includes(value)
      }
    },
    setup(props, { emit }) {
      const productStore = useProductStore();
      const form = reactive(new Recipe());
  
      const availableProducts = computed(() => productStore.products);
  
      watch(() => props.initialData, (newData) => {
        if (newData) {
          Object.assign(form, {
            ...newData,
            ingredients: newData.ingredients ? [...newData.ingredients] : []
          });
        }
      }, { immediate: true });
  
      const imagePreview = ref(null);
      const selectedImage = ref(null);

      const handleImageSelect = (event) => {
        const file = event.target.files[0];
        if (file) {
          selectedImage.value = file;
          const reader = new FileReader();
          reader.onload = (e) => {
            imagePreview.value = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      };

      const removeImage = () => {
        imagePreview.value = null;
        selectedImage.value = null;
        form.image_url = null;
      };

      const isFormValid = computed(() => {
        return form.name.trim().length > 0 &&
               form.servings > 0 &&
               form.preparation_time > 0 &&
               form.instructions.trim().length > 0 &&
               form.ingredients.length > 0 &&
               form.ingredients.every(ing => 
                 ing.product_id && ing.amount > 0 && ing.unit.trim().length > 0
               );
      });
  
      const addIngredient = () => {
        form.addIngredient();
      };
  
      const removeIngredient = (index) => {
        form.removeIngredient(index);
      };
  
      const handleSubmit = () => {
        if (isFormValid.value) {
          const submitData = {
            ...form.toAPI(),
            image: selectedImage.value
          }

          emit('submit', submitData);
        }
      };

      const recipeNutrition = computed(() => {
        // Create a temporary recipe object with current form data
        const tempRecipe = {
          ...form,
          ingredients: form.ingredients.map(ing => ({
            ...ing,
            product: availableProducts.value.find(p => p.id === ing.product_id)
          }))
        };
        return recipeService.calculateNutrition(tempRecipe);
      });
  
      // Load products on mount
      onMounted(async () => {
        try {
          await productStore.fetchProducts();
          // Add empty ingredient only for create mode
          if (props.mode === 'create' && form.ingredients.length === 0) {
            addIngredient();
          }
        } catch (error) {
          console.error('Error loading products:', error);
        }
      });
  
      return {
        form,
        availableProducts,
        isFormValid,
        addIngredient,
        removeIngredient,
        handleSubmit,
        recipeNutrition,
        imagePreview,
        handleImageSelect,
        removeImage
      };
    }
  }
  </script>
  
  <style scoped>
  .image-section {
    margin-bottom: 32px;
    text-align: center;
  }

  .image-preview {
    position: relative;
    display: inline-block;
  }

  .recipe-image {
    max-width: 500px;
    max-height: 400px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .remove-image-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .upload-btn {
    background: #f3f4f6;
    border: 2px dashed #d1d5db;
    border-radius: 8px;
    padding: 40px 60px;
    cursor: pointer;
    font-size: 16px;
    color: #6b7280;
    transition: all 0.2s;
  }

  .upload-btn:hover {
    border-color: #3b82f6;
    background: #f0f9ff;
  }

  .recipe-form-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .recipe-form-container h1 {
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