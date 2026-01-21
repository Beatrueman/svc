<template>
  <div class="files-container">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <h1>毕业设计指导网站</h1>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              {{ authStore.user?.username }}
              <el-icon class="icon"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToProfile">个人信息</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-container>
        <el-aside width="200px" class="aside">
          <el-menu router :default-active="activeMenu">
            <el-menu-item index="/dashboard" route="/dashboard">
              <template #title>首页</template>
            </el-menu-item>
            <el-menu-item index="/files" route="/files">
              <template #title>文件管理</template>
            </el-menu-item>
            <el-menu-item index="/questions" route="/questions">
              <template #title>问题中心</template>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <el-main>
        <!-- 文件上传卡片 -->
        <el-card class="upload-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>上传文件</span>
            </div>
          </template>

          <el-row :gutter="20">
            <el-col :xs="24" :sm="24" :md="18">
              <el-upload
                ref="uploadRef"
                class="upload-area"
                drag
                action="#"
                :auto-upload="false"
                :on-change="handleFileSelect"
                multiple
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  拖拽文件到此或 <em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    支持 pdf、doc、docx、xls、xlsx、ppt、pptx、txt、zip、rar、jpg、jpeg、png、gif 等文件
                  </div>
                  <div class="el-upload__tip">
                    单个文件最大 100MB
                  </div>
                </template>
              </el-upload>
            </el-col>

            <el-col :xs="24" :sm="24" :md="6">
              <div class="upload-options">
                <el-form :model="uploadForm" label-width="80px">
                  <el-form-item label="文件描述">
                    <el-input
                      v-model="uploadForm.description"
                      type="textarea"
                      placeholder="请输入文件描述（可选）"
                      :rows="3"
                    />
                  </el-form-item>

                  <el-form-item label="公开文件">
                    <el-switch v-model="uploadForm.isPublic" />
                  </el-form-item>

                  <el-button
                    type="primary"
                    @click="handleUpload"
                    :loading="uploading"
                    style="width: 100%"
                  >
                    上传
                  </el-button>
                </el-form>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 文件列表卡片 -->
        <el-card class="files-card" shadow="hover" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>文件列表</span>
              <el-input-group style="width: 300px">
                <el-input
                  v-model="searchKeyword"
                  placeholder="搜索文件名"
                  clearable
                  @keyup.enter="handleSearch"
                />
                <el-button @click="handleSearch" type="primary">搜索</el-button>
              </el-input-group>
            </div>
          </template>

          <el-table
            :data="fileList"
            style="width: 100%"
            stripe
            v-loading="loading"
          >
            <el-table-column prop="filename" label="文件名" min-width="200">
              <template #default="{ row }">
                <div class="filename-cell">
                  <el-icon v-if="isImageFile(row.file_type)" style="margin-right: 8px">
                    <picture />
                  </el-icon>
                  <el-icon v-else style="margin-right: 8px">
                    <document />
                  </el-icon>
                  {{ row.filename }}
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="owner" label="上传者" width="120" />

            <el-table-column label="大小" width="100">
              <template #default="{ row }">
                {{ formatFileSize(row.file_size) }}
              </template>
            </el-table-column>

            <el-table-column label="上传时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>

            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_public ? 'success' : 'info'">
                  {{ row.is_public ? '公开' : '私有' }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="handleDownload(row)"
                >
                  下载
                </el-button>
                <el-button
                  v-if="canDeleteFile(row)"
                  link
                  type="danger"
                  size="small"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[5, 10, 20, 50]"
            :total="total"
            layout="total, sizes, prev, pager, next"
            style="margin-top: 20px; text-align: right"
            @change="loadFiles"
          />
        </el-card>
      </el-main>
    </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { filesAPI } from '@/api/files'
import { authAPI } from '@/api/auth'
import { UploadFilled, Picture, Document, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const activeMenu = ref('/files')
const uploadRef = ref()

// 上传相关
const uploading = ref(false)
const selectedFile = ref(null)
const uploadForm = ref({
  description: '',
  isPublic: false
})

// 文件列表相关
const loading = ref(false)
const fileList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  try {
    await authAPI.logout()
  } catch (error) {
    console.error('登出请求失败:', error)
  } finally {
    authStore.clearAuth()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}

const handleFileSelect = (file) => {
  selectedFile.value = file.raw || file
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  uploading.value = true
  try {
    const response = await filesAPI.uploadFile(
      selectedFile.value,
      uploadForm.value.description,
      uploadForm.value.isPublic
    )

    if (response.data.code === 201) {
      ElMessage.success('文件上传成功')
      uploadRef.value?.clearFiles()
      selectedFile.value = null
      uploadForm.value = { description: '', isPublic: false }
      await loadFiles()
    } else {
      ElMessage.error(response.data.message || '上传失败')
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessage.error(error.response?.data?.message || error.message || '上传失败，请检查网络连接')
  } finally {
    uploading.value = false
  }
}

const loadFiles = async () => {
  loading.value = true
  try {
    const response = await filesAPI.getFiles(currentPage.value, pageSize.value)

    if (response.data.code === 200) {
      fileList.value = response.data.data.files
      total.value = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '加载失败')
    }
  } catch (error) {
    ElMessage.error('加载文件列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = async () => {
  currentPage.value = 1
  loading.value = true
  try {
    const response = await filesAPI.searchFiles(
      searchKeyword.value,
      '',
      currentPage.value,
      pageSize.value
    )

    if (response.data.code === 200) {
      fileList.value = response.data.data.files
      total.value = response.data.data.total
    } else {
      ElMessage.error(response.data.message || '搜索失败')
    }
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

const handleDownload = async (file) => {
  try {
    const response = await filesAPI.downloadFile(file.id)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.filename)
    document.body.appendChild(link)
    link.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(link)
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const handleDelete = async (file) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件 "${file.filename}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await filesAPI.deleteFile(file.id)

    if (response.data.code === 200) {
      ElMessage.success('文件删除成功')
      await loadFiles()
    } else {
      ElMessage.error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const canDeleteFile = (file) => {
  return file.user_id === authStore.user?.id || authStore.user?.user_type === 'admin'
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const isImageFile = (fileType) => {
  return ['jpg', 'jpeg', 'png', 'gif'].includes(fileType)
}

// 初始化加载
loadFiles()
</script>

<style scoped lang="scss">
.files-container {
  min-height: 100vh;
  background-color: #fafafa;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #409EFF;
    color: white;
    padding: 0 20px;

    h1 {
      margin: 0;
      font-size: 20px;
    }

    .user-info {
      cursor: pointer;
      display: flex;
      align-items: center;

      .icon {
        margin-left: 8px;
      }
    }
  }

  .aside {
    background-color: #f5f5f5;
    border-right: 1px solid #e0e0e0;
  }

  .el-main {
    padding: 20px;
  }

  .upload-card,
  .files-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      color: #333;
    }
  }

  .upload-card {
    .upload-area :deep(.el-upload-dragger) {
      width: 100%;
      height: 200px;
    }

    .upload-options {
      padding: 10px;
    }
  }

  .files-card {
    .card-header {
      .el-input-group {
        margin-left: auto;
      }
    }

    .filename-cell {
      display: flex;
      align-items: center;
      word-break: break-all;
    }
  }
}
</style>
