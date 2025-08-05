<template>
  <div class="recipe-add">
    <RecipeForm
      :loading="recipeStore.loading"
      :error="recipeStore.error"
      @submit="handleSubmit"
      @cancel="$router.push('/')"
    />
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { useRecipeStore } from '../stores/recipeStore.js';
import RecipeForm from '../components/forms/RecipeForm.vue';

export default {
  name: 'RecipeAdd',
  components: {
    RecipeForm
  },
  setup() {
    const router = useRouter();
    const recipeStore = useRecipeStore();

    const handleSubmit = async (recipeData) => {
      try {
        await recipeStore.createRecipe(recipeData);
        router.push('/recipes');
      } catch (error) {
        console.error('Error creating recipe:', error);
      }
    };

    return {
      recipeStore,
      handleSubmit
    };
  }
}
</script>

<style scoped>
.recipe-add {
  padding: 24px;
}
</style>