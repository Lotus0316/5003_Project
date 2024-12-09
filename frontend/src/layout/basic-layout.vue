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
        </el-container>
    </div>
</template>

<script>
import GlobalHeader from '../components/GlobalHeader.vue'
export default {
    components: {
    GlobalHeader,
  }
}
</script>

<style scoped>
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