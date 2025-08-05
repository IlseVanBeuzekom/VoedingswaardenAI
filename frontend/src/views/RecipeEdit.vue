<template>
    <div class="recipe-edit">
      <div v-if="recipeStore.loading" class="loading">
        Recept laden...
      </div>
  
      <div v-else-if="recipeStore.error" class="error">
        {{ recipeStore.error }}
        <BaseButton 
          @click="$router.push('/recipes')"
          variant="secondary"
        >
          Terug naar overzicht
        </BaseButton>
      </div>
  
      <RecipeForm
        v-else-if="recipeStore.currentRecipe"
        :loading="recipeStore.loading"
        :error="recipeStore.error"
        :initial-data="recipeStore.currentRecipe"
        @submit="handleRecipeUpdate"
        @cancel="$router.push('/recipes')"
        mode="edit"
      />
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useRecipeStore } from '../stores/recipeStore.js';
  import RecipeForm from '../components/forms/RecipeForm.vue';
  import BaseButton from '../components/ui/BaseButton.vue';
  
  export default {
    name: 'RecipeEdit',
    components: {
      RecipeForm,
      BaseButton
    },
    setup() {
      const route = useRoute();
      const router = useRouter();
      const recipeStore = useRecipeStore();
  
      const recipeId = parseInt(route.params.id);
  
      onMounted(async () => {
        try {
          await recipeStore.fetchRecipeById(recipeId);
        } catch (error) {
          console.error('Error loading recipe:', error);
        }
      });
  
      const handleRecipeUpdate = async (recipeData) => {
        try {
          await recipeStore.updateRecipe(recipeId, recipeData);
          router.push('/recipes');
        } catch (error) {
          console.error('Error updating recipe:', error);
        }
      };
  
      return {
        recipeStore,
        handleRecipeUpdate
      };
    }
  }
  </script>
  
  <style scoped>
  .recipe-edit {
    padding: 24px;
  }
  
  .loading, .error {
    text-align: center;
    padding: 48px 24px;
  }
  
  .error {
    color: #dc2626;
    background-color: #fef2f2;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
  </style>