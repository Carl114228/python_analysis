# python_analysis
python数据可视化

## 本地运行

使用 Python 3.13，在项目根目录执行：

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

页面使用 `DjangoProject/web/TwoColorBall.csv` 中的数据。项目自带的 Django 密钥仅用于本地开发；部署时请设置 `DJANGO_SECRET_KEY` 环境变量并检查 `DEBUG` 等配置。
