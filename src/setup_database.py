import os
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Error: {error.decode('utf-8')}")
        return False
    return True

def setup_database():
    db_name = input("Enter the database name (default: job_search_db): ") or "job_search_db"
    db_user = input("Enter the database user (default: postgres): ") or "postgres"
    db_password = input("Enter the database password: ")

    # 创建数据库和用户
    commands = [
        f"createdb {db_name}",
        f"psql postgres -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\"",
        f"psql postgres -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\""
    ]

    for command in commands:
        print(f"Running: {command}")
        if not run_command(command):
            print("Setup failed. Please check your PostgreSQL installation and try again.")
            return

    # 更新 models.py 中的 DATABASE_URL
    models_path = os.path.join(os.path.dirname(__file__), 'models.py')
    with open(models_path, 'r') as file:
        content = file.read()

    new_url = f"postgresql://{db_user}:{db_password}@localhost/{db_name}"
    updated_content = content.replace(
        "DATABASE_URL = \"postgresql://username:password@localhost/job_search_db\"",
        f"DATABASE_URL = \"{new_url}\""
    )

    with open(models_path, 'w') as file:
        file.write(updated_content)

    print("Database setup complete. models.py has been updated with the new database URL.")

if __name__ == "__main__":
    setup_database()