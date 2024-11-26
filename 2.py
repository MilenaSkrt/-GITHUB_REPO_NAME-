import os
import requests

# Получаем переменные окружения
username = os.getenv('USERNAME')  # Убедитесь, что вы установили переменную окружения
token = os.getenv('TOKEN')  # Убедитесь, что вы установили переменную окружения

# Заголовки для авторизации
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def list_user_repos():
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        # Форматируем вывод, чтобы показать только названия и ID
        return [(repo['name'], repo['id']) for repo in repos]
    else:
        return f"Ошибка: {response.status_code}, {response.json()}"

def create_repo(repo_name):
    url = 'https://api.github.com/user/repos'
    data = {
        'name': repo_name,
        'private': False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in [201, 202]:  # 201 Created, 202 Accepted
        return response.json()
    else:
        return f"Ошибка: {response.status_code}, {response.json()}"

def delete_repo(repo_name):
    url = f'https://api.github.com/repos/{username}/{repo_name}'
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:  # 204 No Content
        return "Репозиторий успешно удален."
    else:
        return f"Ошибка: {response.status_code}, {response.json()}"

def main():
    while True:
        print("\nВыберите действие:")
        print("1 - Список репозиториев")
        print("2 - Создать репозиторий")
        print("3 - Удалить репозиторий")
        print("4 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            print("Список репозиториев текущего пользователя:")
            repos = list_user_repos()
            if isinstance(repos, str):  # Проверка на ошибку
                print(repos)
            else:
                for repo_name, repo_id in repos:
                    print(f"ID: {repo_id}, Название: {repo_name}")

        elif choice == '2':
            repo_name = input("Введите название нового репозитория: ")
            result = create_repo(repo_name)
            print(result)

        elif choice == '3':
            repo_name = input("Введите название репозитория для удаления: ")
            result = delete_repo(repo_name)
            print(result)

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 4.")

if __name__ == "__main__":
    main()
