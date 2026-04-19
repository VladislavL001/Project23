from django import forms
from django.core.exceptions import ValidationError

from .models import  Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    ]

    def clean(self):
        cleaned_data  = super().clean()

        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Запрещено использовать слово "{word}" в названии')
            if word in description:
                raise ValidationError(f'Запрещено использовать слово "{word}" в описании')


        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        return price

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите название'  # Текст подсказки внутри поля
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control', # Добавление CSS-класса для стилизации поля
            'rows': 4,
            'placeholder': 'Введите описание'  # Текст подсказки внутри поля
        })

        self.fields['image'].widget.attrs.update({
            'placeholder': 'Добавьте картинку'  # Текст подсказки внутри поля
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Выберите категорию'  # Текст подсказки внутри поля
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите цену'  # Текст подсказки внутри поля
        })

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image.size > 5 * 1024 * 1024:
            raise ValidationError('Размер изображения не должен превышать 5 МБ')

        valid_formats = ['image/jpeg', 'image/png']
        if image.content_type not in valid_formats:
            raise ValidationError('Разрешены только JPEG и PNG')

        return image