
<style scoped>
.questions-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.aside {
  background-color: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  height: 100vh;
}

.main {
  padding: 20px;
  background-color: #fafafa;
  overflow-y: auto;
}

.page-content {
  max-width: 800px;
  margin: 0 auto;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.banner {
  background-color: #667eea;
  color: white;
  padding: 20px;
  text-align: center;
  margin-bottom: 16px;
  height: 80px; /* 统一Banner的高度 */
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.banner-content h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: bold;
}

.banner-content p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #fff;
}

h2 {
  margin-top: 0;
  font-size: 18px;
}

textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  box-sizing: border-box;
  resize: vertical;
}

input[type='text'] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  margin-bottom: 12px;
}

.actions {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

button {
  padding: 6px 12px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #66b1ff;
}

.tip {
  font-size: 13px;
  color: #67c23a;
}

.question-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.question-list li {
  border-bottom: 1px solid #eee;
  padding: 8px 0;
}

.question-list li:last-child {
  border-bottom: none;
}

.q-title {
  font-size: 14px;
}

.q-time {
  font-size: 12px;
  color: #888;
  margin-top: 4px;
}

.empty {
  text-align: center;
  color: #aaa;
  padding: 12px 0;
}
</style>