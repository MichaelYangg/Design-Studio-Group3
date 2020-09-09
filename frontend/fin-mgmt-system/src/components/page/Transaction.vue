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
                <el-input v-model="search" placeholder="输入交易编号" clearable @clear="handleSearch" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button type="primary" @click="dialogVisible=true">添加交易信息</el-button>
            </div>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
            >
                <el-table-column type="index" align=center></el-table-column>
                <el-table-column prop="transaction_id" label="交易编号" align="center"></el-table-column>
                <el-table-column prop="volume" label="交易额" align=center></el-table-column>
                <el-table-column prop="unit" label="交易单位" align=center></el-table-column>
                <el-table-column prop="date_time" label="交易日期时间" :formatter="dateTimeFormat" align=center></el-table-column>
                <el-table-column prop="resource" label="交易类型" align=center></el-table-column>
                <el-table-column prop="category" label="交易物品类别" align=center></el-table-column>
                <el-table-column prop="explanation" label="注释" align=center></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)">
                        编辑</el-button>
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
      title="新增交易信息"
      :visible.sync="dialogVisible"
      width="80%"
    >
      <el-form
        :model="addTransactionForm"
        :rules="addTransactionFormRules"
        ref="addTransactionFormRef"
        label-width="110px"
        class="demo-ruleForm"
      >
        <el-form-item label="交易编号" prop="transaction_id">
          <el-input v-model="addTransactionForm.transaction_id" placeholder="请输入交易编号"></el-input>
        </el-form-item>
        <el-form-item label="交易额" prop="volume">
          <el-input v-model="addTransactionForm.volume" placeholder="请输入交易额"></el-input>
        </el-form-item>
        <el-form-item label="交易单位" prop="unit">
          <el-input v-model="addTransactionForm.unit" placeholder="请输入交易单位"></el-input>
        </el-form-item>
        <el-form-item label="交易日期时间" prop="date_time" >
          <el-input v-model="addTransactionForm.date_time" placeholder="YYYY-MM-DD HH:mm:ss"></el-input>
        </el-form-item>
        <el-form-item label="交易类型" prop="resource">
          <el-input v-model="addTransactionForm.resource" placeholder="0：收银 1：储值 2：入库 3：出库 4：加工费用 5：盘亏盘盈 6：外卖 7：其他"></el-input>
        </el-form-item>
        <el-form-item label="交易物品类别" prop="category">
          <el-input v-model="addTransactionForm.category" placeholder="请输入交易物品类别"></el-input>
        </el-form-item>
        <el-form-item label="注释" prop="explanation" placeholder="请输入注释">
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
            <el-form ref="editTransactionFormRef" :model="editTransactionForm" :rules="editTransactionFormRules" label-width="70px">
                <el-form-item label="交易编号">
                    <el-input v-model="editTransactionForm.transaction_id" disabled></el-input>
                </el-form-item>
                <el-form-item label="交易额">
                    <el-input v-model="editTransactionForm.volume"></el-input>
                </el-form-item>
                 <el-form-item label="交易单位">
                    <el-input v-model="editTransactionForm.unit"></el-input>
                </el-form-item>
                 <el-form-item label="交易日期时间">
                    <el-input v-model="editTransactionForm.date_time"></el-input>
                </el-form-item>
                 <el-form-item label="交易类型">
                    <el-input v-model="editTransactionForm.resource"></el-input>
                </el-form-item>
                 <el-form-item label="交易物品类别">
                    <el-input v-model="editTransactionForm.category"></el-input>
                </el-form-item>
                 <el-form-item label="注释">
                    <el-input v-model="editTransactionForm.explanation"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 删除交易信息弹出框 -->
        <el-dialog title="删除交易信息" :visible.sync="deleteVisible" width="30%">
         <span>确定要删除吗？</span>
         <span slot="footer" class="dialog-footer">
           <el-button @click="deleteVisible=false">取 消</el-button>
           <el-button type="warning" @click="deleteTransaction()">删 除</el-button>
         </span>
        </el-dialog>

    </div>
</template>

<script>
import { fetchData, addList, editList, deleteList, queryTransaction } from '../../api/transactions';
import moment from 'moment'
export default {
    name: 'Transaction',
    data() {
        return {
            query: {
                transaction_id: '',
                volume:'',
                unit:'',
                date_time:'',
                resource:'',
                category:'',
                explanation:'',
                pageIndex: 1,
                pageSize: 10
            },
            search:'',
            tableData: [],
            // searchData: [],
            dialogVisible: false,
            editVisible: false,
            deleteVisible: false,
            pageTotal: 0,
            form: {},
            idx: -1,
            id: -1,
    // filters: {
    //   transaction_id:''
    // },
    addTransactionForm: {
        transaction_id:'',
        volume:'',
        unit:'',
        date_time:'',
        resource:'',
        category:'',
        explanation:''
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
        date_time: [
          { required: true, message: "请输入交易日期时间 (ex. 2020-09-04 00:00:00)", trigger: "blur" },
          { require: true, pattern: '', trigger: "blur" }
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
      editTransactionForm: {
        transaction_id:'',
        volume:'',
        unit:'',
        date_time:'',
        resource:'',
        category:'',
        explanation:''
      },
      editTransactionFormRules: {
        transaction_id: [

        ],
        volume: [
          { required: true, message: "请输入交易额", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        unit: [
          { required: true, message: "请输入交易单位", trigger: "blur" },
          { require: true, trigger: "blur" }
        ],
        date_time: [
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
    // computed: {
    //   tableData(){
    //   if(this.search) {
    //     return.this.tableData.filter(item =>
    //     Object.keys(item).some(key =>
    //     String(item[key]).toLowerCase().indexOf(this.search) > -1
    //     )
    //     );
    //   } else return this.tableData;
    // },
    methods: {
        getData() {
            fetchData(this.query).then(res => {
                this.tableData = res.list;
                this.pageTotal = res.pageTotal;
            });
        },

        // 触发搜索按钮
        handleSearch () {
              this.$set(this.query, 'pageIndex', 1);
              this.getData();
        //     // this.$set(this.query, 'transaction_id');
             queryTransaction(this.query.transaction_id).then(res => {
                 var list = [];
                 list.append(res);
                 console.log(list);
                 this.tableData = res.list;
                 this.pageTotal = 1;
             })
             .catch( () => {
             })   
        },
        // 新增操作
         addTransaction() {
        // // 二次进行用户数据的验证
          console.log("here in add transaction")
        //    this.$refs.addTransactionFormRef.validate(valid => {
        //      if (valid) {
               //发起新增交易信息请求
               addList(this.addTransactionForm)
               .then(res => {
                 if (res.data.meta.status === 201) {
                   this.$message.success('新增交易信息成功')
                  //  ({
                  //    type: 'success',
                  //    message: '新增交易信息成功'
                  //  })
                   //数据刷新
                   this.dialogVisible = false
                   //表单元素的数据重置
                   this.$refs.addTransactionFormRef.resetFields()
                   this.init()
                 } else {
                   this.$message.error('新增交易信息失败')
                  //  ({
                  //    type: 'error',
                  //    message: '新增交易信息失败'
                  //  })
                 }
               })
                  .catch( () => {
                    this.$message.info('已取消新增交易信息')
                    // ({
                    //   type: 'error',
                    //   message: '新增交易信息失败'
                    // })
                  })
            //  } else {
            //    //中止此次请求
            //    console.log("here")
            //    return false
            //  }
          //  })
    },

        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该信息吗？', '提示', {
                confirmButtonText: "确 定",
                cancelButtonText: "取 消",
                type: 'warning'
            })
            .then(() => {
           //发起删除请求
            deleteList(this.tableData)
            .then(res => {
              if(res.data.meta.status === 200) {
                this.$message.success('删除成功');
                // ({
                //   type: 'success',
                //   message: '删除成功'
                // })
                this.tableData.splice(index, 1);
              }
            })
            .catch( () => {
              this.$message.error('删除失败');
              // ({
              //   type: 'error',
              //   message: '删除失败'
              // })
            })
          }).catch( () => {
            this.$message.info('已取消删除');
            // ({
            //   type: 'info',
            //   message: '已取消删除'
            // })
          })
        },
        // 编辑操作
        handleEdit (index, row) {
            this.idx = index;
            this.editTransactionForm = row;
            this.editVisible = true;
        },
        // //编辑交易信息
        // editTransaction() {
          
        // },
        // 编辑交易信息
        saveEdit() {
          this.$refs.editTransactionFormRef.validate(valid => {
            if(valid) {
              editList(this.editTransactionForm).then(res => {
                console.log(res)
                if(res.data.meta.status === 200) {
                  this.$message({
                    type: 'success',
                    message: '修改交易信息成功'
                  })
                  //数据刷新
                  this.editVisible=false
                  // 表单元素的数据重置
                  this.$refs.editTransactionFormRef.resetFields()
                  this.init()
                } else {
                  this.$message({
                    type: 'error',
                    message: '修改交易信息失败'
                  })
                }
              }).catch( () => {
                console.log('err')
              })
            } else {
              return false
            }
          })
            // this.editVisible = false;
            // this.$message.success('修改成功');
            this.$set(this.tableData, this.editTransactionform);
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        },
        // 交易信息表中的交易日期时间格式化
        dateTimeFormat(row, column) {
          let date = row[column.property]
          if (date == undefined) {
            return ''
          }
          return moment(date).format("YYYY-MM-DD HH:mm:ss")
        }
        // dateStrFormat(strTime) {
        //   if(strTime == undefined) {
        //     return ''
        //   }
        //   return moment(strTime).format("YYYY-MM-DD HH:mm:ss")
        // }      
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
