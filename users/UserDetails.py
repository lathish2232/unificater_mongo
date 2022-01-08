from service.util import unify_logger


class UserDetails:
    LOGGED_IN_USER_NAME = None
    LOGGED_IN_USER_ID = -1
    REQUEST_API = None
    MONGO_CONNECTION = None
    FLOW_MONGO_CONNECTION = None
    CORRELATION_ID = None
    FLOW = None

    def clear_user_details(self):
        self.LOGGED_IN_USER_NAME = None
        self.LOGGED_IN_USER_ID = -1
        self.REQUEST_API = None
        self.MONGO_CONNECTION = None
        self.FLOW_MONGO_CONNECTION = None
        self.CORRELATION_ID = None
        self.FLOW = None
        unify_logger.unify_log_list = []
