# Use defined Database
def run_initial_migration(sender, **kwargs):
    print("Skipping initial migration as tables already exist.")

from django.db.backends.signals import connection_created
connection_created.connect(run_initial_migration)
