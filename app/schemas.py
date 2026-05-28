from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    cnpj: str = Field(..., examples=["12.345.678/0001-99"])
    razao_social: str = Field(..., examples=["Mercado Exemplo LTDA"])
    email: Optional[str] = Field(None, examples=["compras@exemplo.com"])
    ativo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    email: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    criado_em: datetime


class ProdutoBase(BaseModel):
    sku: str = Field(..., examples=["SKU-001"])
    descricao: str = Field(..., examples=["Café torrado 500g"])
    ativo: bool = True


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    sku: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None


class ProdutoResponse(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    criado_em: datetime


class CondicaoPagamentoBase(BaseModel):
    descricao: str = Field(..., examples=["À vista"])
    dias: int = Field(0, ge=0, examples=[0])
    ativo: bool = True


class CondicaoPagamentoCreate(CondicaoPagamentoBase):
    pass


class CondicaoPagamentoUpdate(BaseModel):
    descricao: Optional[str] = None
    dias: Optional[int] = Field(None, ge=0)
    ativo: Optional[bool] = None


class CondicaoPagamentoResponse(CondicaoPagamentoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PrecoClienteBase(BaseModel):
    cliente_id: int
    produto_id: int
    condicao_pagamento_id: int
    preco: Decimal = Field(..., gt=0, examples=[Decimal("89.90")])
    ativo: bool = True


class PrecoClienteCreate(PrecoClienteBase):
    pass


class PrecoClienteUpdate(BaseModel):
    cliente_id: Optional[int] = None
    produto_id: Optional[int] = None
    condicao_pagamento_id: Optional[int] = None
    preco: Optional[Decimal] = Field(None, gt=0)
    ativo: Optional[bool] = None


class PrecoClienteResponse(PrecoClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    criado_em: datetime
    atualizado_em: datetime


class VendaItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: Decimal = Field(..., gt=0)


class VendaCreate(BaseModel):
    cliente_id: int
    condicao_pagamento_id: int
    itens: List[VendaItemCreate] = Field(..., min_length=1)


class VendaItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class VendaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int
    condicao_pagamento_id: int
    data_venda: datetime
    total: Decimal
    itens: List[VendaItemResponse]


class NotificacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int
    produto_id: int
    mensagem: str
    preco_pago: Decimal
    novo_preco: Decimal
    status: str
    criado_em: datetime
    lida_em: Optional[datetime] = None


class RelatorioItemProduto(BaseModel):
    produto_id: int
    sku: str
    descricao: str
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class RelatorioVenda(BaseModel):
    venda_id: int
    data_venda: datetime
    condicao_pagamento: str
    total: Decimal
    produtos: List[RelatorioItemProduto]


class RelatorioClienteResponse(BaseModel):
    cliente_id: int
    cnpj: str
    razao_social: str
    total_geral: Decimal
    vendas: List[RelatorioVenda]
