from django.db import models
from django_fsm import FSMField, transition

# Create your models here.
STATES = ('Open', 'In Progress', 'Resolved', 'Under Review', 'Re Opened', 'Closed')
STATES = list(zip(STATES, STATES))


class TodoTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = FSMField(default='Open', choices=STATES, protected=True)

    def __str__(self):
        return self.title

    @transition(field=state, source=['Open', 'Re Opened', 'Resolved'], target='In Progress')
    def trans_start(self):
        pass

    @transition(field=state, source=['In Progress', 'Re Opened'], target='Resolved')
    def trans_resolve(self):
        pass

    @transition(field=state, source='Resolved', target='Under Review')
    def trans_review(self):
        pass

    @transition(field=state, source=['Closed', 'Under Review'], target='Re Opened')
    def trans_reopen(self):
        pass

    @transition(field=state, source=['Open', 'In Progress', 'Re Opened', 'Resolved', 'Under Review'], target='Closed')
    def trans_close(self):
        pass
