from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_bot.utils import TelegramBotMixin
from token_auth.enums import Type
from .serializers import *
from .utils import *


class VacancyListView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            if self.request.user.type == Type.ADMINISTRATOR.value:
                return Response(VacancyShortSerializer(Vacancy.objects.all(), many=True).data,
                                status=status.HTTP_200_OK)
        except AttributeError:
            pass

        '''
            experience_type
            1 — без опыта
            2 — от 1 года
            3 — от 3 лет
            4 — от 6 лет
        '''
        experience_type = 1

        '''
            type_of_work
            6 — полный день
            10 — неполный день
            12 — сменный график
            7 — временная работа
            9 — вахтовым методом
        '''
        type_of_work = 6

        q = Q() | filter_by_skills(request.GET.get('skill'))
        q = q & filter_by_specializations(request.GET.getlist('spec'))
        q = q & filter_by_text(request.GET.get('text'))
        q = q & filter_by_experience_type(request.GET.get('experience_type'))
        q = q & filter_by_type_of_work(request.GET.get('type_of_work'))

        keywords = ''
        if request.GET.get('text'):
            keywords = request.GET.get('text')

        if request.GET.get('type_of_work'):
            type_of_work = request.GET.get('type_of_work')
            type_of_work = ConstantsSuperJob().get_employment_types(type_of_work)

        if request.GET.get('experience_type'):
            experience_type = request.GET.get('experience_type')
            experience_type = ConstantsSuperJob().get_experience_types(experience_type)

        external_vacancies = get_super_job_vacancies(keywords, type_of_work, experience_type)

        if request.GET.get('company'):
            company = Company.objects.filter(pk=request.GET.get('company'))

        else:
            company = {}

        if company:
            q = q & Q(company=company[0])

        vacancies = list(Vacancy.objects.filter(q).distinct().order_by('id'))
        if external_vacancies:
            total = vacancies + external_vacancies
        else:
            total = vacancies

        serializer = VacancySerializer(total, many=True)
        setup_vacancy_display(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            if request.GET.get('company') and self.request.user.type == Type.ADMINISTRATOR.value:
                company = Company.objects.filter(pk=request.GET.get('company'))
            elif self.request.user.type == Type.STUDENT.value:
                return Response({'error': 'student can not create a company'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif self.request.user.type == Type.EMPLOYER.value:
                company = Company.objects.filter(hr=self.request.user)
            else:
                return Response({'error': 'provide company id'}, status=status.HTTP_400_BAD_REQUEST)

            if not company:
                return Response({'error': 'user does not belong to any company'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(company=company[0], skills=request.data.get('skills'),
                            specializations=request.data.get('specializations'), courses=request.data.get('courses'))

            telegram_bot = TelegramBotMixin(request.data.get('specializations'), serializer.data.get('id'))
            telegram_bot.get_updates()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        Vacancy.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


class FavouriteVacancyListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        favourites = VacancyFavorites.objects.filter(user=self.request.user)
        serializer = FavouriteVacancySerializer(favourites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavouriteVacancySerializer(data=self.request.data)
        if serializer.is_valid():
            vacancy = Vacancy.objects.get(pk=self.request.data.get('vacancy'))
            serializer.save(user=self.request.user, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Vacancy.objects.all().delete()
        return Response(status=status.HTTP_200_OK)


class VacancyDetailView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        vacancy = self.get_object(pk)
        serializer = VacancySerializer(vacancy)

        return Response(setup_single_vacancy_display(serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        vacancy = self.get_object(pk)
        serializer = VacancySerializer(vacancy, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, vacancy_id=request.data['vacancy'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.request.user.type == Type.EMPLOYER.value:
            company = Company.objects.filter(hr=self.request.user)[0]
            vacancies = VacancyShortSerializer(instance=company.vacancies, many=True)
            for vacancy in vacancies.data:
                responses = list([])

                for request in Request.objects.filter(vacancy_id=vacancy.get('id')):
                    response = dict({})
                    response['vacancy_name'] = vacancy.get('name')
                    response['response_id'] = request.id
                    response['student_id'] = request.user.id
                    response['student_name'] = request.user.first_name + ' ' + request.user.last_name
                    responses.append(response)

                vacancy['responses'] = responses

            responses = vacancies.data

        elif self.request.user.type == Type.STUDENT.value:
            responses = list([])

            for request in Request.objects.filter(user=self.request.user):
                vacancy = Vacancy.objects.get(id=request.vacancy.id)
                company = Company.objects.get(id=vacancy.company.id)

                response = dict({})
                response['vacancy_id'] = vacancy.id
                response['vacancy_name'] = vacancy.name
                response['vacancy_description'] = vacancy.description
                response['vacancy_short_description'] = vacancy.short_description
                response['response_id'] = request.id
                response['response_decision'] = request.decision
                response['response_seen'] = request.seen
                response['company_id'] = company.id
                response['company_logo'] = company.logo
                response['company_name'] = company.name
                responses.append(response)
        else:
            return Response(RequestSerializer(Request.objects.all(), many=True).data, status=status.HTTP_200_OK)

        return Response(responses, status=status.HTTP_200_OK)


class RespondRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @staticmethod
    def get_object(pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        request = self.get_object(pk)
        serializer = RequestSerializer(request, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        request = self.get_object(pk)
        serializer = RequestSerializer(request, data={'seen': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
