<template>
    <div class="header">
        <div class="logo">
            <div class="header-left">
                <!-- 系统名称 -->
            <h4>餐饮财务管理系统</h4>
            </div>
        </div>
        <div class="header-right">
            <div class="header-user-con">
                <!-- 用户退出按钮 -->
                 <el-button type="info" @click="logout">退出</el-button>
            </div>
        </div>
    </div>
</template>

<script>
import bus from '../common/bus';
export default {
    methods: {
        
    logout() {
      window.sessionStorage.clear;
      this.$router.push("/login");
    }
    },
    mounted() {
        if (document.body.clientWidth < 1500) {
            this.collapseChage();
        }
    }
};
</script>

<style scoped>
.header {
    position: relative;
    box-sizing: border-box;
    width: 100%;
    height: 70px;
    font-size: 22px;
    color: #fff;
}
.header .logo {
    float: left;
    width: 250px;
    line-height: 70px;
}
.header-left {
    float: left;
    padding-left: 30px;
}
.header-right {
    float: right;
    padding-right: 50px;
}
.header-user-con {
    display: flex;
    height: 70px;
    align-items: center;
}

</style>
