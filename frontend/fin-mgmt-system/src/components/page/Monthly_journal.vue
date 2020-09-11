<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 账本</el-breadcrumb-item>
                <el-breadcrumb-item>月结账本</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <!-- <div class="handle-box">
                <el-input v-model="monthlyquery.month" placeholder="输入月度（YYYY-MM）" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            </div> -->
       

            <el-table
                :data="tableData"
                border
                class="table"
                ref="monthlyJournalFormRef"
                header-cell-class-name="table-header"
            >
                <el-table-column type="index" align=center></el-table-column>
                <el-table-column prop="month" label="月度" align="center"></el-table-column>
                <el-table-column prop="revenue" label="收入" align=center>
                <template slot-scope="scope">￥{{scope.row.revenue}}</template></el-table-column>
                <el-table-column prop="cost" label="成本" align=center>
                  <template slot-scope="scope">￥{{scope.row.cost}}</template></el-table-column>
                <el-table-column prop="net_profit" label="利润" align=center>
                  <template slot-scope="scope">￥{{scope.row.cost}}</template></el-table-column>
                <el-table-column prop="balance" label="结余" align=center>
                  <template slot-scope="scope">￥{{scope.row.cost}}</template></el-table-column>
                <el-table-column prop="date" label="记录日期" align=center></el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="monthlyquery.pageIndex"
                    :page-size="monthlyquery.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
import { fetchMonthlyData } from '../../api/monthlyjournal';
export default {
    name: 'Monthlyjournal',
    data() {
        return {
            monthlyquery: {
                month: '',
                revenue:'',
                cost:'',
                net_profit:'',
                balance:'',
                date:'',
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
            fetchMonthlyData(this.monthlyquery).then(res => {
                console.log(res);
                this.tableData = res.list;
                this.pageTotal = res.pageTotal;
            });
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.monthlyquery, 'pageIndex', val);
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
