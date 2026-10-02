#!/usr/bin/env node
/**
 * PreToolUse hook : SQL destructive operations guard
 *
 * Bloque (exit 2 = abort + message) si une commande Bash/shell contient
 * DROP, TRUNCATE ou DELETE FROM sans WHERE → évite les accidents Snowflake.
 *
 * Les requêtes SELECT, INSERT, UPDATE (avec WHERE) passent librement.
 *
 * Lecture stdin ASYNCHRONE : process.stdin.read() synchrone renvoyait null
 * avant l'arrivée des données → le hook laissait tout passer (bug 2026-09-03).
 */

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => (raw += d));
process.stdin.on("end", () => {
  let input = {};
  try {
    input = JSON.parse(raw || "{}");
  } catch (_) {
    process.exit(0);
  }

  const toolName = input.tool_name || "";
  const toolInput = input.tool_input || {};

  const SHELL_TOOLS = ["Bash", "bash", "PowerShell", "run_in_terminal"];
  if (!SHELL_TOOLS.includes(toolName)) process.exit(0);

  const cmd =
    typeof toolInput === "string"
      ? toolInput
      : toolInput.command || toolInput.cmd || "";
  if (!cmd) process.exit(0);

  let reason = "";
  for (const sql of sqlReel(cmd, input.cwd)) {
    reason = jugerSql(sql);
    if (reason) break;
  }

  if (reason) {
    console.error(
      `\n🛑 SQL GUARD : Opération destructive détectée : ${reason}\n` +
        `   Commande : ${cmd.substring(0, 120)}${cmd.length > 120 ? "…" : ""}\n\n` +
        `   Demande à Yann une confirmation explicite dans le chat ;\n` +
        `   il exécute lui-même ou via /socle:livrer.\n`
    );
    process.exit(2);
  }
  process.exit(0);
});

/** Enlève les guillemets d'un argument shell et les échappements \" d'une chaîne double. */
function deguillemeter(s) {
  if (s.length >= 2 && (s[0] === '"' || s[0] === "'") && s[s.length - 1] === s[0]) {
    const inner = s.slice(1, -1);
    return s[0] === '"' ? inner.replace(/\\(["\\])/g, "$1") : inner;
  }
  return s;
}

function lireFichier(chemin, cwd) {
  try {
    return require("fs").readFileSync(
      require("path").resolve(cwd || process.cwd(), chemin),
      "utf8"
    );
  } catch (_) {
    return "";
  }
}

/**
 * Ne rend que le SQL réel d'une commande shell :
 *  - snow sql -q "..." / --query "..."  (la chaîne)
 *  - snow sql -f x.sql / --filename x.sql  (le contenu du fichier)
 *  - python ... x.sql  (le contenu du fichier cité)
 * git commit, grep, echo, cat, sed, rg, Select-String... : rien, donc jamais bloqués.
 */
function sqlReel(cmd, cwd) {
  const out = [];
  const arg = String.raw`("(?:\\.|[^"\\])*"|'[^']*'|[^\s"']+)`;
  if (/\bsnow(?:\.exe)?\s+sql\b/i.test(cmd)) {
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)(?:-q|--query)(?:\s+|=)` + arg, "g"))) {
      out.push(deguillemeter(m[1]));
    }
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)(?:-f|--filename)(?:\s+|=)` + arg, "g"))) {
      out.push(lireFichier(deguillemeter(m[1]), cwd));
    }
  }
  if (/\bpython[\d.]*(?:\.exe)?["']?\s/i.test(cmd)) {
    for (const m of cmd.matchAll(/(?:^|\s)["']?([^\s"']+\.sql)["']?(?=\s|$)/gi)) {
      out.push(lireFichier(m[1], cwd));
    }
  }
  return out;
}

/** Une raison de blocage (chaîne) ou "". Le WHERE doit être dans la MÊME instruction (découpe sur ;). */
function jugerSql(sql) {
  const propre = sql.replace(/\/\*[\s\S]*?\*\//g, " ").replace(/--[^\n]*/g, " ");
  for (const brut of propre.split(";")) {
    const st = brut.toUpperCase();
    if (/\bDROP\s+(TABLE|SCHEMA|DATABASE|VIEW|FUNCTION|PROCEDURE|STREAMLIT|STAGE)\b/.test(st))
      return "DROP (suppression définitive d'un objet Snowflake)";
    if (/\bTRUNCATE\b/.test(st)) return "TRUNCATE (vidage complet d'une table)";
    if (/\bDELETE\s+FROM\b/.test(st) && !/\bWHERE\b/.test(st))
      return "DELETE FROM sans clause WHERE (suppression totale)";
    if (/^\s*UPDATE\b/.test(st) && !/\bWHERE\b/.test(st))
      return "UPDATE sans clause WHERE (modification de toutes les lignes)";
  }
  return "";
}
