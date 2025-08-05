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
          v-for="recipe in recipeStore.recipes" 
          :key="recipe.id"
          :recipe="recipe"
          @edit="editRecipe"
          @delete="deleteRecipe"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
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
        editRecipe,
        deleteRecipe
      };
    }
  }
  </script>
  
  <style scoped>
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
    
    .recipes-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>