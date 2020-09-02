<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 账本</el-breadcrumb-item>
                <el-breadcrumb-item>日结账本</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-input v-model="dailyquery.account_type" placeholder="输入账目类别" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            </div>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="index" align=center></el-table-column>
                <el-table-column prop="account_type" label="账目类别" align="center"></el-table-column>
                <el-table-column prop="net_profit" label="盈亏量" align=center></el-table-column>
                <el-table-column prop="unit" label="计量单位" align=center></el-table-column>
                <el-table-column prop="date" label="记录日期" align=center></el-table-column>
                <el-table-column prop="balance" label="结余" align=center></el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="dailyquery.pageIndex"
                    :page-size="dailyquery.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
import { fetchDailyData } from '../../api/dailyindex';
export default {
    name: 'dailyjournal',
    data() {
        return {
            dailyquery: {
                account_type: '',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [],
            pageTotal: 0,
            form: {},
            idx: -1,
            id: -1,
        };
    },
    created() {
        this.getData();
    },
    methods: {
        // 获取数据
        getData() {
            fetchDailyData(this.dailyquery).then(res => {
                console.log(res);
                this.tableData = res.list;
                this.pageTotal = res.pageTotal || 50;
            });
        },
        // 触发搜索按钮
        handleSearch() {
            this.$set(this.dailyquery, 'account_type', );
            this.getData();
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.dailyquery, 'pageIndex', val);
            this.getData();
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
