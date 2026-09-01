---
Status: DRAFT NORMATIVE FOR PERFORMANCE CLAIMS
Version: 2.0.0-beta
---

# MCP-A Benchmarking and Evaluation

## 1. Purpose

Conformance does not imply faster, cheaper, or more accurate answers. Any public
MCP-A performance, efficiency, or precision claim MUST identify a workload,
baseline, environment, quality rubric, and statistical result as defined here.

## 2. Required baselines

At least compare:

1. direct MCP orchestration, where the client model selects and calls source
   tools and consolidates results;
2. MCP-A server-side compilation over the same source capabilities;
3. a deterministic non-model service implementation when the workload permits
   one.

The same authorization scope, source snapshots, network placement, model
families, retry policy, and result-quality requirements MUST be used or the
difference must be disclosed.

## 3. Workload classes

Report separately for:

- single-source lookup;
- single-source filtered aggregation;
- multi-source fan-out without conflict;
- multi-source conflict resolution;
- ambiguous query requiring input;
- structured output with validation;
- long-running task;
- follow-up refinement;
- low-risk idempotent action;
- partial source failure.

Do not average these into one headline number without also publishing each
class.

## 4. Metrics

Required metrics are:

- end-to-end latency: p50, p95, p99;
- time to first usable result for task-based calls;
- client-model input/output tokens;
- server-model input/output tokens;
- total model and infrastructure cost using disclosed prices or normalized
  units;
- MCP round trips and downstream source calls;
- answer task success rate;
- structured schema-validity rate;
- citation precision and claim coverage;
- numeric aggregation exactness;
- entity-resolution accuracy;
- completeness and partial-result detection accuracy;
- action duplicate-effect and unintended-effect rate;
- human approval and clarification rate.

## 5. Quality and safety gates

A latency or cost win MUST NOT be reported as a protocol improvement when it
comes from a lower answer-quality, provenance, authorization, or safety target.
Benchmark runs with unauthorized leakage, hidden partial failure, invalid
structured output, duplicate effects, or incorrect aggregates count as failed
runs.

## 6. Methodology

Reports MUST disclose:

- repository and implementation revisions;
- MCP and MCP-A versions and negotiated features;
- client and server models, parameters, and prompts where publishable;
- source datasets or reproducible generators;
- warm/cold cache state;
- network topology and concurrency;
- sample count, randomization, exclusions, and confidence intervals;
- failure injection method;
- whether results were independently reviewed.

At least 100 successful attempts per ordinary workload class and 30 per
expensive class are RECOMMENDED. Report paired comparisons when the same query
and source snapshot can be used.

## 7. Reference result format

Benchmark results SHOULD be published as JSON or CSV with one row per attempt,
plus a human-readable methodology report. Raw results MUST distinguish client
and server computation so savings are not created by moving cost out of view.

## 8. Permitted claims

Acceptable: “On workload W, implementation X reduced p95 latency by Y% versus
baseline B while meeting quality gates Q.”

Not acceptable: “MCP-A is faster/more precise/cheaper than MCP” without scoped,
reproducible evidence. MCP-A is a profile used over MCP, not its competitor.
