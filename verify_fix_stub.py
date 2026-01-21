
import requests
import sys

BASE_URL = 'http://localhost:5000/api'

def register(username, password, user_type):
    url = f'{BASE_URL}/auth/register'
    data = {
        'username': username,
        'email': f'{username}@example.com',
        'password': password,
        'confirm_password': password,
        'user_type': user_type
    }
    if user_type == 'student':
        data['student_id'] = f'S_{username}'
    else:
        data['teacher_id'] = f'T_{username}'
        
    try:
        response = requests.post(url, json=data)
        # 201 created or 400 exists (which is fine for us, we just need to login)
        return response.status_code
    except Exception as e:
        print(f"Register failed: {e}")
        return 500

def login(username, password):
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def main():
    # 1. Setup Users
    teacher_name = 'teacher_v'
    student_name = 'student_v'
    pwd = 'password123'
    
    print("Registering users...")
    register(teacher_name, pwd, 'teacher')
    register(student_name, pwd, 'student')
    
    print("Logging in...")
    teacher_token = login(teacher_name, pwd)
    student_token = login(student_name, pwd)
    
    if not teacher_token or not student_token:
        print("Login failed")
        return

    teacher_headers = {'Authorization': f'Bearer {teacher_token}'}
    student_headers = {'Authorization': f'Bearer {student_token}'}

    # 2. Link Student to Teacher (Need to find IDs first)
    # Actually, the register API might not support setting guidance teacher directly?
    # Let's check profile.
    
    # We need the teacher's ID to set as guidance_teacher_id for the student.
    # But currently there is no API to set guidance teacher easily without admin or DB access.
    # However, if I create a question, I can specify teacher_id if the backend logic allows?
    # Backend logic: 
    # if user.guidance_teacher_id: question_data['teacher_id'] = user.guidance_teacher_id
    
    # Wait, without guidance_teacher_id, the question might have teacher_id=None.
    # But the teacher dashboard only shows questions where teacher_id = current_user.id.
    
    # So I must set the guidance teacher.
    # Since I cannot easily do this via API (maybe profile update?), I will rely on the fact that
    # the user "jiaqi" was fixed in the database.
    # I should try to use "jiaqi" if possible, but I don't know the password.
    
    # Let's assume I can use a raw SQL script or just check if the code runs without error.
    # But to verify "Teacher sees question", I need the link.
    
    # Let's use a python script that imports app and db to set the link.
    pass

if __name__ == '__main__':
    main()
