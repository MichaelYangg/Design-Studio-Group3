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
                <el-input v-model="query.transaction_id" placeholder="输入交易编号" clearable @clear="handleCancel()" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch()">搜索</el-button>
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
                <el-table-column prop="date_time" label="交易日期时间" :formatter="dateTimeFormat" width=100% align=center></el-table-column>
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
        <el-button type="primary" @click="addTransaction()">确 定</el-button>
      </span>
    </el-dialog>


        <!-- 修改交易信息弹出框 -->
        <el-dialog title="编辑交易信息" :visible.sync="editVisible" width="30%">
            <el-form ref="editTransactionFormRef" :model="editTransactionForm" :rules="editTransactionFormRules" label-width="80px">
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
                    <el-input v-model="editTransactionForm.date_time">
                    </el-input>
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
                <el-button type="primary" @click="saveEdit()">确 定</el-button>
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
            tableData: [],
            mainData: Object,
            dialogVisible: false,
            editVisible: false,
            deleteVisible: false,
            pageTotal: 0,
            form: {},
            idx: -1,
            id: -1,
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
          { required: true, message: "请输入交易类型", trigger: "blur"},
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
        // 从后端数据库获取交易信息
        getData() {
            fetchData(this.query).then(res => {
                this.mainData = res;
                this.tableData = res.list;
                this.pageTotal = res.pageTotal;
            });
        },
        // 触发搜索按钮
        handleSearch () {
              this.$set(this.query, 'pageIndex', 1);
              this.getData();
              console.log(this.query.transaction_id);
             // 通过查询交易编号获取对应的交易信息
             queryTransaction(this.query.transaction_id).then(res => {
                 console.log(res);
                 var list = [];
                 list.push(res); 
                 this.tableData = list;
                 this.pageTotal = 1;
             })
             .catch(err => {
               this.$message.error('该交易编号不存在');
               console.log(err);
             })   
        },
        // 清空搜索框，将交易信息表返回原状
        handleCancel () {
            this.tableData = this.mainData.list;
            this.pageTotal = this.mainData.pageTotal;
        },

         addTransaction() {
          this.$refs.addTransactionFormRef.validate(valid => {
            if(!valid) {
              return false;
            }
            addList(this.addTransactionForm).then(res => {
              this.$message.success('新增交易信息成功')
              this.dialogVisible = false;
              this.getData();
            }).catch(res => 
            {
              this.$message.error('新增交易信息失败')
            }).catch(res => 
            {
              this.$message.info('已取消新增')
              this.dialogVisible=false;
              console.log(res);
            })
          });
        },

        // // 新增操作
        //  addTransaction() {
        //  // 二次进行用户数据的验证
        //    this.$refs.addTransactionFormRef.validate(valid => {
        //      if (valid) {
        //        //发起新增交易信息请求
        //        addList(this.addTransactionForm)
        //        .then(res => {
        //          if (res.code === 200) {
        //            this.$message.error('新增交易信息失败')
        //            this.dialogVisible = false;
        //            //数据刷新
        //           this.getData();
        //            //表单元素的数据重置
        //            this.$refs.addTransactionFormRef.resetFields()
        //            this.init()
        //          } 
        //        })
        //        .catch( () => {
        //           this.$message.success('新增交易信息成功');
        //        })
        //           .catch( () => {
        //             this.$message.info('已取消新增交易信息')
        //             this.dialogVisible = false
        //           });
        //       this.$set(this.tableData, this.addTransactionForm);
        //       }
        //    })
        //  },

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
                this.$message.error('删除失败'); 
              }
              this.getData();
            })
            .catch( () => {
              this.$message.success('删除成功');
              this.tableData.splice(index, 1);  
            })
          }).catch( () => {
            this.$message.info('已取消删除');
          });
        },
        // 编辑操作
        handleEdit (index, row) {
            this.idx = index;
            this.editTransactionForm = row;
            this.editVisible = true;
        },
        // 编辑交易信息
        saveEdit() {
          this.$refs.editTransactionFormRef.validate(valid => {
            if(!valid) {
              return false;
            }
            editList(this.editTransactionForm).then(res => {
              this.$message.success('修改交易信息成功')
              this.editVisible = false;
            }).catch(res => 
            {
              this.$message.error('修改交易信息失败')
            }).catch(res => 
            {
              this.$message.info('已取消修改')
              this.editvisible=false;
            })
          });
        },

        // saveEdit() {
        //   this.$refs.editTransactionFormRef.validate(valid => {
        //     if(valid) {
        //       editList(this.editTransactionForm).then(res => {
        //         console.log(res)
        //         if(res.data.meta.status === 200) {
        //           this.$message.error('修改交易信息失败')
        //           //数据刷新
        //           this.editVisible=false
        //           // 表单元素的数据重置
        //           this.$refs.editTransactionFormRef.resetFields()
        //           this.init()
        //         }
        //         else
        //          {
        //           this.$message.info('修改交易信息成功')
        //           this.editVisible=false;
        //         }
        //       }).catch( () => {
        //         this.$message.success('已取消修改交易信息');
        //         this.editVisible=false;
        //       })
        //     } 
        //   });
        //     this.$set(this.tableData, this.editTransactionform);
        // },



        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        },
        // 交易信息表中的交易日期时间格式化
        dateTimeFormat(row, column) {
          var date = row[column.property];
          if(date == undefined){
            return '';
          }
          return moment(date).utcOffset(0).format("YYYY-MM-DD HH:mm:ss")
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
