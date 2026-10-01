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

  const cmdUpper = cmd.toUpperCase();

  const hasDrop =
    /\bDROP\s+(TABLE|SCHEMA|DATABASE|VIEW|FUNCTION|PROCEDURE|STREAMLIT|STAGE)\b/.test(
      cmdUpper
    );
  const hasTruncate = /\bTRUNCATE\b/.test(cmdUpper);
  const hasDeleteWithoutWhere =
    /\bDELETE\s+FROM\b/.test(cmdUpper) && !/\bWHERE\b/.test(cmdUpper);

  if (hasDrop || hasTruncate || hasDeleteWithoutWhere) {
    let reason = "";
    if (hasDrop) reason = "DROP (suppression définitive d'un objet Snowflake)";
    else if (hasTruncate) reason = "TRUNCATE (vidage complet d'une table)";
    else reason = "DELETE FROM sans clause WHERE (suppression totale)";

    console.error(
      `\n🛑 SQL GUARD : Opération destructive détectée : ${reason}\n` +
        `   Commande : ${cmd.substring(0, 120)}${cmd.length > 120 ? "…" : ""}\n\n` +
        `   Pour confirmer, relance en précisant explicitement que tu valides\n` +
        `   cette opération (ex: "oui, exécute ce DROP, j'ai vérifié").\n`
    );
    process.exit(2);
  }
  process.exit(0);
});
