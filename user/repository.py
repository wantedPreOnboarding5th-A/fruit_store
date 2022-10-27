from rest_framework.response import Response
from user.serializers import UserSignupSerializer


class UserRepo:
    def create(self):
        serializer = UserSignupSerializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)