import json
import copy
from .models import HeroSettings
from .translations import TRANSLATIONS

def translation_processor(request):
    # Check session for the chosen language, default to 'uz'
    lang = request.session.get('django_language', 'uz')
    if lang not in TRANSLATIONS:
        lang = 'uz'
    
    # Retrieve settings from DB, handling fallback if table doesn't exist yet or is empty
    try:
        hero_settings = HeroSettings.objects.first()
    except Exception:
        hero_settings = None

    # Deep copy TRANSLATIONS to prevent persistent in-memory pollution across requests
    translations_copy = copy.deepcopy(TRANSLATIONS)

    if hero_settings:
        translations_copy['uz']['hero_title'] = hero_settings.title_uz
        translations_copy['uz']['hero_subtitle'] = hero_settings.subtitle_uz
        translations_copy['ru']['hero_title'] = hero_settings.title_ru
        translations_copy['ru']['hero_subtitle'] = hero_settings.subtitle_ru
    else:
        # Fallback to the new requested default values
        translations_copy['uz']['hero_title'] = "Murakkab huquqiy muammolarga professional yechim"
        translations_copy['uz']['hero_subtitle'] = "<strong>Solixov Shuxriddin Muxiddin o`g`li</strong> - 2013-yildan buyon huquq sohasida faoliyat yuritib kelayotgan, Jinoiy va ma'muriy ishlar bo'yicha litsenziyaga ega <span class=\"license-text\">(LITSENZIYA Adliya vazirligining Toshkent viloyati xududiy boshqarmasi №1636252)</span> tajribali advokat. Tergov va sud jarayonlarida kafolatlangan himoya hamda murakkab nizolarga professional yechimlar."
        translations_copy['ru']['hero_title'] = "Профессиональное решение сложных правовых вопросов"
        translations_copy['ru']['hero_subtitle'] = "<strong>Солихов Шухриддин Мухиддин угли</strong> - опытный адвокат, осуществляющий деятельность в сфере права с 2013 года, имеющий лицензию по уголовным и административным делам <span class=\"license-text\">(ЛИЦЕНЗИЯ Ташкентского областного территориального управления Министерства юстиции №1636252)</span>. Гарантированная защита в ходе следствия и судебных процессов, а также профессиональное решение сложных споров."

    return {
        'lang': translations_copy[lang],
        'current_lang': lang,
        'translations_json': json.dumps(translations_copy),
    }

