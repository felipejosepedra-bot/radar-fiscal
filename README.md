# Radar Fiscal — Central de Inteligência Fiscal

Site público: https://felipejosepedra-bot.github.io/radar-fiscal/

A central reúne os radares **Reforma Tributária**, **Fiscal Estadual**, **Isenções de Medicamentos**, **LE Logística** e **Relatório Farmacêutico**.

## Situação atual
- O site carrega `atualizacoes.json`, uma base versionada com os 22 registros iniciais de 2026.
- O site tem filtro por radar, UF, período, assunto, situação e empresa impactada.
- Não é obrigatório atualizar o `index.html` ao incluir nova legislação.
- A atualização **não é automática a partir dos agendamentos do ChatGPT** até que exista um conector ou executor que envie o JSON e dispare o fluxo do GitHub.

## Publicar novos registros
1. Abra **Actions > Publicar Radar Fiscal > Run workflow**.
2. No campo `novos_registros`, cole um registro JSON ou `{"atualizacoes":[...]}`.
3. Execute. O script de validação rejeita campos obrigatórios faltantes e exige ao menos uma fonte oficial em domínio `gov.br`, `leg.br` ou `jus.br`.
4. Só quando os registros são diferentes dos existentes, a base é alterada e o site é republicado.

Os campos obrigatórios são: `id`, `titulo`, `resumo`, `publicacao` (AAAA-MM-DD), `norma`, `antes`, `depois`, `providencias`, `uf` (array), `tema` (array), `impacto` (array), `fontes` (array com `titulo` e `url`). Informe também `radares`, um array dos radares de origem. `vigencia`, `tipo` e `observacoes` são recomendados.

**Não copie o exemplo como notícia verdadeira.** Cada entrada deve corresponder a uma publicação real e verificável. Use IDs estáveis para não duplicar o mesmo evento. Se a mesma atualização aparecer em outro radar, reutilize o ID para agregar as origens.

## Ativar GitHub Pages
Acesse **Settings > Pages > Build and deployment > Source: GitHub Actions**, e verifique em **Actions** se o workflow **Publicar Radar Fiscal** passou. Se houver erro de permissão em push, confira **Settings > Actions > General > Workflow permissions**.

## Integração futura com agendamentos
O agendamento precisa produzir registros JSON verificáveis e uma integração autorizada precisa executar o GitHub Actions workflow ou realizar commit com os novos registros. É necessário testar acesso e permissões. Sem alterações novas, não deve haver commit nem modificação no histórico.

Não use este repositório público para colocar dados confidenciais de empresas, clientes, NF-e, CNPJs internos, credenciais ou pareceres internos não destinados à divulgação pública.
