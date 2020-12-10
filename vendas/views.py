from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View
from .models import Venda, ItemDoPedido
from .forms import ItemPedidoForm, ItemDoPedidoModelForm

import logging


logger = logging.getLogger('django')


class DashboardView(View):

    def get(self, request):
        data = {}
        data['media'] = Venda.objects.media()
        data['media_desc'] = Venda.objects.media_desconto()
        data['Min'] = Venda.objects.min()
        data['Max'] = Venda.objects.max()
        data['n_ped'] = Venda.objects.num_pedidos()
        data['n_ped_nfe'] = Venda.objects.num_pedidos_nfe()

        return render(request, 'vendas/dashboard.html', data)


class NovoPedido(View):
    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        data = {}
        data['form_item'] = ItemPedidoForm()
        data['numero'] = request.POST['numero']
        data['desconto'] = float(request.POST['numero']).replace(',', '.')
        data['venda_id'] = request.POST['venda_id']

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
        else:
            venda = Venda.objects.create(
                numero=data['numero'], desconto=data['desconto'])

        itens = venda.itemdopedido_set.all()
        data['venda'] = venda
        data['itens'] = itens
        return render(request, 'vendas/novo-pedido.html', data)

class NovoItemPedido(View):
    def get(self, request, pk):
        pass
    def post(self, request, venda):
        data = {}

        item = ItemDoPedido.objects.filter(
            produto_id=request.POST['produto_id'], venda=venda)

        if item:
            data['mensagem'] = 'Item já incluido no pedido,edite o item'
            item = item[0]
        else:
            item = ItemDoPedido.objects.create(
                produto_id=request.POST['produto_id'],
                quantidade=request.POST['quantidade'],
                desconto=request.POST['desconto'],
                venda=venda
            )
        data[ 'item'] = item
        data['form_item'] = ItemPedidoForm
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(request, 'venda/novo-pedido.html', data)


class ListaVendas(View):
    def get(self, request):
        logger.debug('Acessaram a listagem de vendas')

        try:
            1/0
        except Exception as e:
            time = datetime.datetime.now()
            logger.exception(time.strftime("%Y=%m-%d %H:%M:%S") + '-' + str(
                    request.user))

        vendas = Venda.objects.all()
        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas})


class EditPedido(View):
    def get(self, request, venda):
        data = {}
        venda = Venda.objects.get(id=venda)
        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemdopedido_set.all()

        return render(request, 'venda/novo-pedido.html', data)


class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(request, 'vendas/delete-pedido-confirm.html',
                      {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')


class DeleteItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        form = ItemDoPedidoModelForm(instance=item_pedido)
        return render(request, 'vendas/delete-itempedido-confirm.html',
                      {'item-pedido': item_pedido, 'form':form})

    def post(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        item_pedido.quantidade = request.POST['quantidade']
        item_pedido.desconto = request.POST['desconto']

        item_pedido.save()
        venda_id = item_pedido.venda.id
        return redirect('edit-pedido', venda = venda_id)