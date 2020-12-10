from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.views import View
from clientes.models import Person
from produtos.models import Produto
from django.db.models import Sum, F, FloatField, Max

from .managers import VendaManager


class Venda(models.Model):
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    nfe_emitida = models.BooleanField(default=False)

    objects = VendaManager()

    def calcula_total(self):
        tot = self.itemdopedido_set.all().aggregate(
            tot_ped=Sum((F('quantidade') * F('produto_preco')) - F('desconto'),
                        output_field=FloatField)
        )['tot_ped'] or 0

        tot = tot - float(self.impostos) - float(self.desconto)
        self.valor = tot
        self.save()


    # criando permissão com tupla de tuplas com nome e descrição
    class Meta:
        permissions = (
            ('setar_nfe', 'Usuario pode alterar o parametro NF-e'),
            ('ver_dashboard', 'Pode visualizar o Dashboard'),
            ('permissao3', 'Permissao 3'),
        )

    # def get_total(self):
    #     total = 0
    #     for produto in self.produtos.all():
    #         total += produto.preco
    #     return (total - self.desconto) - self.impostos

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.venda.numero + ' - ' + self.produto.descricao


@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total(sender, instance, **kwargs):
    instance.venda.calcula_total()

@receiver(post_save, sender=Venda)
def update_vendas_total2(sender, instance, **kwargs):
    instance.calcula_total()

# @receiver(m2m_changed, sender=Venda.produtos.through)
# def update_vendas_total(sender, instance, **kwargs):
#     total = instance.get_total()
#     Venda.objects.filter(id=instance.id).update(total = total)


