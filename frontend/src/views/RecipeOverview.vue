<template>
    <div class="recipe-overview">
      <div class="header">
        <h1>Recept Overzicht</h1>
        <BaseButton 
          @click="$router.push('/recipes/add')"
          variant="primary"
        >
          Nieuw Recept
        </BaseButton>
      </div>
  
      <!-- Search Bar -->
      <div class="search-section">
        <div class="search-bar">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Zoek op ingrediënt (bijv. tomaat, kip, pasta...)"
            class="search-input"
          />
          <button 
            v-if="searchQuery"
            @click="clearSearch"
            class="clear-btn"
            title="Wissen"
          >
            ❌
          </button>
        </div>
        
        <!-- <div v-if="searchQuery && filteredRecipes.length > 0" class="search-results-info">
          Recepten met ingrediënt "{{ searchQuery }}" ({{ filteredRecipes.length }})
        </div> -->
        
        <div v-if="searchQuery && filteredRecipes.length === 0 && !recipeStore.loading" class="no-results">
          Geen recepten gevonden met ingrediënt "{{ searchQuery }}"
        </div>
      </div>

      <div v-if="recipeStore.loading" class="loading">
        Recepten laden...
      </div>
  
      <div v-else-if="recipeStore.error" class="error">
        {{ recipeStore.error }}
      </div>
  
      <div v-else-if="recipeStore.recipes.length === 0" class="empty-state">
        <p>Nog geen recepten toegevoegd.</p>
        <BaseButton 
          @click="$router.push('/recipes/add')"
          variant="primary"
        >
          Voeg je eerste recept toe
        </BaseButton>
      </div>
  
      <div v-else class="recipes-grid">
        <RecipeCard
          v-for="recipe in filteredRecipes" 
          :key="recipe.id"
          :recipe="recipe"
          @edit="editRecipe"
          @delete="deleteRecipe"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { useRecipeStore } from '../stores/recipeStore.js';
  import BaseButton from '../components/ui/BaseButton.vue';
  import RecipeCard from '../components/ui/RecipeCard.vue';
  
  export default {
    name: 'RecipeOverview',
    components: {
      BaseButton,
      RecipeCard
    },
    setup() {
      const recipeStore = useRecipeStore();
      const router = useRouter();
      const searchQuery = ref('');
  
      const filteredRecipes = computed(() => {
        if (!searchQuery.value.trim()) {
          return recipeStore.recipes;
        }
        
        const query = searchQuery.value.toLowerCase().trim();
        
        return recipeStore.recipes.filter(recipe => {
          // Zoek in ingrediënten
          return recipe.ingredients.some(ingredient => {
            if (ingredient.product?.name) {
              return ingredient.product.name.toLowerCase().includes(query);
            }
            return false;
          });
        });
      });
  
      const clearSearch = () => {
        searchQuery.value = '';
      };

      onMounted(async () => {
        await recipeStore.fetchRecipes();
      });
  
      const editRecipe = (recipeId) => {
        router.push(`/recipes/edit/${recipeId}`);
      };
  
      const deleteRecipe = async (recipeId) => {
        const recipe = recipeStore.recipes.find(r => r.id === recipeId);
        if (confirm(`Weet je zeker dat je "${recipe?.name}" wilt verwijderen?`)) {
          try {
            await recipeStore.deleteRecipe(recipeId);
          } catch (error) {
            console.error('Error deleting recipe:', error);
          }
        }
      };
  
      return {
        recipeStore,
        searchQuery,
        filteredRecipes,
        clearSearch,
        editRecipe,
        deleteRecipe
      };
    }
  }
  </script>
  
  <style scoped>
  .search-section {
    margin-bottom: 32px;
  }

  .search-bar {
    position: relative;
    max-width: 500px;
    margin: 0 auto;
  }

  .search-input {
    width: 100%;
    padding: 12px 50px 12px 16px;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .clear-btn {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    padding: 4px;
    border-radius: 4px;
    opacity: 0.6;
    transition: opacity 0.2s;
  }

  .clear-btn:hover {
    opacity: 1;
    background-color: #f3f4f6;
  }

  .search-results-info {
    text-align: center;
    margin-top: 12px;
    color: #059669;
    background-color: #ecfdf5;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
  }

  .recipe-overview {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }
  
  .header h1 {
    color: #1f2937;
    margin: 0;
  }
  
  .loading, .error, .empty-state {
    text-align: center;
    padding: 48px 24px;
  }
  
  .error {
    color: #dc2626;
    background-color: #fef2f2;
    border-radius: 8px;
  }
  
  .empty-state p {
    color: #6b7280;
    margin-bottom: 24px;
  }
  
  .recipes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 24px;
  }
  
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }
    
    .search-bar {
      max-width: 100%;
    }

    .recipes-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>