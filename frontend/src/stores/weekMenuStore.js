import { defineStore } from 'pinia';
import weekMenuService from '../services/weekMenuService.js';

export const useWeekMenuStore = defineStore('weekMenu', {
  state: () => ({
    weekMenus: [],
    currentWeekMenu: null,
    loading: false,
    error: null
  }),

  actions: {
    async createWeekMenu(menuData) {
      this.loading = true;
      this.error = null;
      
      try {
        const newMenu = await weekMenuService.createWeekMenu(menuData);
        this.weekMenus.push(newMenu);
        return newMenu;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchWeekMenus() {
      this.loading = true;
      this.error = null;
      
      try {
        this.weekMenus = await weekMenuService.getAllWeekMenus();
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchWeekMenuById(menuId) {
      this.loading = true;
      this.error = null;
      
      try {
        this.currentWeekMenu = await weekMenuService.getWeekMenuById(menuId);
        return this.currentWeekMenu;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Weekmenu niet gevonden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchWeekMenuByDateRange(startDate, endDate) {
      this.loading = true;
      this.error = null;
      
      try {
        this.currentWeekMenu = await weekMenuService.getWeekMenuByDateRange(startDate, endDate);
        return this.currentWeekMenu;
      } catch (error) {
        if (error.response?.status === 404) {
          this.currentWeekMenu = null;
          return null;
        }
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateWeekMenu(menuId, menuData) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedMenu = await weekMenuService.updateWeekMenu(menuId, menuData);
        
        const index = this.weekMenus.findIndex(m => m.id === menuId);
        if (index !== -1) {
          this.weekMenus[index] = updatedMenu;
        }
        
        this.currentWeekMenu = updatedMenu;
        return updatedMenu;
      } catch (error) {
        this.error = error.response?.data?.detail || 'Er is een fout opgetreden';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteWeekMenu(menuId) {
      this.loading = true;
      this.error = null;
      
      try {
        await weekMenuService.deleteWeekMenu(menuId);
        
        this.weekMenus = this.weekMenus.filter(m => m.id !== menuId);
        
        if (this.currentWeekMenu?.id === menuId) {
          this.currentWeekMenu = null;
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