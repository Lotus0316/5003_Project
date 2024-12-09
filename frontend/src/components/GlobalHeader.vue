<template>
    <el-menu
      :default-active="activeIndex"
      id="menu"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
    >
      <el-menu-item index="0" class="no-hover">
        <img
          style="width: 100px;"
          src="../img/CityULogo.webp"
          alt="logo"
        />
        <div style="font-size: large;margin-left: 10px;margin-top: 10px;margin-bottom: 0;">Team Formation System</div>
      </el-menu-item>
      <el-menu-item index="1">Student Information</el-menu-item>
      <el-menu-item index="2">My Team</el-menu-item>
      <el-menu-item index="3">Team Application</el-menu-item>
      <el-menu-item index="4"><el-icon><Notification /></el-icon></el-menu-item>
    </el-menu>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const activeIndex = ref('1')
  const handleSelect = (key, keyPath) => {
    console.log(key, keyPath)
  }
  </script>
  
  <style>
    .no-hover:hover {
    background-color: transparent !important; /* 禁用背景颜色变化 */
    }

    .no-hover {
    pointer-events: none !important; /* 允许点击事件 */
    }

    #menu.el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
    }

    #menu.el-menu--horizontal.el-menu {
    border-bottom: 1px solid #FFFFFF00 ;
    }

    #menu.el-menu {
    background-color: #FFFFFF00 ;
    border-right: 1px solid var(--el-menu-border-color);
    box-sizing: border-box;
    list-style: none;
    margin: 8px 0px ;
    padding-left: 0;
    position: relative;
    }

    #menu.el-menu--horizontal>.el-menu-item.is-active {
    border-bottom: 2px solid #7E0C6E;
    color: #7E0C6E!important;
    }

    #menu {
    --el-menu-hover-text-color: #7E0C6E;
    --el-menu-active-color: #7E0C6E;
    --el-menu-bg-color: #7e0c6f4f;
    --el-menu-hover-bg-color: #7e0c6f4f;
    }
  </style>
  