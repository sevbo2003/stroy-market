from modeltranslation.translator import translator, TranslationOptions
from apps.recommendation.models import Recommendation


class RecommendationTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Recommendation, RecommendationTranslationOptions)