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
}

export default new RecipeService();