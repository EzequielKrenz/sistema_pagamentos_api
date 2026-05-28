from decimal import Decimal

from app.database import SessionLocal, criar_tabelas
from app import models
from app.services.sale_service import criar_venda
from app.schemas import VendaCreate, VendaItemCreate


def popular_banco():
    criar_tabelas()
    db = SessionLocal()
    try:
        if db.query(models.Cliente).first():
            print("Banco já possui dados. Seed ignorado.")
            return

        cliente = models.Cliente(
            cnpj="12.345.678/0001-99",
            razao_social="Mercado Exemplo LTDA",
            email="compras@mercadoexemplo.com",
        )
        produto_1 = models.Produto(sku="SKU-001", descricao="Café torrado 500g")
        produto_2 = models.Produto(sku="SKU-002", descricao="Açúcar cristal 1kg")
        condicao = models.CondicaoPagamento(descricao="À vista", dias=0)
        db.add_all([cliente, produto_1, produto_2, condicao])
        db.commit()
        db.refresh(cliente)
        db.refresh(produto_1)
        db.refresh(produto_2)
        db.refresh(condicao)

        preco_1 = models.PrecoCliente(
            cliente_id=cliente.id,
            produto_id=produto_1.id,
            condicao_pagamento_id=condicao.id,
            preco=Decimal("100.00"),
        )
        preco_2 = models.PrecoCliente(
            cliente_id=cliente.id,
            produto_id=produto_2.id,
            condicao_pagamento_id=condicao.id,
            preco=Decimal("12.00"),
        )
        db.add_all([preco_1, preco_2])
        db.commit()

        venda = VendaCreate(
            cliente_id=cliente.id,
            condicao_pagamento_id=condicao.id,
            itens=[
                VendaItemCreate(produto_id=produto_1.id, quantidade=2, preco_unitario=Decimal("100.00")),
                VendaItemCreate(produto_id=produto_2.id, quantidade=5, preco_unitario=Decimal("12.00")),
            ],
        )
        criar_venda(db, venda)
        print("Seed executado com sucesso.")
        print("Dica: altere o preço do Café para 80.00 em PUT /precos-clientes/1 e rode o worker.")
    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()
