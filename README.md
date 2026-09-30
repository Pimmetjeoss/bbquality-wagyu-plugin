# BBQuality Wagyu-plugin

Officiële repository-marketplace voor de **BBQuality Wagyu** ChatGPT-plugin.

De plugin combineert:

- een Nederlandstalige Wagyu-skill;
- de live, read-only BBQuality Wagyu MCP-server;
- een MCP Apps-interface met recepten, producten, vleesplanning en winkelmandpreview;
- een native global/sidebar-entrypoint voor ondersteunde ChatGPT-hosts.

## Installeren in ChatGPT

Open **Plug-ins → Marktplaatsen → Marktplaats toevoegen** en vul in:

- **Bron:** `Pimmetjeoss/bbquality-wagyu-plugin`
- **Git-referentie:** `main`
- **Sparse-paden:** leeg laten

Open daarna de Plugin Directory, selecteer **BBQuality Plugins** en installeer **BBQuality Wagyu**.

## Live MCP-server

`https://bbquality-mcp-staging.pim-3f7.workers.dev/mcp`

De server is publiek en read-only. De winkelmandfunctie maakt uitsluitend een preview; er wordt niets besteld, betaald of aan een echte winkelwagen toegevoegd.

## Repository-indeling

- `.agents/plugins/marketplace.json` — repo-marketplace voor ChatGPT/Codex.
- `plugins/bbquality-wagyu/plugin.json` — portable Agent Plugin-manifest.
- `plugins/bbquality-wagyu/mcp.json` — remote Streamable HTTP MCP-configuratie.
- `plugins/bbquality-wagyu/skills/` — Wagyu-workflow.
- `plugins/bbquality-wagyu/assets/` — pluginiconen.
- `scripts/validate_plugin.py` — schema-, pad- en endpointvalidatie.

## Verificatie

```bash
python -m pip install jsonschema
python scripts/validate_plugin.py
```

Uitgebracht voor marketplace-testing op 30 september 2026.
