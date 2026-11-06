import { describe, expect, it } from "vitest";
import { rankCapabilities } from "../src/logic";
import type { Capability } from "../src/logic";

const records: Capability[] = [
  {
    id: "cloud-serverless-apps",
    name: "Serverless application architecture",
    domain: "cloud",
    module_id: "domain-cloud",
    description: "Design and implement serverless APIs and edge applications.",
    triggers: ["Cloudflare Workers", "serverless API", "edge function"],
    synonyms: ["edge compute", "cloud function"],
    required_tools: ["cloudflare-workers"],
    risk_level: "moderate",
    approval_required: false,
    status: "experimental",
  },
  {
    id: "youtube-analytics",
    name: "YouTube analytics and reporting",
    domain: "youtube",
    module_id: "domain-youtube",
    description: "Interpret authorized channel analytics and audience retention.",
    triggers: ["YouTube Analytics", "audience retention"],
    synonyms: ["creator analytics", "channel dashboard"],
    required_tools: ["youtube-analytics-api"],
    risk_level: "moderate",
    approval_required: false,
    status: "experimental",
  },
  {
    id: "archived-old",
    name: "Old Cloud Deployment",
    domain: "cloud",
    module_id: "domain-cloud",
    description: "Deprecated archived cloud deployment instructions.",
    triggers: ["old cloud deployment"],
    synonyms: [],
    required_tools: [],
    risk_level: "low",
    approval_required: false,
    status: "archived",
  },
];

describe("rankCapabilities", () => {
  it("routes a Cloudflare Worker task to the cloud capability", () => {
    const result = rankCapabilities("build a Cloudflare Workers serverless API", records);
    expect(result[0]?.capability_id).toBe("cloud-serverless-apps");
  });

  it("routes YouTube analytics to the YouTube capability", () => {
    const result = rankCapabilities("analyze YouTube analytics and audience retention", records);
    expect(result[0]?.capability_id).toBe("youtube-analytics");
  });

  it("reports tools that are not available", () => {
    const result = rankCapabilities("Cloudflare Workers API", records, { availableTools: [] });
    expect(result[0]?.missing_tools).toEqual(["cloudflare-workers"]);
    expect(result[0]?.tools_ready).toBe(false);
  });

  it("filters by domain", () => {
    const result = rankCapabilities("YouTube analytics Cloudflare Workers", records, { domain: "youtube" });
    expect(result.every((item) => item.domain === "youtube")).toBe(true);
  });

  it("excludes archived records by default", () => {
    const result = rankCapabilities("old cloud deployment", records);
    expect(result.some((item) => item.capability_id === "archived-old")).toBe(false);
  });

  it("rejects invalid limits and empty tasks", () => {
    expect(() => rankCapabilities(" ", records)).toThrow("query must not be empty");
    expect(() => rankCapabilities("cloud", records, { limit: 21 })).toThrow("limit must be between 1 and 20");
  });
});
