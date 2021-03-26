from sources.trip_manager import interests_operations, trip_operations
from sources.data_manager import rel_db_manager


class TripManager:
    interests_operations = interests_operations.InterestsOperations(rel_db_manager.RelationalDBManager())
    trip_oper = trip_operations.TripOperations(rel_db_manager.RelationalDBManager())
