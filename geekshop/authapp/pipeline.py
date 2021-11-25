import requests
from datetime import datetime
from authapp.models import ShopUserProfile
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about', 'has_photo', 'photo_max'])
    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data_json = response.json()['response'][0]

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')
        age = datetime.now().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'bdate' in data_json:
        user.shopuserprofile.gender = data_json['about']

    if 'has_photo' in data_json:
        if data_json['has_photo'] == 1:
            user.avatar = data_json['photo_max']
