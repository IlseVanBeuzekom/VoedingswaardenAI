<template>
    <button 
      :class="buttonClasses"
      :disabled="disabled"
      @click="$emit('click')"
    >
      <slot></slot>
    </button>
  </template>
  
  <script>
  export default {
    name: 'BaseButton',
    emits: ['click'],
    props: {
      variant: {
        type: String,
        default: 'primary',
        validator: value => ['primary', 'secondary', 'danger'].includes(value)
      },
      size: {
        type: String,
        default: 'medium',
        validator: value => ['small', 'medium', 'large'].includes(value)
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      buttonClasses() {
        return [
          'btn',
          `btn--${this.variant}`,
          `btn--${this.size}`,
          { 'btn--disabled': this.disabled }
        ];
      }
    }
  }
  </script>
  
  <style scoped>
  .btn {
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  .btn--primary {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
  }
  
  .btn--primary:hover:not(.btn--disabled) {
    background-color: #e5e7eb;
  }
  
  .btn--secondary {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
  }
  
  .btn--secondary:hover:not(.btn--disabled) {
    background-color: #e5e7eb;
  }
  
  .btn--danger {
    background-color: #ef4444;
    color: white;
  }
  
  .btn--danger:hover:not(.btn--disabled) {
    background-color: #dc2626;
  }
  
  .btn--small {
    padding: 6px 12px;
    font-size: 14px;
  }
  
  .btn--medium {
    padding: 10px 20px;
    font-size: 16px;
  }
  
  .btn--large {
    padding: 14px 28px;
    font-size: 18px;
  }
  
  .btn--disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  </style>
  