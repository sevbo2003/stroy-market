from modeltranslation.translator import translator, TranslationOptions
from apps.recommendation.models import Recommendation, RecommentationForCart


class RecommendationTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(Recommendation, RecommendationTranslationOptions)


class RecommentationForCartTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(RecommentationForCart, RecommentationForCartTranslationOptions)
