from rest_framework import serializers
from allauth.account.adapter import get_adapter
from backendPeti import settings
from .models import User, UserRoles
from allauth.account.utils import setup_user_email

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    name = serializers.CharField(required=False, write_only=True)
    sisa_cuti = serializers.CharField(required=False, write_only=True)
    roles = serializers.CharField(required=False, write_only=True)

    password1 = serializers.CharField(required=False, write_only=True)
    password2 = serializers.CharField(required=False, write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match.")
            )
        return data
    
    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name' : self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
            'name' : self.validated_data.get('name', ''),
            'sisa_cuti' : self.validated_data.get('sisa_cuti', ''),
            'roles' : self.validated_data.get('roles', ''),
            'address' : self.validated_data.get('address', ''),
            'user_type' : self.validated_data.get('user_type', ''),
            'password1' : self.validated_data.get('password1', ''),
            'email' : self.validated_data.get('email', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user 

        user.save()
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User Model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'name',
                    'sisa_cuti', 'roles')
        # read_only_fields = ('email', )

class UserRolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__' 
        
        