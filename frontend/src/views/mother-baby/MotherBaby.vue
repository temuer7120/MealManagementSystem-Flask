<template>
  <div class="mother-baby-container">
    <el-container>
      <el-aside width="200px" class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          router
        >
          <el-menu-item index="/mother-baby/confinement-meal">
            <el-icon><Calendar /></el-icon>
            <span>月子餐计划</span>
          </el-menu-item>
          <el-menu-item index="/mother-baby/health">
            <el-icon><Medal /></el-icon>
            <span>健康记录</span>
          </el-menu-item>
          <el-menu-item index="/mother-baby/appointment">
            <el-icon><Ticket /></el-icon>
            <span>服务预约</span>
          </el-menu-item>
          <el-menu-item index="/mother-baby/nutrition">
            <el-icon><Food /></el-icon>
            <span>营养分析</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Calendar, Medal, Ticket, Food } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.fullPath)
</script>

<style scoped>
.mother-baby-container {
  height: 100vh;
  width: 100%;
}

.sidebar {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.el-menu-vertical-demo {
  height: 100%;
}

.el-main {
  padding: 20px;
  background-color: #f0f2f5;
}
</style>