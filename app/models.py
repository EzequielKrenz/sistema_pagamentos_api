from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
    razao_social = Column(String(120), nullable=False, index=True)
    email = Column(String(120), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    precos = relationship("PrecoCliente", back_populates="cliente")
    vendas = relationship("Venda", back_populates="cliente")
    notificacoes = relationship("Notificacao", back_populates="cliente")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(45), unique=True, nullable=False, index=True)
    descricao = Column(String(120), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    precos = relationship("PrecoCliente", back_populates="produto")
    itens_venda = relationship("VendaItem", back_populates="produto")
    notificacoes = relationship("Notificacao", back_populates="produto")


class CondicaoPagamento(Base):
    __tablename__ = "condicoes_pagamento"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(80), nullable=False)
    dias = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, nullable=False, default=True)

    precos = relationship("PrecoCliente", back_populates="condicao_pagamento")
    vendas = relationship("Venda", back_populates="condicao_pagamento")


class PrecoCliente(Base):
    __tablename__ = "precos_cliente"
    __table_args__ = (
        UniqueConstraint(
            "cliente_id",
            "produto_id",
            "condicao_pagamento_id",
            name="uq_preco_cliente_produto_condicao",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    condicao_pagamento_id = Column(Integer, ForeignKey("condicoes_pagamento.id"), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="precos")
    produto = relationship("Produto", back_populates="precos")
    condicao_pagamento = relationship("CondicaoPagamento", back_populates="precos")


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    condicao_pagamento_id = Column(Integer, ForeignKey("condicoes_pagamento.id"), nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=0)

    cliente = relationship("Cliente", back_populates="vendas")
    condicao_pagamento = relationship("CondicaoPagamento", back_populates="vendas")
    itens = relationship("VendaItem", back_populates="venda", cascade="all, delete-orphan")


class VendaItem(Base):
    __tablename__ = "venda_itens"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_venda")


class EventoPreco(Base):
    """Fila de mensagens do domínio.

    Cada registro representa uma mensagem de alteração de preço. O endpoint HTTP
    apenas grava a mensagem; o processamento pesado fica para o worker.
    """

    __tablename__ = "eventos_preco"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    novo_preco = Column(Numeric(10, 2), nullable=False)
    origem_preco_cliente_id = Column(Integer, ForeignKey("precos_cliente.id"), nullable=True)
    status = Column(String(20), nullable=False, default="PENDENTE", index=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    processado_em = Column(DateTime, nullable=True)
    erro = Column(Text, nullable=True)


class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    evento_preco_id = Column(Integer, ForeignKey("eventos_preco.id"), nullable=True)
    mensagem = Column(Text, nullable=False)
    preco_pago = Column(Numeric(10, 2), nullable=False)
    novo_preco = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="PENDENTE")
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    lida_em = Column(DateTime, nullable=True)

    cliente = relationship("Cliente", back_populates="notificacoes")
    produto = relationship("Produto", back_populates="notificacoes")
