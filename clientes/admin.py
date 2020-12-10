from django.contrib import admin
from .models import Person, Documento


class PersonAdmin(admin.ModelAdmin):
    # fields = (('first_name', 'last_name'), ('age', 'salary') , 'bio', 'photo', 'doc')
    # exclude = ('bio', )

    fieldsets = (
        ('Dados pessoais', {'fields': ('first_name', 'last_name', 'doc')}),
        ('Dados complementares', {
            'classes': ('collapse',),
            'fields': ('age', 'salary', 'photo')})
    )
    list_display = ('first_name', 'last_name', 'age', 'salary', 'bio',
                    'tem_foto', 'doc')
    list_filter = ('age', 'salary')
    search_fields = ('id', 'first_name')

    def tem_foto(self, obj):
        if obj.photo:
            return 'Sim'
        else:
            return 'Não'

    tem_foto.short_description = 'Possui foto'



# class ProdutoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'descricao', 'preco')
#     search_fields = ['id', 'descricao']


admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
# admin.site.register(Produto, ProdutoAdmin)

admin.site.site_header = 'Header'
admin.site.index_title = 'Index Title'
admin.site.site_title = 'Site Title'