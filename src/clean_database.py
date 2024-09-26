from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Job  # 假设您的模型定义在 database.py 文件中

# 创建数据库连接
engine = create_engine('sqlite:///jobpush.db')
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 删除所有 Job 记录
    session.query(Job).delete()
    
    # 如果有其他表格,也可以在这里添加删除操作
    # 例如: session.query(OtherTable).delete()
    
    # 提交更改
    session.commit()
    print("数据库已清空")
except Exception as e:
    print(f"清空数据库时出错: {e}")
    session.rollback()
finally:
    session.close()