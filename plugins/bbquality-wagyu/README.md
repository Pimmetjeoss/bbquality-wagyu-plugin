# BBQuality Wagyu ChatGPT-plugin

Portable Agent Plugin-package voor de Wagyu-only BBQuality-assistent.

## Inhoud

- `plugin.json` — portable pluginmanifest.
- `mcp.json` — Streamable HTTP-verbinding met de bestaande staging-origin.
- `skills/bbquality-wagyu-assistant/SKILL.md` — gebundelde Nederlandse workflow.
- `assets/` — eigen Wagyu-assistenticonen; geen gekopieerd officieel woordmerk.

## Releasestatus

De Wagyu-only Worker is live gedeployd op `bbquality-mcp-staging` en protocolmatig geverifieerd met de MCP SDK en MCP Inspector. De server biedt zes Wagyu-tools en een gedeelde MCP Apps-resource met native global/sidebar-entrypointmetadata.

Live endpoint: `https://bbquality-mcp-staging.pim-3f7.workers.dev/mcp`.

Installatie verloopt via de repo-marketplace `Pimmetjeoss/bbquality-wagyu-plugin`. Een echte sidebarweergave blijft afhankelijk van hostondersteuning en de rollout op het doelaccount; de inline MCP Apps-interface blijft de fallback.

## Veiligheid

Alle workflows zijn publiek/read-only. `preview_wagyu_cart` maakt geen winkelwagen, checkout, betaling of bestelling en retourneert `checkoutUrl: null`.
