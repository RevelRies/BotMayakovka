import json

from datetime import datetime

from .serializers import PieceSerializerName, PieceSerializerDesc
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Piece, User, Action

def get_dict_from_json(val, request):
    '''Функция преобразования json объекта в dict'''

    json_data = request.body.decode('utf-8')  # преобразование байтовой строки в строку
    data = json.loads(json_data)  # преобразование JSON-строки в словарь Python
    return data.get(val)  # получение значения по ключу 'val'


class PieceView(APIView):
    def get(self, request: Request):
        """
                Обрабатывает GET-запрос к API-эндпоинту.

                Поддерживаемые GET-параметры:
                - sort_by: параметр сортировки (name, date, genre);
                - genre: жанр произведения (используется только при sort_by=genre);

                :param request: объект Request, содержащий информацию о запросе;
                :return: объект Response с сериализованными данными.
        """

        sort_by = get_dict_from_json(val='sort_by', request=request)

        if sort_by:
            if sort_by == 'name':
                res = Piece.objects.all().order_by('name').values('name', 'id')
            if sort_by == 'date':
                res = Piece.objects.all().order_by('date').values('name', 'id')
            if sort_by == 'genre':
                genre = get_dict_from_json(val='genre', request=request)
                res = Piece.objects.filter(genre=genre).values('name', 'id')
            if sort_by == 'non_popular':
                res = Piece.objects.filter(little_known=True).values('name', 'id')

            return Response(PieceSerializerName(res, many=True).data)



class PieceInfoView(APIView):
    def get(self, request: Request):
        '''
        В методе get происходит извлечение id_piece из тела запроса в формате JSON
        с помощью функции get_dict_from_json и последующий запрос к базе данных Django
        для извлечения информации о пьесе по указанному id_piece.

        Полученные данные сериализуются с помощью класса PieceSerializerDesc и возвращаются
        в виде ответа на GET-запрос в формате JSON с помощью функции Response из Django REST Framework.
        '''
        id_piece = get_dict_from_json(val='id_piece', request=request)

        res = Piece.objects.filter(id=id_piece).values('name',
                                                       'id',
                                                       'description_piece',
                                                       'description_piece_detailed',
                                                       'description_play',
                                                       'link_play',
                                                       'link_video')

        return Response(PieceSerializerDesc(res, many=True).data)



class PieceImgView(APIView):
    def get(self, request: Request):
        '''
        Внутри функции из запроса request извлекается параметр id_piece с помощью функции
        get_dict_from_json. Затем, с использованием метода get модели Piece,
        выбирается объект Piece с определенным id_piece. Затем получается путь к изображению
        объекта Piece с помощью res.image.path.

        В результате функция возвращает Response с путем к изображению в виде строки.
        '''
        id_piece = get_dict_from_json(val='id_piece', request=request)
        res = Piece.objects.get(id=id_piece)
        image_path = res.image.path
        return Response(image_path)


class UserAddView(APIView):
    def get(self, request: Request):
        '''
        проверяет наличие пользователя в БД
        :param request:
        :return:
        '''

        tg_id = get_dict_from_json(val='tg_id', request=request)
        try:
            User.objects.get(tg_id=tg_id)
            return Response(True)
        except:
            return Response(False)

    def post(self, request: Request):
        '''
        функция добавляет нового пользователя в БД
        :param request:
        :return:
        '''

        tg_id = get_dict_from_json(val='tg_id', request=request)
        full_name = get_dict_from_json(val='full_name', request=request)
        username = get_dict_from_json(val='username', request=request)
        reg_time = last_time = datetime.now()

        User.objects.create(tg_id=tg_id,
                            full_name=full_name,
                            username=username,
                            reg_time=reg_time,
                            last_time=last_time)

        return Response('Пользователь создан')
    def put(self, request: Request):
        '''
        функция изменяет пользователю последнее время входа
        :param request:
        :return:
        '''

        tg_id = get_dict_from_json(val='tg_id', request=request)
        last_time = datetime.now()

        User.objects.filter(tg_id=tg_id).update(last_time=last_time)

        return Response('Время обновлено')


class ActionAddView(APIView):
    def post(self, request: Request):
        '''
        функция добавляет действие в БД
        :param request:
        :return:
        '''
        msg_id = get_dict_from_json(val='msg_id', request=request)
        msg_name = get_dict_from_json(val='msg_name', request=request)
        click_time = datetime.now()
        tg_id = get_dict_from_json(val='tg_id', request=request)
        user = User.objects.get(tg_id=tg_id)

        Action.objects.create(msg_id=msg_id,
                              msg_name=msg_name,
                              click_time=click_time,
                              user=user)

        return Response('Действие создано')


class StatisticsView(APIView):
    def get(self, request: Request):
        '''
        вывод статистики в соответствии с заданными параметрами
        :param request:
        :return:
        '''
        users = get_dict_from_json(val='users', request=request)
        actions = get_dict_from_json(val='actions', request=request)
        comands = get_dict_from_json(val='comands', request=request)

        # вывод статистики пользователей
        if actions == comands == "None":

            # за все время
            all_users = User.objects.count()

            # за день
            today = datetime.now().day
            day_users = User

            # за неделю



















