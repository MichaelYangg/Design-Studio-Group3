<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 交易信息
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-input v-model="query.transaction_id" placeholder="输入交易编号" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button type="primary" @click="dialogVisible = true">添加交易信息</el-button>
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
                <el-table-column prop="transaction_id" label="交易编号" align="center"></el-table-column>
                <el-table-column prop="volume" label="交易额" align=center></el-table-column>
                <el-table-column prop="unit" label="交易单位" align=center></el-table-column>
                <el-table-column prop="time_date" label="交易日期时间" align=center>

                  
                </el-table-column>
                <el-table-column prop="resource" label="交易类型" align=center></el-table-column>
                <el-table-column prop="category" label="交易物品类别" align=center></el-table-column>
                <el-table-column prop="explanation" label="注释" align=center></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="query.pageIndex"
                    :page-size="query.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>

 <!-- 添加交易信息对话框 -->
    <el-dialog
      title="添加交易信息"
      :visible.sync="dialogVisible"
      width="80%"
      @close="addDialogClosed"
    >
      <el-form
        :model="addTransactionForm"
        :rules="addTransactionFormRules"
        ref="addTransactionFormRef"
        label-width="110px"
        class="demo-ruleForm"
      >
        <el-form-item label="交易编号" prop="transaction_id">
          <el-input v-model="addTransactionForm.transaction_id"></el-input>
        </el-form-item>
        <el-form-item label="交易额" prop="volume">
          <el-input v-model="addTransactionForm.volume"></el-input>
        </el-form-item>
        <el-form-item label="交易单位" prop="unit">
          <el-input v-model="addTransactionForm.unit"></el-input>
        </el-form-item>
        <el-form-item label="交易日期时间" prop="time_date">
          <el-input v-model="addTransactionForm.time_date"></el-input>
        </el-form-item>
        <el-form-item label="交易类型" prop="resource">
          <el-input v-model="addTransactionForm.resource"></el-input>
        </el-form-item>
        <el-form-item label="交易物品类别" prop="category">
          <el-input v-model="addTransactionForm.category"></el-input>
        </el-form-item>
        <el-form-item label="注释" prop="explanation">
          <el-input v-model="addTransactionForm.explanation"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addTransaction">确 定</el-button>
      </span>
    </el-dialog>


        <!-- 修改交易信息弹出框 -->
        <el-dialog title="编辑交易信息" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="交易编号">
                    <el-input v-model="form.transaction_id" disabled></el-input>
                </el-form-item>
                <el-form-item label="交易额">
                    <el-input v-model="form.volume"></el-input>
                </el-form-item>
                 <el-form-item label="交易单位">
                    <el-input v-model="form.unit"></el-input>
                </el-form-item>
                 <el-form-item label="交易日期时间">
                    <el-input v-model="form.time_date"></el-input>
                </el-form-item>
                 <el-form-item label="交易类型">
                    <el-input v-model="form.resource"></el-input>
                </el-form-item>
                 <el-form-item label="交易物品类别">
                    <el-input v-model="form.category"></el-input>
                </el-form-item>
                 <el-form-item label="注释">
                    <el-input v-model="form.explanation"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { fetchData } from '../../api/transactions';
export default {
    name: 'transaction',
    data() {
        return {
            query: {
                transaction_id: '',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [],
            dialogVisible: false,
            editVisible: false,
            pageTotal: 0,
            form: {},
            idx: -1,
            id: -1,
    addTransactionForm: {
        transaction_id:"",
        volume:"",
        unit:"",
        time_date:"",
        resource:"",
        category:"",
        explanation:""
      },
      addTransactionFormRules: {
        transaction_id: [
          { required: true, message: "请输入交易编号", trigger: "blur"},
          {
            require: true,
            trigger: "blur"
          }
        ],
        volume: [
          { required: true, message: "请输入交易单位", trigger: "blur" },
          {
            require: true,
            trigger: "blur"
          }
        ],
        unit: [
          { required: true, message: "请选择交易单位", trigger: "blur" },
          {
            require: true, trigger: "blur"
          }
        ],
        time_date: [
          { required: true, message: "请输入交易日期时间", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        resource: [
          { required: true, message: "0：收银 1：储值 2：入库 3：出库 4：加工费用 5：盘亏盘盈 6：外卖 7：其他", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        category: [
          { required: true, message: "请输入交易物品类别", trigger: "blur"},
          { require: true, trigger: "blur"}
        ]
      },
      editTransactionForm: {},
      editTransactionFormRules: {
        volume: [
          { required: true, message: "请输入交易额", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        unit: [
          { required: true, message: "请输入交易单位", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        time_date: [
          { required: true, message: "请输入交易日期时间", trigger: "blur"},
          { require: true, trigger: "blur"}
        ],
        resource: [
          { required: true, message: "0：收银 1：储值 2：入库 3：出库 4：加工费用 5：盘亏盘盈 6：外卖 7：其他", trigger: "blur"},
          { require: true, trigger: "blur"}
        ],
        category: [
          { required: true, message: "请输入交易物品类别", trigger: "blur" },
          { require: true, trigger: "blur"}
        ],
      },
        };
    },
    created() {
        this.getData();
    },
    methods: {
        // 获取数据
        getData() {
            fetchData(this.query).then(res => {
                console.log(res);
                this.tableData = res.list;
                this.pageTotal = res.pageTotal || 50;
            });
        },
        // 触发搜索按钮
        handleSearch() {
            this.$set(this.query, 'transaction_id', );
            this.getData();
        },
        // 新增操作
         addTransaction() {
        this.$refs.addTransactionFormRef.validate(async valid => {
        if (!valid) return;
        const { data } = await this.$http.post("users", this.addTransactionForm);
        if (data.meta.status !== 201) {
          this.$message.error("新增失败");
        }
        this.$message.success("新增成功");
        this.dialogVisible = false;
        this.getTransactionList();
        });
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    this.$message.success('删除成功');
                    this.tableData.splice(index, 1);
                })
                .catch(() => {});
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit() {
            this.editVisible = false;
            this.$message.success('修改成功');
            this.$set(this.tableData, this.idx, this.form);
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
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
