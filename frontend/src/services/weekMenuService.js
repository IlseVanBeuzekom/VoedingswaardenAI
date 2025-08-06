import axios from 'axios';
import { WeekMenu } from '../models/WeekMenu.js';

const API_BASE_URL = 'http://localhost:8000/api';

class WeekMenuService {
  async createWeekMenu(menuData) {
    const response = await axios.post(`${API_BASE_URL}/weekmenus/`, menuData);
    return WeekMenu.fromAPI(response.data);
  }

  async getAllWeekMenus() {
    const response = await axios.get(`${API_BASE_URL}/weekmenus/`);
    return response.data.map(menu => WeekMenu.fromAPI(menu));
  }

  async getWeekMenuById(menuId) {
    const response = await axios.get(`${API_BASE_URL}/weekmenus/${menuId}`);
    return WeekMenu.fromAPI(response.data);
  }

  async getWeekMenuByDateRange(startDate, endDate) {
    const response = await axios.get(`${API_BASE_URL}/weekmenus/by-date`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return WeekMenu.fromAPI(response.data);
  }

  async updateWeekMenu(menuId, menuData) {
    const response = await axios.put(`${API_BASE_URL}/weekmenus/${menuId}`, menuData);
    return WeekMenu.fromAPI(response.data);
  }

  async deleteWeekMenu(menuId) {
    await axios.delete(`${API_BASE_URL}/weekmenus/${menuId}`);
  }
}

export default new WeekMenuService();