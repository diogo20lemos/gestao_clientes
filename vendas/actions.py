from django.http import HttpResponseNotFound


def nfe_emitida(modeladmin, request, queryset):
    if request.user.has_perm('clientes.setar_nfe'):
        queryset.update(nfe_emitida=True)
    else:
        return HttpResponseNotFound('<h1>Sem permissao</h1>')

nfe_emitida.short_description = "NF-e Emitida"


def nfe_nao_emitida(modeladmin, request, queryset):
    queryset.update(nfe_emitida=False)


nfe_nao_emitida.short_description = "NF-e Não Emitida"