import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { mkdir, mkdtemp, readFile, readdir, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cli = path.join(root, "bin", "compound-knowledge.mjs");
const skills = ["zs-boom", "zs-plan", "zs-confidence", "zs-review", "zs-work", "zs-compound"];

function run(args, cwd, home) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd,
    env: { ...process.env, HOME: home },
    encoding: "utf8",
  });
}

test("installs, protects, updates, and uninstalls Codex skills", async () => {
  const sandbox = await mkdtemp(path.join(tmpdir(), "compound-knowledge-installer-"));
  const project = path.join(sandbox, "project");
  const home = path.join(sandbox, "home");
  await mkdir(project, { recursive: true });

  let result = run(["install", "--platform", "codex"], project, home);
  assert.equal(result.status, 0, result.stderr);
  for (const skill of skills) {
    const skillFile = path.join(project, ".agents", "skills", skill, "SKILL.md");
    assert.match(await readFile(skillFile, "utf8"), new RegExp(`name: ${skill}`));
  }

  result = run(["status", "--platform", "codex"], project, home);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /已安装，内容一致/);

  const modified = path.join(project, ".agents", "skills", "zs-boom", "SKILL.md");
  await writeFile(modified, `${await readFile(modified, "utf8")}\n本地修改\n`);
  result = run(["install", "--platform", "codex"], project, home);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /发现不同内容，未写入任何文件/);

  result = run(["update", "--platform", "codex"], project, home);
  assert.equal(result.status, 0, result.stderr);
  const backups = await readdir(path.join(project, ".agents", "skills"));
  assert.ok(backups.some((entry) => entry.startsWith("zs-boom.backup-")));

  result = run(["uninstall", "--platform", "codex"], project, home);
  assert.equal(result.status, 0, result.stderr);
  const remaining = await readdir(path.join(project, ".agents", "skills"));
  assert.ok(remaining.every((entry) => entry.includes(".backup-") || entry.includes(".removed-")));
});

test("installs Claude Code as a user skills-directory plugin", async () => {
  const sandbox = await mkdtemp(path.join(tmpdir(), "compound-knowledge-installer-"));
  const project = path.join(sandbox, "project");
  const home = path.join(sandbox, "home");
  await mkdir(project, { recursive: true });

  const result = run(["install", "--platform", "claude"], project, home);
  assert.equal(result.status, 0, result.stderr);
  const pluginManifest = path.join(home, ".claude", "skills", "compound-knowledge", ".claude-plugin", "plugin.json");
  assert.match(await readFile(pluginManifest, "utf8"), /compound-knowledge/);
});

test("preflights every target before writing any Codex skill", async () => {
  const sandbox = await mkdtemp(path.join(tmpdir(), "compound-knowledge-installer-"));
  const project = path.join(sandbox, "project");
  const home = path.join(sandbox, "home");
  const conflicting = path.join(project, ".agents", "skills", "zs-plan");
  await mkdir(conflicting, { recursive: true });
  await writeFile(path.join(conflicting, "SKILL.md"), "用户已有的技能\n");

  const result = run(["install", "--platform", "codex"], project, home);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /未写入任何文件/);
  assert.equal(await readFile(path.join(conflicting, "SKILL.md"), "utf8"), "用户已有的技能\n");
  assert.equal(pathExists(path.join(project, ".agents", "skills", "zs-boom")), false);
});

test("rejects a shared scope that would silently target the wrong platform", async () => {
  const sandbox = await mkdtemp(path.join(tmpdir(), "compound-knowledge-installer-"));
  const result = run(["install", "--platform", "all", "--scope", "global"], sandbox, path.join(sandbox, "home"));
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /不要传 --scope/);
});

function pathExists(target) {
  return existsSync(target);
}
