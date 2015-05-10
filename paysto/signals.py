from django.dispatch import Signal

# Signal sent whenever status is changed for a Payment. This usually happens
# when a transaction is either accepted or rejected.
paysto_status_changed = Signal()
