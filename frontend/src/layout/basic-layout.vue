<template>
    <div id="basic-layout">
        <el-container class="body" style="height: 100vh">
            <el-header class="header">
                <GlobalHeader/>
            </el-header>
            <el-container>
            <el-main class="content">
                <router-view/>
            </el-main>
            </el-container>
            <el-footer style="display: flex; justify-content: end; align-items: flex-start">
                <div class="logout-icon" @click="handleLogout">
                    Log out
                </div>
            </el-footer>
        </el-container>
    </div>
</template>

<script>
import GlobalHeader from '../components/GlobalHeader.vue'

export default {
    components: {
    GlobalHeader,
  },
  methods: {
    handleLogout() {
      this.$confirm('Are you sure you want to logout?', 'Logout', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        type: 'warning',
      })
        .then(() => {
          this.$message({
            type: 'success',
            message: 'You have logged out.',
          });
          this.$router.push('/login'); // 跳转到登录页面
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: 'Logout canceled',
          });
        });
    },
  },
}
</script>

<style scoped>
.content {
  position: relative;
}

.logout-icon {
  cursor: pointer;
  font-size: 20px;
  color: #7e0c6fd8;
  background: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.logout-icon:hover {
  transform: scale(1.1);
  color: #7E0C6E;
}
#basic-layout .content {
    padding: 0px 20px;
    background: linear-gradient(to bottom, #d188c6, #fff);
}

#basic-layout .header {
    background: #bb60af;
}

.el-header {
    --el-header-padding: 0;
    --el-header-height: 60px;
    box-sizing: border-box;
    flex-shrink: 0;
    height: var(--el-header-height);
    padding: var(--el-header-padding);
}

</style>