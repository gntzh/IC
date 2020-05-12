
# 安装测试
建议克隆到本地后，先进行开发环境测试。

**必需**
- Python环境和Pip
- Node环境和Npm或Yarn

## 启动后端

```shell
# 安装依赖
pip install -r requirements/dev.txt
python manage.py makemigratons # 生成数据库迁移文件
python manage.py migrate # 数据库迁移
python manage.py runserver # 运行开发服务器，默认8000端口
```

创建管理用户
```shell
python manage.py createsuperuser
```
之后即可打开后台`localhost:8000/admin/`，使用刚创建的用户登录即可

## 启动前端
```shell
cd front
npm install
npm run dev # 默认8080端口
```

即可打开前端界面`localhost:8000`， 登录后即可查看各功能
