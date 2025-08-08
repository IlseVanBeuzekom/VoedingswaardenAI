import axios from 'axios';
import { DailyFoodLog, DailyFoodEntry } from '../models/DailyFoodLog.js';

const API_BASE_URL = 'http://localhost:8000/api';

class DailyFoodService {
  async getDailyLog(date) {
    const response = await axios.get(`${API_BASE_URL}/daily-food/${date}`);
    return DailyFoodLog.fromAPI(response.data);
  }

  async addEntry(date, entryData) {
    const response = await axios.post(`${API_BASE_URL}/daily-food/${date}/entries`, entryData);
    return DailyFoodEntry.fromAPI(response.data);
  }

  async updateEntry(entryId, entryData) {
    const response = await axios.put(`${API_BASE_URL}/daily-food/entries/${entryId}`, entryData);
    return DailyFoodEntry.fromAPI(response.data);
  }

  async deleteEntry(entryId) {
    await axios.delete(`${API_BASE_URL}/daily-food/entries/${entryId}`);
  }
}

export default new DailyFoodService();