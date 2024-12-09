<template>
    <el-menu
    :default-active="activeIndex"
    id="menu"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
    >
    <el-menu-item index="0" class="no-hover">
        <img style="width: 85px;" src="../img/CityULogo.webp" alt="logo" />
        <div style="font-size: large; margin-left: 8px; margin-top: 10px; margin-bottom: 0;">
        Team Formation System
        </div>
    </el-menu-item>
    <el-menu-item index="1" @click="goToStudentInfo">Student Information</el-menu-item>
    <el-menu-item index="2" @click="goToTeamDashboard">My Team</el-menu-item>
    <el-menu-item index="3" @click="goToTeamRequest">Team Application</el-menu-item>
    <el-menu-item index="4"><el-badge is-dot :offset="[0, 15]"><el-icon style="font-size: 35px;"><Message /></el-icon></el-badge></el-menu-item>
    </el-menu>

  </template>
  
  <script setup>
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'
    import { API_BASE_URL } from '@/config/api'
    
    const student = ref({
        sid: '',
        name: '',
        cur_major: '',
        email: ''
    })
    
    const router = useRouter()
    
    const sid = sessionStorage.getItem('user_sid')
    const token = sessionStorage.getItem('access_token')
    
    const activeIndex = ref(sessionStorage.getItem('activeIndex') || '1')
    
    const goToTeamDashboard = () => {
        if (student.value.sid) {
        router.push({
            name: 'TeamDashboard',
            params: { sid: student.value.sid }
        })
        updateActiveMenu(2)
        }
    }
    
    const goToTeamRequest = () => {
        if (student.value.sid) {
        router.push({
            name: 'TeamRequest',
            params: { sid: student.value.sid }
        })
        updateActiveMenu(3)
        }
    }
    
    const goToStudentInfo = () => {
        if (student.value.sid) {
        router.push({
            name: 'StudentInfo',
            params: { sid: student.value.sid }
        })
        updateActiveMenu(1)
        }
    }
    
    const loadStudentInfo = async () => {
        if (sid && token) {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/student/${sid}/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
            })
            student.value = response.data
        } catch (error) {
            if (error.response) {
            const status = error.response.status
            if (status === 403) {
                const currentSid = error.response.data.csid
                router.push({
                name: 'NoPermission',
                params: { reason: 'unauthorized', sid: currentSid }
                })
            } else if (status === 401) {
                router.push({ name: 'Login' })
            } else {
                console.error('Error loading student info:', error)
            }
            }
        }
        } else {
        console.error('No SID or token found in sessionStorage')
        router.push({ name: 'Login' })
        }
    }
    
    // 更新菜单的 active 状态并保存到 sessionStorage
    const updateActiveMenu = (index) => {
        activeIndex.value = index.toString()
        sessionStorage.setItem('activeIndex', activeIndex.value)
    }
    
    onMounted(async () => {
        await loadStudentInfo()
    })
  </script>
  

  <style>
    .no-hover:hover {
        background-color: transparent !important;
    }

    .no-hover {
        pointer-events: none !important;
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
        margin: 0px ;
        padding-left: 0;
        position: relative;
    }

    #menu.el-menu--horizontal>.el-menu-item.is-active {
        border-bottom: 2px solid #7E0C6E;
        color: #7E0C6E!important;
    }

    #menu.el-menu--horizontal>.el-menu-item {
        font-size: 17px;
    }

    #menu {
        --el-menu-hover-text-color: #3d0f37;
        --el-menu-active-color: #3d0f37;
        --el-menu-bg-color: #7e0c6f4f;
        --el-menu-hover-bg-color: #7e0c6f00;
    }

  </style>
  