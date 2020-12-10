from django.test import TestCase
from vendas.models import Venda, ItemPedido
from produtos.models import Produto

class VendasTestCase(TestCase):
    def setUp(self):
        self.venda = Venda.objects.create(numero='123', desconto=10, status='AB')
        self.produto = Produto.objects.create(descricao='Produto 1', preco=10)


    def test_num_vendas_db(self):
        """animals that can speak are coorently identified """
        assert Venda.objects.all().count() == 1

    def test_valor_venda(self):
        """ Verifica valor total da venda """
        ItemPedido.objctes.create(
            venda=self.venda, produto=self.produto, quantidade=10, desconto=10)
        assert self.venda.valor == 90

    def test_desconto(self):
        assert self.venda.desconto == 10

    def test_intem_incluido_lista_items(self):
        item = ItemPedido.objctes.create(
            venda=self.venda, produto=self.produto, quantidade=1, desconto=0)
        self.assertIn(item, self.venda.itemdopedido_set.all())

    def test_checa_nfe_nao_emitida(self):
        self.assertFalse(self.venda.nfe_emitida)

    def test_checa_status(self):
        self.venda.status = 'PC'
        self.venda.save()
        self.assertEqual(self.venda.status, 'PC')
