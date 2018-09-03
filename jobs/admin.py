from django.contrib import admin
import models
# Register your models here.

admin.site.register(models.Script)

admin.site.register(models.Template)
admin.site.register(models.TemplateStep)
admin.site.register(models.TemplateStepScript)
admin.site.register(models.TemplateStepText)