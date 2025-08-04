<template>
    <div id="app">
      <nav class="navbar">
        <router-link to="/" class="nav-brand">
          Voedingswaarden App
        </router-link>
        
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/products" class="nav-link">Producten</router-link>
        </div>
      </nav>
  
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App'
  }
  </script>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #f9fafb;
    color: #1f2937;
    line-height: 1.6;
  }
  
  #app {
    min-height: 100vh;
  }
  
  .navbar {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
  }
  
  .nav-brand {
    font-size: 1.25rem;
    font-weight: bold;
    color: #1f2937;
    text-decoration: none;
  }
  
  .nav-links {
    display: flex;
    gap: 24px;
  }
  
  .nav-link {
    color: #6b7280;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
  }
  
  .nav-link:hover,
  .nav-link.router-link-active {
    color: #3b82f6;
  }
  
  .main-content {
    min-height: calc(100vh - 64px);
  }
  
  @media (max-width: 768px) {
    .navbar {
      padding: 0 16px;
    }
    
    .nav-links {
      gap: 16px;
    }
  }
  </style>