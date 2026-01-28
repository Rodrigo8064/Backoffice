import json
from django.conf import settings
from django.db.models import Q
from openai import OpenAI
from client import prompts
from product_type.models import ProductType
from category.models import Category


class IAgent:

    def __init__(self):
        self.__client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL,
        )

    def __get_data(self, message):
        text_message = str(message)
        keywords = text_message.split()
        query = Q()
        for word in keywords:
            if len(word) > 3:
                query |= Q(name__icontains=word)

        products = list(ProductType.objects.filter(query).values_list('name', flat=True)[:50])
        categories = list(Category.objects.filter(query).values_list('name', flat=True)[:50])
        
        return json.dumps({
            'tipos_existentes': products,
            'categorias_existentes': categories,
        }, ensure_ascii=False)

    def invoke(self, message):
        context_data = self.__get_data(message)

        user_content = prompts.USER_PROMPT.replace('{{data}}', context_data)
        user_content = user_content.replace('{message}', message)

        response = self.__client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            response_format={ "type": "json_object" },
            messages=[
                {'role': 'system', 'content': prompts.SYSTEM_PROMPT},
                {'role': 'user', 'content': user_content},
            ],
            temperature=0.2,
        )
        return json.loads(response.choices[0].message.content)
