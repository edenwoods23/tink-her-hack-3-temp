 from django import forms
from .models import SkinProfile

class SkinProfileForm(forms.ModelForm):
    class Meta:
        model = SkinProfile
        fields = ['summer_skin_type', 'winter_skin_type', 'spring_skin_type', 
                 'concerns', 'goals', 'allergies']
        widgets = {
            'concerns': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'summer_skin_type': forms.Select(attrs={'class': 'form-select'}),
            'winter_skin_type': forms.Select(attrs={'class': 'form-select'}),
            'spring_skin_type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'summer_skin_type': 'Summer Skin Type',
            'winter_skin_type': 'Winter Skin Type',
            'spring_skin_type': 'Spring Skin Type',
            'concerns': 'Skin Concerns',
            'goals': 'Skincare Goals',
            'allergies': 'Known Allergies'
        }
        help_texts = {
            'concerns': 'Describe any skin concerns you have (e.g., acne, dryness, aging)',
            'goals': 'What are your skincare goals?',
            'allergies': 'List any known allergies to skincare ingredients'
        }
