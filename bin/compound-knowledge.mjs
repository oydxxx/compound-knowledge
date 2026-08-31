#!/usr/bin/env node

import { createHash } from "node:crypto";
import { cp, mkdir, readdir, readFile, rename, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pluginRoot = path.join(packageRoot, "plugins", "compound-knowledge");
const skillsRoot = path.join(pluginRoot, "skills");
const skills = ["zs-boom", "zs-plan", "zs-confidence", "zs-review", "zs-work", "zs-compound"];
const platforms = new Set(["codex", "claude", "all"]);
const commands = new Set(["install", "update", "uninstall", "status", "help"]);

function usage() {
  return `
Compound Knowledge 安装器

用法：
  compound-knowledge install --platform <codex|claude|all> [--scope <project|global|user>] [--force]
  compound-knowledge update --platform <codex|claude|all> [--scope <project|global|user>]
  compound-knowledge status --platform <codex|claude|all> [--scope <project|global|user>]
  compound-knowledge uninstall --platform <codex|claude|all> [--scope <project|global|user>] [--force]

说明：
  Codex 默认安装到当前项目的 .agents/skills/；--scope global 安装到 ~/.codex/skills/。
  Claude Code 默认安装到 ~/.claude/skills/；可显式使用 --scope user。
  install 会先检查所有目标，绝不在冲突时留下半套安装；update 会先备份旧版本。
`;
}

function fail(message) {
  console.error(`错误：${message}`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const options = { command: "help", platform: null, scope: null, force: false };
  let index = 0;
  if (argv[0] && !argv[0].startsWith("-")) {
    options.command = argv[0];
    index = 1;
  }
  while (index < argv.length) {
    const current = argv[index];
    if (current === "--platform") options.platform = argv[++index];
    else if (current === "--scope") options.scope = argv[++index];
    else if (current === "--force") options.force = true;
    else if (current === "--help" || current === "-h") options.command = "help";
    else throw new Error(`不认识的参数：${current}`);
    index += 1;
  }
  return options;
}

async function hashDirectory(directory) {
  const files = [];
  async function walk(current) {
    for (const entry of await readdir(current, { withFileTypes: true })) {
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) await walk(absolute);
      else if (entry.isFile()) files.push(absolute);
    }
  }
  await walk(directory);
  files.sort();
  const hash = createHash("sha256");
  for (const file of files) {
    hash.update(path.relative(directory, file));
    hash.update(await readFile(file));
  }
  return hash.digest("hex");
}

async function sameDirectory(left, right) {
  if (!existsSync(left) || !existsSync(right)) return false;
  return (await hashDirectory(left)) === (await hashDirectory(right));
}

function timestamp() {
  return new Date().toISOString().replaceAll(":", "-").replaceAll(".", "-");
}

function selectedPlatforms(platform) {
  return platform === "all" ? ["codex", "claude"] : [platform];
}

function codexDestination(scope) {
  return scope === "global"
    ? path.join(os.homedir(), ".codex", "skills")
    : path.join(process.cwd(), ".agents", "skills");
}

function claudeDestination() {
  return path.join(os.homedir(), ".claude", "skills", "compound-knowledge");
}

function targetsFor(options) {
  return selectedPlatforms(options.platform).flatMap((platform) => {
    if (platform === "claude") {
      return [{ label: "Claude Code compound-knowledge", source: pluginRoot, destination: claudeDestination() }];
    }
    const destinationRoot = codexDestination(options.scope);
    return skills.map((skill) => ({
      label: `Codex ${skill}`,
      source: path.join(skillsRoot, skill),
      destination: path.join(destinationRoot, skill),
    }));
  });
}

async function inspectTargets(targets) {
  return Promise.all(targets.map(async (target) => ({
    ...target,
    state: !existsSync(target.destination)
      ? "missing"
      : await sameDirectory(target.source, target.destination)
        ? "unchanged"
        : "different",
  })));
}

async function stageChanges(inspections, transaction) {
  const staged = [];
  try {
    for (const inspection of inspections.filter((item) => item.state !== "unchanged")) {
      const staging = `${inspection.destination}.staging-${transaction}`;
      await mkdir(path.dirname(staging), { recursive: true });
      await cp(inspection.source, staging, { recursive: true });
      staged.push({ ...inspection, staging });
    }
    return staged;
  } catch (error) {
    await Promise.all(staged.map((item) => rm(item.staging, { recursive: true, force: true })));
    throw error;
  }
}

async function applyInstall(inspections, options) {
  const conflicts = inspections.filter((item) => item.state === "different");
  if (conflicts.length && !options.update && !options.force) {
    fail(`发现不同内容，未写入任何文件：${conflicts.map((item) => item.label).join("、")}。请先运行 status，或使用 update 进行带备份的更新。`);
    return;
  }

  const transaction = timestamp();
  const staged = await stageChanges(inspections, transaction);
  const completed = [];
  try {
    for (const item of staged) {
      const backup = item.state === "different" ? `${item.destination}.backup-${transaction}` : null;
      if (backup) await rename(item.destination, backup);
      await rename(item.staging, item.destination);
      completed.push({ ...item, backup });
    }
  } catch (error) {
    for (const item of completed.reverse()) {
      await rm(item.destination, { recursive: true, force: true });
      if (item.backup && existsSync(item.backup)) await rename(item.backup, item.destination);
    }
    await Promise.all(staged.map((item) => rm(item.staging, { recursive: true, force: true })));
    throw error;
  }

  const stagedByDestination = new Map(staged.map((item) => [item.destination, item]));
  for (const item of inspections) {
    const change = stagedByDestination.get(item.destination);
    if (!change) console.log(`${item.label}: 已安装，内容一致`);
    else if (change.state === "different") console.log(`${item.label}: 已更新（旧版本已备份到 ${change.destination}.backup-${transaction}）`);
    else console.log(`${item.label}: 已安装`);
  }
}

async function printStatus(inspections) {
  for (const item of inspections) {
    const state = item.state === "missing" ? "未安装" : item.state === "unchanged" ? "已安装，内容一致" : "已安装，但内容不同";
    console.log(`${item.label} (${item.destination}): ${state}`);
  }
}

async function uninstall(inspections, force) {
  const changed = inspections.filter((item) => item.state === "different");
  if (changed.length && !force) {
    fail(`发现用户修改，未移除任何文件：${changed.map((item) => item.label).join("、")}。确认后加 --force。`);
    return;
  }
  const transaction = timestamp();
  for (const item of inspections) {
    if (item.state === "missing") {
      console.log(`${item.label}: 未安装`);
      continue;
    }
    const removed = `${item.destination}.removed-${transaction}`;
    await rename(item.destination, removed);
    console.log(`${item.label}: 已从发现路径移除（可恢复副本：${removed}）`);
  }
}

function validateOptions(options) {
  if (!commands.has(options.command)) return `不认识的命令：${options.command}。请使用 install、update、status、uninstall 或 help。`;
  if (options.command === "help") return null;
  if (!options.platform || !platforms.has(options.platform)) return "请通过 --platform 指定 codex、claude 或 all。";
  if (options.scope && !["project", "global", "user"].includes(options.scope)) return "--scope 只支持 project、global 或 user。";
  if (options.platform === "all" && options.scope) return "同时安装多个平台时不要传 --scope；它们使用各自默认位置。";
  if (options.platform === "codex" && options.scope === "user") return "Codex 的 --scope 只支持 project 或 global。";
  if (options.platform === "claude" && options.scope && options.scope !== "user") return "Claude Code 的 --scope 只支持 user。";
  return null;
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    fail(error.message);
    console.log(usage());
    return;
  }

  const validationError = validateOptions(options);
  if (validationError) {
    fail(validationError);
    console.log(usage());
    return;
  }
  if (options.command === "help") {
    console.log(usage());
    return;
  }

  const inspections = await inspectTargets(targetsFor(options));
  if (options.command === "status") return printStatus(inspections);
  if (options.command === "uninstall") return uninstall(inspections, options.force);

  await applyInstall(inspections, { ...options, update: options.command === "update" });
  if (process.exitCode) return;
  if (selectedPlatforms(options.platform).includes("codex")) {
    console.log("\nCodex：新开任务后输入 $zs-boom 我有一堆事情，但不知道该先想清楚什么。");
  }
  if (selectedPlatforms(options.platform).includes("claude")) {
    console.log("Claude Code：新开会话后输入 /compound-knowledge:zs-boom 我有一堆事情，但不知道该先想清楚什么。");
  }
}

main().catch((error) => fail(error.stack || error.message));
