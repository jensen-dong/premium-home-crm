from django import template

register = template.Library()

@register.filter
def stage_progress(stage):
    stages = ['contact', 'consultation', 'design', 'proposal', 'order']
    try:
        index = stages.index(stage)
        return (index + 1) / len(stages) * 100
    except ValueError:
        return 0