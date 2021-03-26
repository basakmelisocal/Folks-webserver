from sources.contacts_manager import message_operations, contacts_operations
from sources.data_manager import rel_db_manager


class ContactsManager:
    message = message_operations.MessageOper(rel_db_manager.RelationalDBManager())
    contacts = contacts_operations.ContactsOper(rel_db_manager.RelationalDBManager())