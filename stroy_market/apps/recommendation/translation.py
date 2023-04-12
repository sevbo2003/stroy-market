from modeltranslation.translator import translator, TranslationOptions
from apps.recommendation.models import Recommendation, RecommentationForCart, RecommendationForProductDetail


class RecommendationTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(Recommendation, RecommendationTranslationOptions)


class RecommentationForCartTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(RecommentationForCart, RecommentationForCartTranslationOptions)


class RecommendationForProductDetailTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(RecommendationForProductDetail, RecommendationForProductDetailTranslationOptions)