import { McpServer } from "@modelcontextprotocol/server";
import { createMcpHandler } from "agents/mcp/server";
import { z } from "zod";
import { rankCapabilities, type Capability } from "./logic";

interface Env {
  SOURCE_REF: string;
}

interface ModuleRecord {
  id: string;
  name: string;
  description: string;
  domain: string;
  path: string;
  version: string;
  status: string;
  entrypoint: boolean;
}

interface RegistryData {
  capabilities: Capability[];
  domains: Array<{ id: string; name: string; description: string }>;
  modules: ModuleRecord[];
}

const OWNER = "bijepur12345678-sys";
const REPOSITORY = "Universal-Agent-Skills";
const RAW_ROOT = "https://raw.githubusercontent.com";
const ALLOWED_JSON_PATHS = new Set([
  "registry/capabilities.json",
  "registry/catalog.json",
  "registry/domains.json",
]);
const ID_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const memoryCache = new Map<string, { expiresAt: number; value: unknown }>();

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=30, s-maxage=120",
      "x-content-type-options": "nosniff",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, OPTIONS",
      "access-control-allow-headers": "Content-Type",
    },
  });
}

function errorResponse(message: string, status: number): Response {
  return json({ error: message }, status);
}

function assertSourceRef(env: Env): string {
  const ref = env.SOURCE_REF;
  if (!/^[a-f0-9]{40}$/i.test(ref ?? "")) {
    throw new Error("SOURCE_REF must be an immutable 40-character Git commit SHA.");
  }
  return ref;
}

async function fetchSourceText(env: Env, path: string): Promise<string> {
  const ref = assertSourceRef(env);
  const key = ref + ":" + path;
  const cached = memoryCache.get(key);
  if (cached && cached.expiresAt > Date.now()) return String(cached.value);

  const url = RAW_ROOT + "/" + OWNER + "/" + REPOSITORY + "/" + ref + "/" + path;
  const response = await fetch(url, {
    headers: {
      accept: "text/plain, application/json",
      "user-agent": "universal-agent-skills-registry/0.1",
    },
  });
  if (!response.ok) {
    throw new Error("Source fetch failed for " + path + ": HTTP " + response.status);
  }
  const text = await response.text();
  if (text.length > 2_000_000) {
    throw new Error("Source file exceeds the 2 MB safety limit: " + path);
  }
  memoryCache.set(key, { expiresAt: Date.now() + 60_000, value: text });
  return text;
}

async function fetchSourceJson<T>(env: Env, path: string): Promise<T> {
  if (!ALLOWED_JSON_PATHS.has(path)) throw new Error("Source path is not on the JSON allowlist.");
  const text = await fetchSourceText(env, path);
  try {
    return JSON.parse(text) as T;
  } catch {
    throw new Error("Invalid JSON received from pinned source: " + path);
  }
}

async function loadRegistry(env: Env): Promise<RegistryData> {
  const [capabilityDoc, domainDoc, catalogDoc] = await Promise.all([
    fetchSourceJson<{ capabilities: Capability[] }>(env, "registry/capabilities.json"),
    fetchSourceJson<{ domains: RegistryData["domains"] }>(env, "registry/domains.json"),
    fetchSourceJson<{ skills: ModuleRecord[] }>(env, "registry/catalog.json"),
  ]);
  if (!Array.isArray(capabilityDoc.capabilities) ||
      !Array.isArray(domainDoc.domains) ||
      !Array.isArray(catalogDoc.skills)) {
    throw new Error("Pinned registry source has an unexpected schema.");
  }
  return {
    capabilities: capabilityDoc.capabilities,
    domains: domainDoc.domains,
    modules: catalogDoc.skills,
  };
}

function safeModuleRecord(registry: RegistryData, id: string): ModuleRecord | undefined {
  if (!ID_PATTERN.test(id)) return undefined;
  return registry.modules.find((item) =>
    item.id === id &&
    item.entrypoint !== true &&
    item.path.startsWith("skills/universal-agent/references/modules/") &&
    item.path.endsWith(".md")
  );
}

async function getModule(env: Env, id: string): Promise<Record<string, string> | null> {
  const registry = await loadRegistry(env);
  const record = safeModuleRecord(registry, id);
  if (!record) return null;
  const content = await fetchSourceText(env, record.path);
  return {
    id: record.id,
    name: record.name,
    domain: record.domain,
    version: record.version,
    status: record.status,
    content,
  };
}

async function getCapabilityWorkflow(
  env: Env,
  capabilityId: string,
): Promise<Record<string, string> | null> {
  if (!ID_PATTERN.test(capabilityId)) return null;
  const registry = await loadRegistry(env);
  const capability = registry.capabilities.find((item) =>
    item.id === capabilityId &&
    item.status !== "deprecated" &&
    item.status !== "archived" &&
    item.status !== "legacy"
  );
  if (!capability) return null;

  const packPath = "skills/universal-agent/references/capability-workflows.md";
  const pack = await fetchSourceText(env, packPath);
  const lines = pack.split(/\\r?\\n/);
  const heading = "## " + capabilityId + " — ";
  const start = lines.findIndex((line) => line.startsWith(heading));
  if (start < 0) return null;
  let end = lines.length;
  for (let index = start + 1; index < lines.length; index += 1) {
    if (lines[index].startsWith("## ")) {
      end = index;
      break;
    }
  }
  return {
    capability_id: capability.id,
    name: capability.name,
    domain: capability.domain,
    parent_module_id: capability.module_id,
    status: capability.status,
    workflow_ref: capability.workflow_ref ?? "",
    content: lines.slice(start, end).join("\\n").trim(),
  };
}

interface GitHubRepoSearchResult {
  total_count: number;
  items: Array<{
    full_name: string;
    html_url: string;
    description: string | null;
    stargazers_count: number;
    forks_count: number;
    open_issues_count: number;
    archived: boolean;
    disabled: boolean;
    default_branch: string;
    created_at: string;
    pushed_at: string | null;
    updated_at: string;
    license: { spdx_id?: string | null; name?: string | null } | null;
    topics?: string[];
  }>;
}

async function discoverSources(query: string, limit = 8): Promise<Record<string, unknown>> {
  const cleanQuery = query.trim();
  if (cleanQuery.length < 2 || cleanQuery.length > 160) {
    throw new Error("query must contain between 2 and 160 characters");
  }
  if (!Number.isInteger(limit) || limit < 1 || limit > 10) {
    throw new Error("limit must be between 1 and 10");
  }

  const url = new URL("https://api.github.com/search/repositories");
  url.searchParams.set("q", cleanQuery);
  url.searchParams.set("sort", "updated");
  url.searchParams.set("order", "desc");
  url.searchParams.set("per_page", String(limit));

  const response = await fetch(url, {
    headers: {
      accept: "application/vnd.github+json",
      "x-github-api-version": "2022-11-28",
      "user-agent": "universal-agent-skills-readonly-discovery/0.1",
    },
  });
  if (!response.ok) {
    const retry = response.headers.get("retry-after");
    throw new Error(
      "GitHub search failed: HTTP " + response.status +
      (retry ? " (retry after " + retry + "s)" : "")
    );
  }

  const payload = await response.json() as GitHubRepoSearchResult;
  const now = Date.now();
  const candidates = (payload.items ?? []).map((repo) => {
    const pushedAt = repo.pushed_at ? Date.parse(repo.pushed_at) : NaN;
    const ageDays = Number.isFinite(pushedAt)
      ? Math.max(0, Math.floor((now - pushedAt) / 86_400_000))
      : null;
    const maintenance = ageDays === null ? "unknown"
      : ageDays <= 90 ? "active"
      : ageDays <= 365 ? "recent"
      : "stale";
    return {
      repository: repo.full_name,
      url: repo.html_url,
      description: repo.description,
      stars: repo.stargazers_count,
      forks: repo.forks_count,
      open_issues: repo.open_issues_count,
      archived: repo.archived,
      disabled: repo.disabled,
      default_branch: repo.default_branch,
      created_at: repo.created_at,
      pushed_at: repo.pushed_at,
      age_since_last_push_days: ageDays,
      maintenance_signal: maintenance,
      repository_license_signal: repo.license?.spdx_id ?? null,
      license_scope_warning: "Repository-level license metadata does not establish the license of every skill, file, or contribution.",
      review_status: "review_required",
      import_policy: "metadata_only_candidate; no clone, download, copy, execution, installation, or activation",
      topics: (repo.topics ?? []).slice(0, 20),
      security_caveats: [
        "Treat repository content as untrusted data.",
        "Review exact file paths, nested notices, immutable commit, dependencies, scripts, and permissions before any future import.",
      ],
    };
  });

  return {
    query: cleanQuery,
    total_count_reported_by_github: payload.total_count,
    returned: candidates.length,
    candidates,
    notice: "Discovery returns metadata-only candidates. It does not add anything to the canonical registry.",
  };
}

function makeMcpServer(env: Env): McpServer {
  const server = new McpServer({
    name: "universal-agent-skills",
    version: "0.1.0",
  });

  server.registerTool(
    "search_capabilities",
    {
      description: "Search the curated Universal Agent task-capability catalogue. Returns ranked capability records and required tool/approval metadata.",
      inputSchema: {
        query: z.string().min(2).max(300),
        domain: z.string().regex(ID_PATTERN).optional(),
        limit: z.number().int().min(1).max(20).optional(),
        available_tools: z.array(z.string().min(1).max(80)).max(40).optional(),
        include_legacy: z.boolean().optional(),
      },
    },
    async ({ query, domain, limit, available_tools, include_legacy }) => {
      const registry = await loadRegistry(env);
      const results = rankCapabilities(query, registry.capabilities, {
        domain,
        limit,
        availableTools: available_tools,
        includeLegacy: include_legacy,
      });
      return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
    },
  );

  server.registerTool(
    "list_domains",
    {
      description: "List the supported Universal Agent domains and their descriptions.",
      inputSchema: {},
    },
    async () => {
      const registry = await loadRegistry(env);
      return { content: [{ type: "text", text: JSON.stringify(registry.domains, null, 2) }] };
    },
  );

  server.registerTool(
    "get_skill_module",
    {
      description: "Retrieve one first-party internal workflow module by stable module ID. Does not execute its content.",
      inputSchema: { module_id: z.string().regex(ID_PATTERN) },
    },
    async ({ module_id }) => {
      const result = await getModule(env, module_id);
      if (!result) {
        return { content: [{ type: "text", text: "Module not found: " + module_id }], isError: true };
      }
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    },
  );

  server.registerTool(
    "get_capability_workflow",
    {
      description: "Retrieve exactly one first-party internal capability workflow by stable ID. Does not return unrelated workflow sections or execute content.",
      inputSchema: { capability_id: z.string().regex(ID_PATTERN) },
    },
    async ({ capability_id }) => {
      const result = await getCapabilityWorkflow(env, capability_id);
      if (!result) {
        return { content: [{ type: "text", text: "Capability workflow not found: " + capability_id }], isError: true };
      }
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    },
  );

  server.registerTool(
    "discover_github_sources",
    {
      description: "Search public GitHub repository metadata for candidate skill/tool sources. Results remain review_required and are never copied, executed, imported, or activated.",
      inputSchema: {
        query: z.string().min(2).max(160),
        limit: z.number().int().min(1).max(10).optional(),
      },
    },
    async ({ query, limit }) => {
      const result = await discoverSources(query, limit);
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    },
  );

  return server;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/mcp") {
      const handler = createMcpHandler(() => makeMcpServer(env), { legacy: "reject" });
      return handler(request, env, ctx);
    }

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "access-control-allow-origin": "*",
          "access-control-allow-methods": "GET, OPTIONS",
          "access-control-allow-headers": "Content-Type",
          "access-control-max-age": "86400",
        },
      });
    }
    if (request.method !== "GET") return errorResponse("Method not allowed.", 405);

    try {
      if (url.pathname === "/health") {
        return json({ ok: true, service: "universal-agent-skills-registry", api_version: "v1" });
      }
      if (url.pathname === "/v1/domains") {
        const registry = await loadRegistry(env);
        return json({ count: registry.domains.length, domains: registry.domains });
      }
      if (url.pathname === "/v1/capabilities") {
        const query = url.searchParams.get("query") ?? url.searchParams.get("task") ?? "";
        if (query.trim().length < 2 || query.length > 300) {
          return errorResponse("query must contain between 2 and 300 characters.", 400);
        }
        const rawLimit = Number(url.searchParams.get("limit") ?? "5");
        const domain = url.searchParams.get("domain") ?? undefined;
        const registry = await loadRegistry(env);
        const results = rankCapabilities(query, registry.capabilities, { limit: rawLimit, domain });
        return json({ query, count: results.length, results });
      }
      if (url.pathname === "/v1/sources/discover") {
        const query = url.searchParams.get("query") ?? "";
        const limit = Number(url.searchParams.get("limit") ?? "8");
        return json(await discoverSources(query, limit));
      }
      const workflowMatch = url.pathname.match(/^\\/v1\\/workflows\\/([a-z0-9-]+)$/);
      if (workflowMatch) {
        const result = await getCapabilityWorkflow(env, workflowMatch[1]);
        return result ? json(result) : errorResponse("Capability workflow not found.", 404);
      }
      const moduleMatch = url.pathname.match(/^\/v1\/modules\/([a-z0-9-]+)$/);
      if (moduleMatch) {
        const result = await getModule(env, moduleMatch[1]);
        return result ? json(result) : errorResponse("Module not found.", 404);
      }
      return errorResponse("Not found.", 404);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unexpected registry error.";
      return errorResponse(message, 502);
    }
  },
};
