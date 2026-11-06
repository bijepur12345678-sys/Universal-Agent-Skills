export interface Capability {
  id: string;
  domain: string;
  module_id: string;
  name: string;
  description: string;
  triggers: string[];
  synonyms: string[];
  required_tools: string[];
  risk_level: "low" | "moderate" | "elevated";
  approval_required: boolean;
  status: "stable" | "experimental" | "legacy" | "deprecated" | "archived";
  workflow_ref?: string;
}

const STOP_WORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "build", "by", "do", "for",
  "from", "get", "how", "i", "in", "is", "it", "make", "me", "my", "of",
  "on", "or", "please", "set", "that", "the", "this", "to", "use", "with",
]);
const ID_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function tokens(value: string): Set<string> {
  const matches = value.toLocaleLowerCase().match(/[a-z0-9][a-z0-9+#._-]*/g) ?? [];
  return new Set(matches.filter((token) => token.length > 1 && !STOP_WORDS.has(token)));
}

export function rankCapabilities(
  task: string,
  records: Capability[],
  options: {
    limit?: number;
    domain?: string;
    availableTools?: string[];
    includeLegacy?: boolean;
  } = {},
): Array<Record<string, unknown>> {
  const query = task.trim().toLocaleLowerCase().replace(/\s+/g, " ");
  if (!query) throw new Error("query must not be empty");
  const limit = options.limit ?? 5;
  if (!Number.isInteger(limit) || limit < 1 || limit > 20) {
    throw new Error("limit must be between 1 and 20");
  }
  if (options.domain && !ID_PATTERN.test(options.domain)) {
    throw new Error("domain must be a lowercase domain ID");
  }

  const queryTokens = tokens(query);
  const available = options.availableTools === undefined ? undefined : new Set(options.availableTools);
  const ranked: Array<Record<string, unknown> & { score: number; capability_id: string }> = [];

  for (const item of records) {
    if (item.status === "deprecated" || item.status === "archived") continue;
    if (item.status === "legacy" && !options.includeLegacy) continue;
    if (options.domain && item.domain !== options.domain) continue;

    let score = 0;
    const matched = new Set<string>();
    for (const phrase of item.triggers ?? []) {
      const normalized = phrase.toLocaleLowerCase();
      if (normalized && query.includes(normalized)) {
        score += 12;
        matched.add(normalized);
      }
    }
    for (const phrase of item.synonyms ?? []) {
      const normalized = phrase.toLocaleLowerCase();
      if (normalized && query.includes(normalized)) {
        score += 7;
        matched.add(normalized);
      }
    }
    const name = item.name.toLocaleLowerCase();
    if (name && query.includes(name)) {
      score += 10;
      matched.add(name);
    }

    const nameTokens = tokens(item.name);
    const triggerTokens = new Set((item.triggers ?? []).flatMap((value) => [...tokens(value)]));
    const synonymTokens = new Set((item.synonyms ?? []).flatMap((value) => [...tokens(value)]));
    const descriptionTokens = tokens(item.description);

    for (const token of queryTokens) {
      if (nameTokens.has(token)) { score += 4; matched.add(token); }
      if (triggerTokens.has(token)) { score += 3; matched.add(token); }
      if (synonymTokens.has(token)) { score += 2; matched.add(token); }
      if (descriptionTokens.has(token)) score += 1;
    }
    if (!score) continue;

    const requiredTools = [...new Set(item.required_tools ?? [])].sort();
    const missingTools = available
      ? requiredTools.filter((tool) => !available.has(tool))
      : [];
    ranked.push({
      capability_id: item.id,
      name: item.name,
      domain: item.domain,
      module_id: item.module_id,
      workflow_ref: item.workflow_ref ?? null,
      status: item.status,
      score,
      matched_terms: [...matched].sort(),
      required_tools: requiredTools,
      missing_tools: missingTools,
      tools_ready: available ? missingTools.length === 0 : null,
      risk_level: item.risk_level,
      approval_required: item.approval_required,
    });
  }

  ranked.sort((a, b) => b.score - a.score || a.capability_id.localeCompare(b.capability_id));
  return ranked.slice(0, limit);
}
