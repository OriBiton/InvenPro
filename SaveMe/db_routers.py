class AppDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'inventory':
            return 'inventory'
        elif model._meta.app_label == 'orders':
            return 'orders'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'inventory':
            return 'inventory'
        elif model._meta.app_label == 'orders':
            return 'orders'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True  # אפשר קישורים בין דאטהבייסים

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'inventory':
            return db == 'inventory'
        elif app_label == 'orders':
            return db == 'orders'
        return db == 'default'
