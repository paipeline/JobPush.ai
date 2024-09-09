# Job Search Project

## 设置说明

### 1. 安装 PostgreSQL

#### macOS:
使用 Homebrew 安装 PostgreSQL：
   - 对于 macOS，使用 Homebrew：`brew install postgresql`
   - 对于 Ubuntu：`sudo apt-get install postgresql`
   - 对于 Windows，下载并安装 [PostgreSQL](https://www.postgresql.org/download/windows/)

2. 确保 PostgreSQL 服务正在运行。
    ```
    python src/setup_database.py
    ```

3. 安装项目依赖：
   ```
   pip install -r requirements.txt
   ```

4. 运行数据库设置脚本：
   ```
   python src/setup_database.py
   ```
   按照提示输入数据库名称、用户名和密码。

5. 初始化数据库：
   ```
   python src/models.py
   ```

6. 运行主程序：
   ```
   python src/main.py
   ```

## 使用说明

[在这里添加项目的使用说明]

job_search_project/
│
├── configs/
│   └── search_terms.json
│
├── src/
│   ├── __init__.py
│   ├── job_scraper.py
│   ├── job_filter.py
│   ├── job_formatter.py
│   └── utils.py
│
├── jobs/
│   └── (generated job files will be stored here)
│
├── main.py
├── requirements.txt
└── README.md







