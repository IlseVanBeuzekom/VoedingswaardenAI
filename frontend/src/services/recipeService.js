import axios from 'axios';
import { Recipe } from '../models/Recipe.js';

const API_BASE_URL = 'http://localhost:8000/api';

class RecipeService {
  async createRecipe(recipeData) {
    const response = await axios.post(`${API_BASE_URL}/recipes/`, recipeData);
    return Recipe.fromAPI(response.data);
  }

  async getAllRecipes() {
    const response = await axios.get(`${API_BASE_URL}/recipes/`);
    return response.data.map(recipe => Recipe.fromAPI(recipe));
  }

  async getRecipeById(recipeId) {
    const response = await axios.get(`${API_BASE_URL}/recipes/${recipeId}`);
    return Recipe.fromAPI(response.data);
  }

  async updateRecipe(recipeId, recipeData) {
    const response = await axios.put(`${API_BASE_URL}/recipes/${recipeId}`, recipeData);
    return Recipe.fromAPI(response.data);
  }

  async deleteRecipe(recipeId) {
    await axios.delete(`${API_BASE_URL}/recipes/${recipeId}`);
  }

  calculateNutrition(recipe) {
    if (!recipe.ingredients || recipe.ingredients.length === 0) {
      return {
        energy_kcal: 0,
        proteins: 0,
        carbohydrates: 0,
        sugars: 0,
        fats: 0,
        fibers: 0
      };
    }
  
    const totals = recipe.ingredients.reduce((acc, ingredient) => {
      if (!ingredient.product) return acc;
      
      const product = ingredient.product;
      const factor = ingredient.amount / product.serving_size;
      
      acc.energy_kcal += (product.energy_kcal || 0) * factor;
      acc.proteins += (product.proteins || 0) * factor;
      acc.carbohydrates += (product.carbohydrates || 0) * factor;
      acc.sugars += (product.sugars || 0) * factor;
      acc.fats += (product.fats || 0) * factor;
      acc.fibers += (product.fibers || 0) * factor;
      
      return acc;
    }, {
      energy_kcal: 0,
      proteins: 0,
      carbohydrates: 0,
      sugars: 0,
      fats: 0,
      fibers: 0
    });
  
    // Divide by servings to get per portion
    const servings = recipe.servings || 1;
    Object.keys(totals).forEach(key => {
      totals[key] = totals[key] / servings;
    });
  
    return totals;
  }
}

export default new RecipeService();