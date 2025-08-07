import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

class ShoppingListService {
  async getShoppingList(menuId) {
    const response = await axios.get(`${API_BASE_URL}/shopping-list/${menuId}`);
    return response.data;
  }
}

export default new ShoppingListService();