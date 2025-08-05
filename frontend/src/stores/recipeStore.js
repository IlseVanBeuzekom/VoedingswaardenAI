import { defineStore } from 'pinia';
import recipeService from '../services/recipeService.js';

export const useRecipeStore = defineStore('recipe', {
  state: () => ({
    recipes: [],
    currentRecipe: null,
    loading: false,
    error: null
  }),

  actions: {
    async createRecipe(recipeData) {
      this.loading = true;
      this.error = null;
      
      try {
        const newRecipe = await recipeService.createRecipe(recipeData);
        this.recipes.push(newRecipe);
        return newRecipe;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchRecipes() {
      this.loading = true;
      this.error = null;
      
      try {
        this.recipes = await recipeService.getAllRecipes();
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchRecipeById(recipeId) {
      this.loading = true;
      this.error = null;
      
      try {
        this.currentRecipe = await recipeService.getRecipeById(recipeId);
        return this.currentRecipe;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Recept niet gevonden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateRecipe(recipeId, recipeData) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedRecipe = await recipeService.updateRecipe(recipeId, recipeData);
        
        const index = this.recipes.findIndex(r => r.id === recipeId);
        if (index !== -1) {
          this.recipes[index] = updatedRecipe;
        }
        
        this.currentRecipe = updatedRecipe;
        return updatedRecipe;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteRecipe(recipeId) {
      this.loading = true;
      this.error = null;
      
      try {
        await recipeService.deleteRecipe(recipeId);
        
        this.recipes = this.recipes.filter(r => r.id !== recipeId);
        
        if (this.currentRecipe?.id === recipeId) {
          this.currentRecipe = null;
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});