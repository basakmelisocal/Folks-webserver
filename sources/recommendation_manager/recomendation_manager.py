from recommendation_operations import RecomendationOper
from sources.data_manager.rel_db_manager import RelationalDBManager

class RecomendationManager:
    recommendation_operations = RecomendationOper(RelationalDBManager())

