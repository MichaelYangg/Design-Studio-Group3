from django import forms
from .models import Daily, Monthly

# Daily Form 
# Daily의 Model를 참조하고, 아래 적힌 fields의 list값들은 나중에 html에 생성될 form들이다.
class DailyFrom(forms.ModelForm):
    class Meta:
        model = Daily
        fields = ['id', 'account_type', 'net_profit', 'unit', 'date']

# Monthly Form
# Monthly의 Model를 참조하고, 아래 적힌 fields의 list값들은 나중에 html에 생성될 form들이다.
class MonthlyFrom(forms.ModelForm):
    class Meta:
        model = Monthly
        fields = ['id', 'date', 'revenue', 'cost']
