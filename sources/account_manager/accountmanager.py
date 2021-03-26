from sources.account_manager import reg_oper, user_operations
from sources.data_manager import rel_db_manager


class AccountManager:
    registration_operations = reg_oper.RegistrationOperations(rel_db_manager.RelationalDBManager())
    user_operations = user_operations.UserOperations(rel_db_manager.RelationalDBManager())
