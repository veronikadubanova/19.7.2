from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, invalid_pet_id, invalid_name
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Пуша', animal_type='беспородный', age='3', pet_photo='image/kot.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Муся", "Сибирская", "2", "images/kot.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Пуша', animal_type='беспородный', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_successful_add_new_pet_no_photo(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.add_new_pet_no_photo(auth_key['key'], name='Дилли', animal_type='собака', age=7)
    assert status == 200
    assert result['name'] == 'Дилли'

def test_successful_set_pet_photo(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    if len1 > 0:
        last_pet_id = pets_list[0]['id']
        status, result = pf.set_pet_photo(auth_key['key'], pet_id=last_pet_id, pet_photo='image/kot.jpg')
        edited_pet_id = result['id']
        assert status == 200
        assert edited_pet_id == last_pet_id
    else:
        raise Exception('There is no pets in list to be updated')

#10 тестов для задания

def test_negative_get_api_key_for_valid_user(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    if type(result) is str:
        print('Неправильно введен пароль')
    assert status == 403

def test_negative_get_api_key_for_valid_user(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    if type(result) is str:
        print('Неправильно введен адрес электронной почты')
    assert status == 403

def test_negative_get_api_key_for_valid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    if type(result) is str:
        print('Неправильно введен адрес электронной почты и пароль')
    assert status == 403

def test_negative_get_all_pets_invalid_filter(filter='invalid_filter', email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key['key'], filter)
    if type(result) is str:
        print('Невалидный параметр')
    assert status == 500

def test_negative_add_new_pet_with_invalid_photo(email=valid_email, password=valid_password, name='Котя', animal_type='беспородный', age='3',
                                                 pet_photo='image/bad.pdf'):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)
    if type(result) is str:
        print('Неверный формат фото')
        assert status == 500
        assert len1 == len2

def test_negative_delete_pet_invalid_id(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    status, result = pf.delete_pet(auth_key['key'],
                             pet_id='invalid_pet_id'
                           )
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len2 = len(pets_list)
    if type(result) is str:
        print('Нет животного с таким id')
    assert status == 403
    assert len1 == len2

def test_negative_delete_others_pet(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='')
    all_pets_list = answer['pets']
    last_pet_id = all_pets_list[0]['id']
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    my_last_pet_id = my_pets_list[0]['id']

    if last_pet_id != my_last_pet_id:
        len1 = len(all_pets_list)
        status = pf.delete_pet(auth_key['key'],
                                 pet_id='last_pet_id'
                                )
        _, answer = pf.get_list_of_pets(auth_key['key'], filter='')
        all_pets_list = answer['pets']
        len2 = len(all_pets_list)
        assert status == 404
        assert len1 == len2
    else:
        print('Вы не можете удалить чужого питомца')

#В следующем тесте проверим, что будет, если при создании питомца указать невалидный возраст
def test_negative_add_new_pet_invalid_age(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.add_new_pet_no_photo(auth_key['key'], 'name', 'animal_type', 'age')
    my_pets_list = answer
    len1 = len(my_pets_list)
    status, result = pf.add_new_pet_no_photo(auth_key['key'], name='Кити', animal_type='кошка', age='500')
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer
    len2 = len(my_pets_list)
    if type(result) is str:
        print('Неверный формат в поле Возраст')
        assert status == 500
        assert len1 == len2

# В следующем тесте проверим, что будет, если добавить питомца с именем, превышающим разрешенное количество символов
def test_negative_add_new_pet_invalid_name(email=valid_email, password=valid_password):
    _, auth_key = pf.get_api_key(email, password)
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)
    status, result = pf.add_new_pet_no_photo(auth_key['key'],
                                                    name=invalid_name,
                                                    animal_type="кот",
                                                    age=8
                                                    )
    _, answer = pf.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        print('Превышено допустимое количество символов')
    assert status == 500
    assert len1 == len2




