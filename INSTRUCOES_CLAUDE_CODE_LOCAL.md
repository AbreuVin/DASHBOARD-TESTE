# Como usar o Claude Code no seu computador com o painel da CGPRES

Objetivo: colocar o projeto em `C:\Users\vfabreu\Downloads\CGPRES` e deixar o Claude Code trabalhar
direto nessa pasta, ligando o painel à lista real do SharePoint.

> **Antes de começar:** confirme com a STI do TJBA se você pode instalar programas e usar
> ferramentas de IA na máquina do Tribunal. O Claude Code envia ao serviço da Anthropic o conteúdo
> dos arquivos que lê. Trabalhe com a **estrutura** do projeto, não com dados reais de processos.

---

## 1. Instalar o que é preciso (uma vez só)

### 1.1 Git para Windows
O Claude Code no Windows precisa do Git (ele usa o Git Bash por baixo).

1. Baixe em https://git-scm.com/download/win e instale com as opções padrão.
2. Feche e reabra o PowerShell e confira:
   ```powershell
   git --version
   ```

### 1.2 Claude Code
No **PowerShell** (não precisa ser administrador):
```powershell
irm https://claude.ai/install.ps1 | iex
```
Feche e reabra o PowerShell e confira:
```powershell
claude --version
```
Se o comando `claude` não for encontrado, reinicie o computador ou adicione ao PATH a pasta que o
instalador mostrou no final.

Instruções oficiais e alternativas: https://code.claude.com/docs/en/setup

### 1.3 (Opcional) Python, para validar os arquivos
Se quiser que o Claude valide o relatório contra os schemas da Microsoft:
```powershell
winget install Python.Python.3.12
```

---

## 2. Colocar o projeto na pasta CGPRES

Escolha **uma** das opções.

### Opção A — com Git (recomendada: dá para receber atualizações depois)
```powershell
cd $env:USERPROFILE\Downloads
git clone --branch claude/jolly-pascal-u6lui6 https://github.com/AbreuVin/DASHBOARD-TESTE.git CGPRES
```
Se a pasta `CGPRES` já existir e não estiver vazia, renomeie-a antes ou use outro nome.
Se o GitHub pedir login, entre com a sua conta (o repositório é seu).

### Opção B — com o ZIP que o Claude enviou
```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\controle_demandas_cgpres.zip" `
  -DestinationPath "$env:USERPROFILE\Downloads\CGPRES" -Force
```
Depois copie também o arquivo `CLAUDE.md` para dentro de `Downloads\CGPRES`
(é ele que dá o contexto ao Claude Code).

### Conferir
```powershell
dir $env:USERPROFILE\Downloads\CGPRES
```
Devem aparecer `controle_demandas_cgpres.pbip`, as pastas `.Report` e `.SemanticModel` e o `CLAUDE.md`.

---

## 3. Abrir o Claude Code na pasta

1. **Feche o projeto no Power BI Desktop**, se estiver aberto. Se o Desktop salvar depois, ele
   sobrescreve o que o Claude editou.
2. No PowerShell:
   ```powershell
   cd $env:USERPROFILE\Downloads\CGPRES
   claude
   ```
3. Na primeira vez ele pede para entrar na sua conta Claude e pergunta se você confia na pasta:
   responda que sim.
4. O Claude lê o `CLAUDE.md` automaticamente. Para conferir, pergunte:
   *"Resuma o projeto e as pendências que estão no CLAUDE.md."*

---

## 4. Pedir o trabalho

Responda primeiro as três pendências e cole a mensagem abaixo no Claude Code, trocando o que está
entre `< >`:

```
Leia o CLAUDE.md e o controle_demandas_cgpres.md.

Respostas às pendências:
1. Prazo (Dias): <conta a partir da Data de Entrada? corridos ou úteis? é o prazo externo?>
2. Prazo interno: <a coluna "Prazo para Orientação Complementar" é o prazo interno? se não, qual é?>
3. Prioridade: <Sim/Não basta, ou vamos criar níveis na lista?>

Tarefa:
- Adapte o modelo semântico para a estrutura real da lista ControleDemandas descrita no CLAUDE.md:
  renomeie colunas, trate tipoDiligencia e objeto como múltipla escolha com tabelas-ponte,
  use Prioridade Sim/Não e acrescente Origem e Unidade Destino como filtros.
- Mantenha os dados fictícios, agora no formato da lista real, e crie o parâmetro
  UsarDadosFicticios para alternar entre eles e SharePoint.Tables.
- Ajuste os visuais que mudarem de campo e mantenha a identidade visual.
- Valide todos os JSON do relatório contra os schemas oficiais da Microsoft.
- Não leia nem copie dados reais da lista.
- No fim, me diga exatamente o que conferir quando eu abrir no Power BI Desktop.
```

Enquanto trabalha, o Claude vai pedir permissão para editar arquivos e rodar comandos. Leia cada
pedido e aprove. Para ele parar, aperte `Esc`.

---

## 5. Testar no Power BI Desktop

1. Abra `Downloads\CGPRES\controle_demandas_cgpres.pbip`.
2. Clique em **Atualizar**. Com `UsarDadosFicticios = true`, os dados fictícios carregam.
3. Para usar a lista real:
   - Vá em **Transformar dados → Editar parâmetros**, mude `UsarDadosFicticios` para `false` e atualize.
   - Na primeira vez, o Desktop pede credenciais do SharePoint: escolha **Conta organizacional** e
     entre com o seu login do TJBA.
4. Se aparecer erro, tire um print da mensagem e cole no Claude Code. Diga em qual tabela e etapa do
   Power Query o erro apareceu.

---

## 6. Guardar as alterações (só na Opção A)

```powershell
cd $env:USERPROFILE\Downloads\CGPRES
git status
git add -A
git commit -m "Liga o painel à lista real do SharePoint"
git push
```
Você também pode pedir ao Claude: *"faça o commit e o push das alterações"*.

---

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| `claude` não é reconhecido | Reabra o PowerShell; se persistir, reinicie o Windows |
| Pede Git Bash / "git not found" | Instale o Git para Windows (passo 1.1) |
| Instalação bloqueada | Política da máquina do TJBA: fale com a STI |
| Power BI diz que o projeto foi alterado fora | Normal: aceite recarregar |
| Visual em branco depois da troca para a lista real | O nome de alguma coluna mudou: mande o erro ao Claude |
| Credenciais do SharePoint recusadas | Arquivo → Opções → Configurações da fonte de dados → limpar permissões e entrar de novo |
