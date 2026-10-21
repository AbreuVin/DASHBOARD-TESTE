# Controle de Demandas · CGPRES

Painel em Power BI (projeto `controle_demandas_cgpres.pbip`) que atende os pontos de melhoria
enviados pela Chefia de Gabinete da Presidência em 19/10/2026.

Os dados atuais são **fictícios** e são gerados no Power Query, com datas relativas à data de hoje
para o painel sempre parecer atual. Para ligar o painel à lista do SharePoint, veja
[Trocar os dados fictícios pela lista real](#trocar-os-dados-fictícios-pela-lista-real).

## Páginas

| Página | Conteúdo |
| --- | --- |
| Visão geral | Indicadores (recebidas, finalizadas, em tramitação, % no prazo externo, em andamento vencidas), cumprimento do prazo nas quatro situações, recebidas por mês, dentro e fora do prazo por objeto, quantidade por tipo |
| Metas | Finalizadas no período contra a meta, atingimento, % no prazo externo e interno, gráficos mensais e tabela mês a mês |
| Diligências | Lista detalhada com prazo interno e prazo externo lado a lado, situação colorida e dias de atraso |

As segmentações de período, tipo de diligência, prioridade e situação do prazo ficam sincronizadas
entre as três páginas.

## Regras de negócio

- **Data-limite:** a situação do prazo é calculada contra o **prazo externo**. O prazo interno
  aparece em cinza na tabela e tem um indicador próprio (*Entregues no prazo interno*).
- **Quatro situações** (coluna calculada `Situação do prazo`):
  - *Entregue no prazo*: data de entrega ≤ prazo externo
  - *Entregue com atraso*: data de entrega > prazo externo
  - *Em andamento no prazo*: sem data de entrega e hoje ≤ prazo externo
  - *Em andamento com prazo vencido*: sem data de entrega e hoje > prazo externo
- **Status:** *Finalizada* quando há data de entrega; caso contrário, *Em tramitação*.
- **Por que no Power BI e não no SharePoint:** uma coluna calculada do SharePoint com HOJE só se
  recalcula quando o item é editado. No Power BI ela se recalcula a cada atualização dos dados.
- **Metas:** comparadas pelo mês da **entrega** (`Finalizadas no mês` usa a relação inativa
  `dataEntrega → calendario`). As demais visões usam o mês do **recebimento**.

## Colunas esperadas da lista

| Coluna no modelo | Tipo | Observação |
| --- | --- | --- |
| `numeroProcesso` | texto | |
| `objeto` | texto (escolha) | |
| `tipoDiligencia` | texto (escolha) | filtro |
| `prioridade` | texto (escolha) | filtro |
| `setorResponsavel` | texto | |
| `dataRecebimento` | data | filtro de período e "criação por mês" |
| `prazoInterno` | data | |
| `prazoExterno` | data | data-limite das quatro situações |
| `dataEntrega` | data | vazia enquanto a diligência está em andamento |

Metas (tabela `metas`): `mes` (primeiro dia do mês), `metaFinalizadas` (número) e
`metaPercNoPrazo` (0 a 1). Hoje são 8 finalizadas e 85% no prazo em todos os meses.

## Trocar os dados fictícios pela lista real

1. No Power BI Desktop, abra o Power Query da tabela `diligencias`.
2. Substitua as etapas `Hoje` até `ComEntrega` por
   `Fonte = SharePoint.Tables("<url do site>", [Implementation="2.0", ViewMode="All"])` e navegue até a lista.
3. Expanda as colunas de pesquisa/escolha e renomeie-as para os nomes da tabela acima.
   Os tipos de data devem ser `date`.
4. Faça o mesmo na tabela `metas`, se as metas ficarem em uma lista própria.

Medidas, colunas calculadas e visuais não precisam mudar se os nomes forem mantidos.
