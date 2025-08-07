<template>
  <div class="shopping-item" :class="{ 'checked': item.checked }">
    
    
    <div class="item-details">
      
      <div class="item-amount-control">
        <label class="item-checkbox">
        <input
          v-model="item.checked"
          type="checkbox"
          @change="$emit('toggle', item)"
        />
        <span class="checkmark"></span>
        </label>
        <input
          v-model.number="localAmount"
          type="number"
          step="0.1"
          min="0.1"
          class="amount-input"
          @blur="updateAmount"
          @keyup.enter="updateAmount"
        />
        <select v-model="localUnit" @change="updateUnit" class="unit-select">
          <option value="gram">gram</option>
          <option value="kg">kg</option>
          <option value="ml">ml</option>
          <option value="liter">liter</option>
          <option value="stuk">stuk</option>
          <option value="el">eetlepel</option>
          <option value="tl">theelepel</option>
          <option value="kopje">kopje</option>
        </select>

        <span class="item-name">{{ item.product_name }}</span>

        <button 
          @click="$emit('remove', item)"
          class="remove-btn"
          title="Verwijder item"
        >
          ❌
        </button>
      </div>
      
    </div>

    
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'ShoppingListItem',
  emits: ['toggle', 'updateAmount', 'updateUnit', 'remove'],
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const localAmount = ref(props.item.amount);
    const localUnit = ref(props.item.unit);

    watch(() => props.item.amount, (newAmount) => {
      localAmount.value = newAmount;
    });

    watch(() => props.item.unit, (newUnit) => {
      localUnit.value = newUnit;
    });

    const updateAmount = () => {
      if (localAmount.value > 0) {
        emit('updateAmount', props.item, localAmount.value);
      }
    };

    const updateUnit = () => {
      emit('updateUnit', props.item, localUnit.value);
    };

    return {
      localAmount,
      localUnit,
      updateAmount,
      updateUnit
    };
  }
}
</script>

<style scoped>
/* Bestaande styles blijven... */

.item-amount-control {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 4px;
}

.amount-input {
  width: 70px;
  padding: 4px 6px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.unit-select {
  padding: 4px 6px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  background: white;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 8px;
  border-radius: 4px;
  opacity: 0.7;
  transition: all 0.2s;
}

.remove-btn:hover {
  background-color: #fee2e2;
  opacity: 1;
}

.shopping-item {
  /* Update bestaande style */
  justify-content: space-between;
}
</style>