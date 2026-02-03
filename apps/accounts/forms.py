
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # This is correct, keep the dot
from django import forms
from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('department', 'avatar',)



class ProfileUpdateForm(forms.ModelForm):
    # This must be 'def', not 'class'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind styling to all fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition'
            })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'avatar']



class AdminWorkerEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'department', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-5 py-3 rounded-xl border border-gray-100 bg-gray-50 font-bold'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-5 py-3 rounded-xl border border-gray-100 bg-gray-50 font-bold'}),
            'department': forms.TextInput(attrs={'class': 'w-full px-5 py-3 rounded-xl border border-gray-100 bg-gray-50 font-bold'}),
        }